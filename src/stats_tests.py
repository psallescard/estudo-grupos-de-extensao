"""Hypothesis tests from the PRO3201 syllabus, returning tables ready to display (headers in PT-BR).

Covered: descriptive summaries, paired t-test, chi-square test of association, one- and two-way ANOVA
(partial F tests), Bartlett's test of homogeneity of variances and Scheffé contrasts.
"""

from itertools import combinations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

ALPHA = 0.05


def format_p(p_value):
    """p-values below 0.001 in scientific notation, the others with 4 decimals."""
    return f"{p_value:.1e}" if p_value < 0.001 else f"{p_value:.4f}"


def _decision(p_value, alpha=ALPHA):
    return "Rejeita H0" if p_value < alpha else "Não rejeita H0"


def _q(name: str) -> str:
    """Quotes a column name for statsmodels formulas."""
    return f'Q("{name}")'


# ---------------------------------------------------------------------------
# Descriptive statistics
# ---------------------------------------------------------------------------
def describe_scales(df: pd.DataFrame, columns: dict) -> pd.DataFrame:
    """n, mean, standard deviation, quartiles and share of top scores for 1-5 scales. `columns` maps column -> label.
    The '% nota 5' column is left empty for variables that are not 1-5 scales (e.g. the net gain)."""
    rows = []
    for col, label in columns.items():
        s = df[col].dropna()
        is_scale = s.min() >= 1 and s.max() <= 5
        rows.append({
            "Variável": label, "n": len(s), "Média": s.mean(), "Desvio-padrão": s.std(), "Mínimo": s.min(),
            "1º quartil": s.quantile(0.25), "Mediana": s.median(), "3º quartil": s.quantile(0.75), "Máximo": s.max(),
            "% nota 5": (s == 5).mean() * 100 if is_scale else np.nan,
        })
    return pd.DataFrame(rows).set_index("Variável").round(2)


def group_means(df: pd.DataFrame, value: str, group: str, group_label: str | None = None) -> pd.DataFrame:
    """Mean of `value` per group with a 95% t confidence interval."""
    rows = []
    for level, sub in df[[value, group]].dropna().groupby(group, observed=True):
        v = sub[value].to_numpy(dtype=float)
        half = stats.t.ppf(0.975, v.size - 1) * v.std(ddof=1) / np.sqrt(v.size) if v.size > 1 else np.nan
        rows.append({group: level, "n": v.size, "Média": v.mean(), "Desvio-padrão": v.std(ddof=1),
                     "IC 95% inf": v.mean() - half, "IC 95% sup": v.mean() + half})
    return pd.DataFrame(rows).set_index(group).rename_axis(group_label or group).round(2)


def group_means_for_outcomes(df: pd.DataFrame, outcomes: dict, group: str, group_label: str | None = None) -> pd.DataFrame:
    """Mean (and t confidence interval) of several outcomes per group, side by side (`outcomes` maps column -> label)."""
    table = pd.concat({label: group_means(df, col, group, group_label)[["Média", "IC 95% inf", "IC 95% sup"]]
                       for col, label in outcomes.items()}, axis=1)
    table.insert(0, ("", "n"), group_means(df, next(iter(outcomes)), group, group_label)["n"])
    return table


# ---------------------------------------------------------------------------
# Paired t-test
# ---------------------------------------------------------------------------
def paired_t_test(df: pd.DataFrame, col_a: str, col_b: str, alternative: str = "greater") -> pd.DataFrame:
    """Paired t-test for the mean of d = col_a - col_b (H0: mu_d = 0)."""
    data = df[[col_a, col_b]].dropna()
    d = (data[col_a] - data[col_b]).to_numpy(dtype=float)
    n = d.size
    res = stats.ttest_rel(data[col_a], data[col_b], alternative=alternative)
    se = d.std(ddof=1) / np.sqrt(n)
    t_crit = stats.t.ppf(0.975, n - 1)
    rows = {
        "n (pares)": n,
        "Média de d": round(d.mean(), 3),
        "Desvio-padrão de d": round(d.std(ddof=1), 3),
        "IC 95% da média de d": f"[{d.mean() - t_crit * se:.2f}; {d.mean() + t_crit * se:.2f}]",
        "Estatística t": round(res.statistic, 2),
        "Graus de liberdade": n - 1,
        "p-valor": format_p(res.pvalue),
        "Tamanho de efeito (d de Cohen = média de d / DP de d)": round(d.mean() / d.std(ddof=1), 2),
        "% com d > 0 / d = 0 / d < 0": f"{(d > 0).mean():.1%} / {(d == 0).mean():.1%} / {(d < 0).mean():.1%}",
        "Decisão (α = 5%)": _decision(res.pvalue),
    }
    return pd.Series(rows, name="Teste t pareado").to_frame()


# ---------------------------------------------------------------------------
# Chi-square test of association
# ---------------------------------------------------------------------------
def chi_square_association(df: pd.DataFrame, row: str, col: str) -> tuple:
    """Returns (observed contingency table, result table) for the chi-square test of independence."""
    observed = pd.crosstab(df[row], df[col])
    res = stats.chi2_contingency(observed, correction=False)
    n = observed.to_numpy().sum()
    k = min(observed.shape) - 1
    expected = res.expected_freq
    result = pd.Series({
        "Qui-quadrado (χ²)": round(res.statistic, 2),
        "Graus de liberdade": res.dof,
        "p-valor": format_p(res.pvalue),
        "V de Cramér (0 = nenhuma, 1 = total)": round(np.sqrt(res.statistic / (n * k)), 3),
        "Menor frequência esperada": round(expected.min(), 2),
        "% de caselas com esperado < 5": f"{(expected < 5).mean():.0%}",
        "Decisão (α = 5%)": _decision(res.pvalue),
    }, name="Teste de associação").to_frame()
    return observed, result


# ---------------------------------------------------------------------------
# ANOVA
# ---------------------------------------------------------------------------
def bartlett_test(df: pd.DataFrame, value: str, group: str) -> dict:
    """Bartlett's test (H0: equal variances across groups). Undefined when a group has zero variance."""
    samples = [sub[value].to_numpy(dtype=float) for _, sub in df[[value, group]].dropna().groupby(group, observed=True)]
    zero_var = [np.var(s) == 0 for s in samples]
    if any(zero_var):
        return {"Bartlett (χ²)": np.nan, "p Bartlett": np.nan,
                "Variâncias homogêneas?": "Não calculável: há grupo com variância zero"}
    res = stats.bartlett(*samples)
    return {"Bartlett (χ²)": round(res.statistic, 2), "p Bartlett": format_p(res.pvalue),
            "Variâncias homogêneas?": "Sim (não rejeita H0)" if res.pvalue >= ALPHA else "Não (rejeita H0)"}


def one_way_anova(df: pd.DataFrame, value: str, group: str, title: str | None = None) -> pd.DataFrame:
    """One-way ANOVA (H0: all group means are equal) with eta-squared and Bartlett's test."""
    data = df[[value, group]].dropna()
    model = smf.ols(f"{_q(value)} ~ C({_q(group)})", data).fit()
    k = data[group].nunique()
    row = {
        "F": round(model.fvalue, 2),
        "gl (fator; resíduo)": f"{k - 1}; {int(model.df_resid)}",
        "p-valor": format_p(model.f_pvalue),
        "η² (variância explicada)": round(model.rsquared, 3),
        "Decisão (α = 5%)": _decision(model.f_pvalue),
        **bartlett_test(data, value, group),
    }
    return pd.Series(row, name=title or f"ANOVA de 1 fator: {value} por {group}").to_frame()


def two_way_anova(df: pd.DataFrame, value: str, factor_a: str, factor_b: str, labels: dict | None = None) -> pd.DataFrame:
    """Additive two-way ANOVA. Each factor is tested with a partial F test: the full model (A + B) is compared
    with the model without that factor, so the test answers 'does the factor matter once the other is known?'."""
    data = df[[value, factor_a, factor_b]].dropna()
    terms = {factor_a: f"C({_q(factor_a)})", factor_b: f"C({_q(factor_b)})"}
    full = smf.ols(f"{_q(value)} ~ {terms[factor_a]} + {terms[factor_b]}", data).fit()
    rows = []
    for factor, other in [(factor_a, factor_b), (factor_b, factor_a)]:
        alone = smf.ols(f"{_q(value)} ~ {terms[factor]}", data).fit()
        reduced = smf.ols(f"{_q(value)} ~ {terms[other]}", data).fit()
        f_partial, p_partial, df_diff = full.compare_f_test(reduced)
        ss_factor = reduced.ssr - full.ssr
        rows.append({
            "Fator": factor,
            "p sozinho (ANOVA 1 fator)": format_p(alone.f_pvalue),
            "F parcial (controlando o outro fator)": round(f_partial, 2),
            "gl": f"{int(df_diff)}; {int(full.df_resid)}",
            "p parcial": format_p(p_partial),
            "η² parcial": round(ss_factor / (ss_factor + full.ssr), 3),
            "Decisão (α = 5%)": _decision(p_partial),
        })
    table = pd.DataFrame(rows).set_index("Fator")
    return table.rename(index=labels) if labels else table


def scheffe_contrasts(df: pd.DataFrame, value: str, group: str, contrasts: dict | None = None) -> pd.DataFrame:
    """Scheffé tests for contrasts L = sum(c_i * mean_i), with sum(c_i) = 0, on the one-way ANOVA of `value` by `group`
    (i.e. on the raw group means, not adjusted for other factors).

    By default all pairwise differences are tested. `contrasts` maps a label to {group_level: weight}.
    Scheffé controls the error rate for any number of contrasts, including ones chosen after looking at the data.
    """
    data = df[[value, group]].dropna()
    summary = data.groupby(group, observed=True)[value].agg(["mean", "size"])
    k, n_total = len(summary), len(data)
    model = smf.ols(f"{_q(value)} ~ C({_q(group)})", data).fit()
    mse = model.ssr / model.df_resid
    f_crit = stats.f.ppf(1 - ALPHA, k - 1, n_total - k)
    s_crit = np.sqrt((k - 1) * f_crit)

    if contrasts is None:
        contrasts = {f"{a} − {b}": {a: 1, b: -1} for a, b in combinations(summary.index, 2)}
    rows = []
    for label, weights in contrasts.items():
        c = np.array([weights.get(level, 0) for level in summary.index], dtype=float)
        if not np.isclose(c.sum(), 0):
            raise ValueError(f"Contrast '{label}' weights must sum to zero")
        estimate = float(np.sum(c * summary["mean"]))
        se = float(np.sqrt(mse * np.sum(c**2 / summary["size"])))
        f_stat = estimate**2 / (se**2 * (k - 1))
        p = stats.f.sf(f_stat, k - 1, n_total - k)
        rows.append({
            "Contraste": label, "Estimativa (diferença)": round(estimate, 2),
            "IC 95% de Scheffé": f"[{estimate - s_crit * se:.2f}; {estimate + s_crit * se:.2f}]",
            "p de Scheffé": format_p(p), "Significativo?": "Sim" if p < ALPHA else "Não",
        })
    return pd.DataFrame(rows).set_index("Contraste")


# ---------------------------------------------------------------------------
# Convenience wrappers that stack several tests in one table
# ---------------------------------------------------------------------------
def two_way_anova_for_outcomes(df: pd.DataFrame, outcomes: dict, factor_a: str, factor_b: str,
                               labels: dict | None = None) -> pd.DataFrame:
    """Runs `two_way_anova` for each outcome (`outcomes` maps column -> label) and stacks the results."""
    return pd.concat({label: two_way_anova(df, col, factor_a, factor_b, labels) for col, label in outcomes.items()},
                     names=["Variável resposta", "Fator"])


def bartlett_table(df: pd.DataFrame, value: str, groups: dict) -> pd.DataFrame:
    """Bartlett's test of `value` across the levels of each grouping variable (`groups` maps column -> label)."""
    return pd.DataFrame({label: bartlett_test(df, value, col) for col, label in groups.items()}).T.rename_axis(
        "Grupos comparados")


def chi_square_table(df: pd.DataFrame, variables: dict, outcome: str) -> pd.DataFrame:
    """Chi-square test of association between `outcome` and each variable (`variables` maps column -> label)."""
    return pd.concat({label: chi_square_association(df, col, outcome)[1].iloc[:, 0] for col, label in variables.items()},
                     axis=1).T.rename_axis("Variável testada")


def scheffe_for_outcomes(df: pd.DataFrame, outcomes: dict, group: str) -> pd.DataFrame:
    """Pairwise Scheffé contrasts of `group` for each outcome (`outcomes` maps column -> label), stacked."""
    return pd.concat({label: scheffe_contrasts(df, col, group) for col, label in outcomes.items()},
                     names=["Variável resposta", "Contraste"])
