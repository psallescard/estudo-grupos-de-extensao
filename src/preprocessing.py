from enum import Enum

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize


class Distribution(Enum):
    NORMAL = (lambda p1, p2: stats.norm(loc=p1, scale=p2), -np.inf)
    LOGNORMAL = (lambda p1, p2: stats.lognorm(s=p2, scale=np.exp(p1)), 0.0)

    def __init__(self, factory, lower_bound):
        self._factory = factory
        self.lower_bound = lower_bound

    def __call__(self, p1: float, p2: float):
        return self._factory(p1, p2)

    def cdf(self, x, p1: float, p2: float):
        return self._factory(p1, p2).cdf(x)

    def __str__(self) -> str:
        return self.name.capitalize()


def convert_responses(df_renamed: pd.DataFrame, exclude_non_poli: bool = False) -> pd.DataFrame:
    df = df_renamed.copy()

    obj_cols = df.select_dtypes(include="str").columns
    df[obj_cols] = df[obj_cols].apply(lambda s: s.str.strip())

    df = df.drop(columns=["termo_consentimento", "timestamp"])

    # Columns whose categories order does not matter
    nominal_cols = [
        "curso",
        "tipo_escola",
        "area_pretendida",
        "grupo_extensao",
        "motivacao_ingresso",
        "faz_atividade_remunerada",
        "objetivo_faculdade",
    ]
    for col in nominal_cols:
        df[col] = df[col].astype("category")

    # Categories where order matter
    ordinal_orders = {
        "tempo_deslocamento": [
            "Menos de 30 min",
            "30 a 60 min",
            "60 a 120 min",
            "Mais de 120 min",
        ],
        "renda_familiar": [
            "Até 3 salários mínimos",
            "De 3 a 10 salários mínimos",
            "De 10 a 20 salários mínimos",
            "Acima de 20 salários mínimos",
        ],  # "Prefiro não informar" converts to NaN
        "media_ponderada": [
            "Menor que 5.0",
            "5.0 a 5.9",
            "6.0 a 6.9",
            "7.0 a 7.9",
            "8.0 a 8.9",
            "9.0 a 10.0",
        ],  # "Prefiro não informar" converts to NaN
        "tempo_grupo": [
            "Menos de 6 meses",
            "6 meses a 1 ano",
            "1 a 2 anos",
            "Mais de 2 anos",
        ],
        "horas_semanais_grupo": [
            "1 a 5h",
            "6 a 10h",
            "11 a 20h",
            "21 a 40h",
            "Mais de 40h",
        ],
        "momento_estagio": [
            "Antes do 3º ano",
            "No 3ºano",
            "No 4ºano",
            "A partir do 5ºano",
            "Não pretendo realizar estágio",
        ],
    }
    for col, categories in ordinal_orders.items():
        df[col] = pd.Categorical(df[col], categories=categories, ordered=True)

    # Explode multiple choice variable into boolean flags
    raw_extra = df["outras_extracurriculares"]
    df["extra_esportes"] = raw_extra.str.contains("Esportes", regex=False)
    df["extra_outro_grupo"] = raw_extra.str.contains("Outros grupos de extensão", regex=False)
    df["extra_ca_gremio"] = raw_extra.str.contains("Gestão de CAs ou Grêmios", regex=False)
    df = df.drop(columns=["outras_extracurriculares"])

    if exclude_non_poli:
        df = df[df["curso"] != "Não faço Poli"].copy()
        df["curso"] = df["curso"].cat.remove_unused_categories()

    return df.reset_index(drop=True)


def fit_binned_mle(freqs, edges, cdf_func, initial_guess):
    # negative because scipy optimization function minimize values, but we need to maximize
    def negative_log_likelihood(params):
        cdf_values = cdf_func(edges, *params)
        probabilities = np.clip(np.diff(cdf_values), 1e-15, 1.0)
        # -SUM[ n_j ln[p_j(theta)] ]
        return -np.sum(freqs * np.log(probabilities))

    # Solve MLE with numerical calc
    result = minimize(
        negative_log_likelihood,
        x0=initial_guess,
        bounds=[(None, None), (1e-5, None)],  # mean is unbounded, var must be strictly positive
        tol=1e-4,
    )
    return result.x


def chi_square_gof(counts, edges, cdf_func, params, alpha=0.05):
    probabilities = np.diff(cdf_func(edges, *params))
    expected = np.sum(counts) * probabilities  # expected values vector

    dof = len(counts) - 1 - len(params)  # K - p - 1
    chi2_stat = np.sum((counts - expected) ** 2 / expected)
    chi2_crit = stats.chi2.ppf(1 - 0.05, df=dof)
    p_value = stats.chi2.sf(chi2_stat, df=dof)

    return expected, chi2_stat, chi2_crit, dof, p_value


def run_adhesion_tests(df, variables_config, alpha=0.05):
    results = []
    for var in variables_config:
        observed = df[var["col"]].value_counts().reindex(var["order"], fill_value=0.0).to_numpy()

        for dist, guess in var["guesses"].items():
            edges = [dist.lower_bound] + var["upper_edges"]
            params = fit_binned_mle(observed, edges, dist.cdf, initial_guess=guess)
            gof_metrics = chi_square_gof(observed, edges, dist.cdf, params, alpha)
            results.append((var["label"], str(dist), params, observed, *gof_metrics))

    return results


def compute_bin_expected_values(edges, dist):
    """Computes E[X | a_{j-1} < X <= a_j] for any frozen scipy.stats distribution."""
    edges = np.asarray(edges, dtype=float)
    return np.array([dist.expect(lb=low, ub=high, conditional=True) for low, high in zip(edges[:-1], edges[1:])])
