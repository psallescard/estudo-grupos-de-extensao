"""Multiple linear regression helpers in the style of the PRO3201 syllabus: OLS, partial F test,
backward elimination by partial F, coefficient tables and scenario predictions (confidence and prediction
intervals). Tables come back with PT-BR headers."""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from src.stats_tests import format_p

ALPHA = 0.05


def _formula(response: str, terms: list) -> str:
    return f"{response} ~ " + (" + ".join(terms) if terms else "1")


def fit_ols(df: pd.DataFrame, response: str, terms):
    """Ordinary least squares with the given formula terms (a list, or a dict whose values are the terms)."""
    terms = list(terms.values()) if isinstance(terms, dict) else list(terms)
    return smf.ols(_formula(response, terms), df).fit()


def model_summary(model) -> pd.DataFrame:
    """Global fit of a model: R², adjusted R², global F test and residual standard error."""
    return pd.Series({
        "n": int(model.nobs),
        "R²": round(model.rsquared, 3),
        "R² ajustado": round(model.rsquared_adj, 3),
        "F global": round(model.fvalue, 2),
        "gl (modelo; resíduo)": f"{int(model.df_model)}; {int(model.df_resid)}",
        "p-valor do F global": format_p(model.f_pvalue),
        "Erro-padrão residual": round(np.sqrt(model.mse_resid), 3),
    }, name="Ajuste do modelo").to_frame()


def backward_elimination(df: pd.DataFrame, response: str, blocks: dict, alpha: float = ALPHA):
    """Starts from the full model and, at each step, tests every block with a partial F test
    (full model vs. model without the block). The block with the largest p-value is removed if p >= alpha.
    `blocks` maps a readable name to its formula term. Returns (steps table, final model, kept block names)."""
    data = df.dropna(subset=[response]).copy()
    kept = dict(blocks)
    steps = []
    step = 1
    while kept:
        full = fit_ols(data, response, list(kept.values()))
        tests = {}
        for name, term in kept.items():
            reduced = fit_ols(data, response, [t for n, t in kept.items() if n != name])
            f_value, p_value, df_diff = full.compare_f_test(reduced)
            tests[name] = (f_value, p_value, int(df_diff))
        worst = max(tests, key=lambda name: tests[name][1])
        f_value, p_value, df_diff = tests[worst]
        removed = p_value >= alpha
        steps.append({
            "Passo": step,
            "Nº de variáveis no modelo": len(kept),
            "Variável com maior p": worst,
            "F parcial": round(f_value, 2),
            "gl": f"{df_diff}; {int(full.df_resid)}",
            "p parcial": format_p(p_value),
            "Decisão": "Remover (p ≥ 0,05)" if removed else "Manter todas (p < 0,05)",
            "R² ajustado": round(full.rsquared_adj, 3),
        })
        if not removed:
            break
        kept.pop(worst)
        step += 1
    final = fit_ols(data, response, list(kept.values()))
    return pd.DataFrame(steps).set_index("Passo"), final, list(kept)


def joint_partial_f_test(full, reduced, name: str = "Modelo completo vs. modelo final") -> pd.DataFrame:
    """Partial F test between two nested models (H0: the removed coefficients are all zero)."""
    f_value, p_value, df_diff = full.compare_f_test(reduced)
    return pd.Series({
        "F parcial": round(f_value, 2),
        "gl": f"{int(df_diff)}; {int(full.df_resid)}",
        "p-valor": format_p(p_value),
        "Decisão (α = 5%)": "Rejeita H0" if p_value < ALPHA else "Não rejeita H0 (modelo reduzido é suficiente)",
    }, name=name).to_frame()


def coefficient_table(model, labels: dict | None = None) -> pd.DataFrame:
    """β estimates with standard error, t test and 95% confidence interval."""
    ci = model.conf_int()
    table = pd.DataFrame({
        "β (estimativa)": model.params.round(3),
        "Erro-padrão": model.bse.round(3),
        "t": model.tvalues.round(2),
        "p-valor": model.pvalues.map(format_p),
        "IC 95% inf": ci[0].round(3),
        "IC 95% sup": ci[1].round(3),
    })
    if labels:
        table.index = [labels.get(name, name) for name in table.index]
    return table


def predict_scenarios(model, scenarios: pd.DataFrame, label_col: str = "Cenário") -> pd.DataFrame:
    """Predicted mean response for each scenario, with the 95% confidence interval of the mean
    (where the average student of that profile lies) and the 95% prediction interval (where an individual lies)."""
    pred = model.get_prediction(scenarios).summary_frame(alpha=ALPHA)
    out = scenarios[[label_col]].copy() if label_col in scenarios else pd.DataFrame(index=scenarios.index)
    out["Valor estimado (média do perfil)"] = pred["mean"].to_numpy()
    out["IC 95% da média"] = [f"[{lo:.2f}; {hi:.2f}]" for lo, hi in zip(pred["mean_ci_lower"], pred["mean_ci_upper"])]
    out["IP 95% individual"] = [f"[{lo:.2f}; {hi:.2f}]" for lo, hi in zip(pred["obs_ci_lower"], pred["obs_ci_upper"])]
    return out.set_index(label_col).round(2) if label_col in out else out.round(2)


def coefficients_by_response(df: pd.DataFrame, responses: dict, terms, labels: dict | None = None) -> pd.DataFrame:
    """Fits the same right-hand side to several responses (`responses` maps column -> label) and puts the
    β and p-values side by side. Used to split the net gain into its two components."""
    columns = {}
    for col, label in responses.items():
        model = fit_ols(df, col, terms)
        columns[(label, "β")] = model.params.round(3)
        columns[(label, "p-valor")] = model.pvalues.map(format_p)
    table = pd.DataFrame(columns)
    if labels:
        table.index = [labels.get(name, name) for name in table.index]
    return table
