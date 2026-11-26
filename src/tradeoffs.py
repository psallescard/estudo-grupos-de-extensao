"""Statistical helpers for front 2 (trade-offs, performance and time allocation)."""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

ALPHA = 0.05
CONFIDENCE_LEVEL = 0.95
HOURS_ORDER = ["1 a 5h", "6 a 10h", "11 a 20h", "21 a 40h", "Mais de 40h"]
HIGH_PERFORMANCE_BANDS = ["8.0 a 8.9", "9.0 a 10.0"]
PAID_ACTIVITY_ORDER = ["Não", "Sim (parcial ou recorrente)"]


def _mean_confidence_interval(values: pd.Series, confidence_level: float) -> tuple[float, float, float]:
    """Return a sample mean and its two-sided Student t confidence interval."""
    sample = values.dropna().to_numpy(dtype=float)
    mean = float(sample.mean())
    if sample.size < 2:
        return mean, np.nan, np.nan
    half_width = stats.t.ppf((1 + confidence_level) / 2, sample.size - 1) * (
        sample.std(ddof=1) / np.sqrt(sample.size)
    )
    return mean, float(mean - half_width), float(mean + half_width)


def prepare_p1_data(df: pd.DataFrame) -> pd.DataFrame:
    """Keep students who reported a weighted average and flag scores of at least 8.0."""
    data = df.dropna(subset=["media_ponderada"]).copy()
    data["alto_rendimento"] = data["media_ponderada"].isin(HIGH_PERFORMANCE_BANDS)
    return data


def p1_descriptive_summary(df: pd.DataFrame, confidence_level: float = CONFIDENCE_LEVEL) -> pd.DataFrame:
    """Summarize estimated weighted average and high-performance share by weekly-hours band."""
    data = df.dropna(subset=["horas_semanais_grupo", "media_ponderada_num", "alto_rendimento"])
    rows = []
    for band in HOURS_ORDER:
        group = data.loc[data["horas_semanais_grupo"].astype(str) == band]
        if group.empty:
            continue
        mean, lower, upper = _mean_confidence_interval(group["media_ponderada_num"], confidence_level)
        high_count = int(group["alto_rendimento"].sum())
        rows.append({
            "Faixa de dedicação": band,
            "n": len(group),
            "Média ponderada estimada": mean,
            "IC 95% inf": lower,
            "IC 95% sup": upper,
            "Alto rendimento (n)": high_count,
            "Alto rendimento (%)": 100 * high_count / len(group),
        })
    return pd.DataFrame(rows).set_index("Faixa de dedicação").round(2)


def chi_square_hours_high_yield(
    df: pd.DataFrame, alpha: float = ALPHA
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Test independence, merging adjacent dedication bands until expected counts are adequate."""
    data = df[["horas_semanais_grupo", "alto_rendimento"]].dropna().copy()
    observed = pd.crosstab(data["horas_semanais_grupo"], data["alto_rendimento"])
    observed = observed.reindex(HOURS_ORDER, fill_value=0)
    observed = observed.reindex(columns=[False, True], fill_value=0)
    expected = stats.chi2_contingency(observed, correction=False).expected_freq
    merged_bands = []

    if (expected < 5).any():
        hours = data["horas_semanais_grupo"].astype(str).replace({
            "1 a 5h": "Até 10h",
            "6 a 10h": "Até 10h",
        })
        merged_bands.append("1 a 5h + 6 a 10h → Até 10h")
        observed = pd.crosstab(hours, data["alto_rendimento"]).reindex(
            ["Até 10h", "11 a 20h", "21 a 40h", "Mais de 40h"], fill_value=0
        )
        observed = observed.reindex(columns=[False, True], fill_value=0)
        expected = stats.chi2_contingency(observed, correction=False).expected_freq

    if (expected < 5).any():
        hours = data["horas_semanais_grupo"].astype(str).replace({
            "1 a 5h": "Até 10h",
            "6 a 10h": "Até 10h",
            "21 a 40h": "Mais de 20h",
            "Mais de 40h": "Mais de 20h",
        })
        merged_bands.append("21 a 40h + Mais de 40h → Mais de 20h")
        observed = pd.crosstab(hours, data["alto_rendimento"]).reindex(
            ["Até 10h", "11 a 20h", "Mais de 20h"], fill_value=0
        )
        observed = observed.reindex(columns=[False, True], fill_value=0)
        expected = stats.chi2_contingency(observed, correction=False).expected_freq

    if (expected < 5).any():
        raise ValueError("Não foi possível obter frequências esperadas de pelo menos 5.")

    test = stats.chi2_contingency(observed, correction=False)
    expected = test.expected_freq
    result = pd.Series({
        "N": int(observed.to_numpy().sum()),
        "χ²": test.statistic,
        "gl": test.dof,
        "p-valor": test.pvalue,
        "Menor frequência esperada": float(expected.min()),
        "Faixas agregadas": "; ".join(merged_bands) if merged_bands else "Não",
        "Decisão (α = 5%)": "Rejeita H₀" if test.pvalue < alpha else "Não rejeita H₀",
    }, name="Qui-quadrado: dedicação × alto rendimento").to_frame()
    return observed.rename(columns={False: "< 8,0", True: "≥ 8,0"}), result


def p2_external_restrictions_summary(
    df: pd.DataFrame, confidence_level: float = CONFIDENCE_LEVEL
) -> pd.DataFrame:
    """Summarize weekly hours with t confidence intervals across the three external constraints."""
    data = df.copy()
    data["atividade_remunerada_grupo"] = np.where(
        data["faz_atividade_remunerada"].astype(str) == "Não",
        PAID_ACTIVITY_ORDER[0],
        PAID_ACTIVITY_ORDER[1],
    )
    groupings = [
        ("Tempo de deslocamento", "tempo_deslocamento", None),
        ("Atividade remunerada", "atividade_remunerada_grupo", PAID_ACTIVITY_ORDER),
        ("Atividades secundárias", "qtd_outras_atividades", None),
    ]
    rows = []
    for label, group_column, order in groupings:
        summary = data.groupby(group_column, observed=True)["horas_semanais_grupo_num"].agg(["count", "mean"])
        levels = order if order is not None else summary.index.tolist()
        if group_column == "tempo_deslocamento" and isinstance(data[group_column].dtype, pd.CategoricalDtype):
            levels = [level for level in data[group_column].cat.categories if level in summary.index]
        for level in levels:
            if level not in summary.index:
                continue
            values = data.loc[data[group_column] == level, "horas_semanais_grupo_num"].dropna()
            mean, lower, upper = _mean_confidence_interval(values, confidence_level)
            rows.append({
                "Restrição": label,
                "Nível": level,
                "n": len(values),
                "Média de horas/semana": mean,
                "IC 95% inf": lower,
                "IC 95% sup": upper,
            })
    return pd.DataFrame(rows).set_index(["Restrição", "Nível"]).round(2)


def paid_activity_levene_test(df: pd.DataFrame, alpha: float = ALPHA) -> pd.DataFrame:
    """Levene test for weekly-hour variance between students with and without paid activity."""
    data = df[["faz_atividade_remunerada", "horas_semanais_grupo_num"]].dropna().copy()
    employed = data.loc[data["faz_atividade_remunerada"].astype(str) != "Não", "horas_semanais_grupo_num"]
    not_employed = data.loc[data["faz_atividade_remunerada"].astype(str) == "Não", "horas_semanais_grupo_num"]
    test = stats.levene(not_employed, employed, center="median")
    return pd.Series({
        "Estatística": test.statistic,
        "p-valor": test.pvalue,
        "Variâncias iguais?": "Não rejeita H₀" if test.pvalue >= alpha else "Rejeita H₀",
    }, name="Levene (Não vs. com atividade remunerada)").to_frame()


def paid_activity_t_test(
    df: pd.DataFrame, equal_var: bool, alpha: float = ALPHA
) -> pd.DataFrame:
    """Two-sample t test comparing students with and without paid activity."""
    data = df[["faz_atividade_remunerada", "horas_semanais_grupo_num"]].dropna()
    paid = data.loc[data["faz_atividade_remunerada"].astype(str) != "Não", "horas_semanais_grupo_num"]
    unpaid = data.loc[data["faz_atividade_remunerada"].astype(str) == "Não", "horas_semanais_grupo_num"]
    test = stats.ttest_ind(unpaid, paid, equal_var=equal_var)
    return pd.Series({
        "Média sem atividade remunerada": unpaid.mean(),
        "Média com atividade remunerada": paid.mean(),
        "Diferença de médias (não − sim)": unpaid.mean() - paid.mean(),
        "Estatística t": test.statistic,
        "gl": len(unpaid) + len(paid) - (2 if equal_var else 0),
        "p-valor": test.pvalue,
        "Variâncias consideradas iguais?": "Sim" if equal_var else "Não (Welch)",
        "Decisão (α = 5%)": "Rejeita H₀" if test.pvalue < alpha else "Não rejeita H₀",
    }, name="Teste t: atividade remunerada").to_frame()


def run_commute_anova(df: pd.DataFrame, alpha: float = ALPHA) -> dict[str, pd.DataFrame]:
    """Run Bartlett before one-way ANOVA; calculate Scheffé contrasts only if ANOVA is significant."""
    data = df[["tempo_deslocamento", "horas_semanais_grupo_num"]].dropna()
    groups = [
        values.to_numpy(dtype=float)
        for _, values in data.groupby("tempo_deslocamento", observed=True)["horas_semanais_grupo_num"]
    ]
    bartlett = stats.bartlett(*groups)
    bartlett_result = pd.Series({
        "χ²": bartlett.statistic,
        "p-valor": bartlett.pvalue,
        "Decisão (α = 5%)": "Rejeita H₀" if bartlett.pvalue < alpha else "Não rejeita H₀",
    }, name="Bartlett: tempo de deslocamento").to_frame()

    model = smf.ols("horas_semanais_grupo_num ~ C(tempo_deslocamento)", data=data).fit()
    anova_result = pd.Series({
        "F": model.fvalue,
        "gl (fator; resíduo)": f"{int(model.df_model)}; {int(model.df_resid)}",
        "p-valor": model.f_pvalue,
        "η²": model.rsquared,
        "Decisão (α = 5%)": "Rejeita H₀" if model.f_pvalue < alpha else "Não rejeita H₀",
    }, name="ANOVA: horas por tempo de deslocamento").to_frame()
    scheffe_result = _scheffe_pairwise(data, model, alpha) if model.f_pvalue <= alpha else pd.DataFrame({
        "Resultado": ["Não realizado: ANOVA não significativa."]
    }, index=pd.Index(["Scheffé"], name="Contraste"))
    return {"bartlett": bartlett_result, "anova": anova_result, "scheffe": scheffe_result}


def _scheffe_pairwise(data: pd.DataFrame, model, alpha: float) -> pd.DataFrame:
    """Compute pairwise Scheffé contrasts from a significant one-way ANOVA."""
    group = "tempo_deslocamento"
    response = "horas_semanais_grupo_num"
    summary = data.groupby(group, observed=True)[response].agg(["mean", "size"])
    group_count = len(summary)
    residual_df = int(model.df_resid)
    mse = model.ssr / model.df_resid
    critical = np.sqrt((group_count - 1) * stats.f.ppf(1 - alpha, group_count - 1, residual_df))
    rows = []
    levels = summary.index.tolist()
    for i, first in enumerate(levels):
        for second in levels[i + 1:]:
            estimate = summary.loc[first, "mean"] - summary.loc[second, "mean"]
            standard_error = np.sqrt(mse * (1 / summary.loc[first, "size"] + 1 / summary.loc[second, "size"]))
            f_statistic = estimate**2 / ((group_count - 1) * standard_error**2)
            p_value = stats.f.sf(f_statistic, group_count - 1, residual_df)
            rows.append({
                "Contraste": f"{first} − {second}",
                "Diferença média": estimate,
                "IC 95% Scheffé inf": estimate - critical * standard_error,
                "IC 95% Scheffé sup": estimate + critical * standard_error,
                "p-valor": p_value,
                "Decisão (α = 5%)": "Rejeita H₀" if p_value < alpha else "Não rejeita H₀",
            })
    return pd.DataFrame(rows).set_index("Contraste").round(3)


def secondary_activities_pearson_regression(
    df: pd.DataFrame, alpha: float = ALPHA
) -> pd.DataFrame:
    """Pearson correlation and simple OLS regression of weekly hours on secondary-activity count."""
    data = df[["qtd_outras_atividades", "horas_semanais_grupo_num"]].dropna()
    correlation = stats.pearsonr(data["qtd_outras_atividades"], data["horas_semanais_grupo_num"])
    model = smf.ols("horas_semanais_grupo_num ~ qtd_outras_atividades", data=data).fit()
    return pd.Series({
        "n": int(model.nobs),
        "r de Pearson": correlation.statistic,
        "p-valor (Pearson)": correlation.pvalue,
        "β₁ (horas por atividade adicional)": model.params["qtd_outras_atividades"],
        "p-valor (β₁)": model.pvalues["qtd_outras_atividades"],
        "R²": model.rsquared,
        "Decisão (α = 5%)": "Rejeita H₀" if correlation.pvalue < alpha else "Não rejeita H₀",
    }, name="Atividades secundárias × horas semanais").to_frame().round(4)