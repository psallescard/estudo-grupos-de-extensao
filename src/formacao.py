"""Front 1 (Formação: extensão vs. Poli): data preparation, constants and scenario builders.

Analytical decisions taken here (documented in the notebook and in the changelog):
- 'Empreendedorismo' (n = 8) is merged into 'Consultoria & Negócios' in `categoria_grupo`, because of thematic
  affinity and because with 4 categories 30% of the expected counts of the chi-square test fall below 5.
- `preparo_ext_maximo` flags the top score (5) of `preparo_extensao`, which has a strong ceiling effect.
- `log_horas_semanais` is the natural log of `horas_semanais_grupo_num`, used in the regression because the
  relationship between hours and the outcome flattens out for large values.
"""

import numpy as np
import pandas as pd

CATEGORY_ORDER = ["Consultoria & Negócios", "Engenharia", "Mercado Financeiro"]
AREA_ORDER = ["Civil & Ambiental", "Elétrica & Computação", "Mecânica, Mecatrônica & Naval", "Produção",
              "Outras Engenharias"]
GOAL_ORDER = ["Grupo de extensão", "Estágio", "Desempenho acadêmico", "Intercâmbio", "Iniciação científica"]
HOURS_ORDER = ["1 a 5h", "6 a 10h", "11 a 20h", "21 a 40h", "Mais de 40h"]
TIME_ORDER = ["Menos de 6 meses", "6 meses a 1 ano", "1 a 2 anos", "Mais de 2 anos"]

MAIN_SCALES = {
    "preparo_extensao": "Preparo profissional na extensão (1–5)",
    "preparo_disciplinas": "Preparo profissional nas disciplinas (1–5)",
    "delta_preparo": "Ganho líquido (extensão − disciplinas; de −4 a 4)",
    "importancia_media": "Importância da média ponderada (1–5)",
}


def prepare_front_data(df: pd.DataFrame) -> pd.DataFrame:
    """Adds the derived columns used in front 1 and fixes the category orders."""
    out = df.copy()
    out["categoria_grupo"] = pd.Categorical(
        out["categoria_extensao"].astype(str).replace({"Empreendedorismo": "Consultoria & Negócios"}),
        categories=CATEGORY_ORDER,
    )
    out["grande_area_curso"] = pd.Categorical(out["grande_area_curso"].astype(str), categories=AREA_ORDER)
    # "IC / Pesquisa" is renamed so that "IC" only ever means "intervalo de confiança" in the text
    goals = out["objetivo_faculdade"].astype(object).replace({"IC / Pesquisa": "Iniciação científica"})
    out["objetivo_faculdade"] = pd.Categorical(goals, categories=GOAL_ORDER)
    out["horas_semanais_grupo"] = pd.Categorical(out["horas_semanais_grupo"].astype(str), categories=HOURS_ORDER, ordered=True)
    out["tempo_grupo"] = pd.Categorical(out["tempo_grupo"].astype(str), categories=TIME_ORDER, ordered=True)
    out["preparo_ext_maximo"] = np.where(out["preparo_extensao"] == 5, "Nota 5", "Nota 3 ou 4")
    out["log_horas_semanais"] = np.log(out["horas_semanais_grupo_num"])

    if (out["delta_preparo"] != out["preparo_extensao"] - out["preparo_disciplinas"]).any():
        raise ValueError("delta_preparo is inconsistent with its two components")
    return out


def check_data_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Missing values in the front variables."""
    cols = ["preparo_extensao", "preparo_disciplinas", "delta_preparo", "importancia_media", "categoria_extensao",
            "grande_area_curso", "horas_semanais_grupo", "tempo_grupo", "objetivo_faculdade", "tempo_deslocamento_num"]
    return df[cols].isna().sum().rename("Valores ausentes").to_frame()


def hours_band_values(df: pd.DataFrame) -> pd.Series:
    """Representative hours of each band (the values of horas_semanais_grupo_num from the preprocessing)."""
    return df.groupby("horas_semanais_grupo", observed=True)["horas_semanais_grupo_num"].first()


def build_scenarios(df: pd.DataFrame, hours_bands=("6 a 10h", "21 a 40h"), extra: dict | None = None) -> pd.DataFrame:
    """A-priori profiles for the regression: every group category combined with the chosen hour bands."""
    hours = hours_band_values(df)
    rows = []
    for category in CATEGORY_ORDER:
        for band in hours_bands:
            row = {"Cenário": f"{category}, {band}", "categoria_grupo": category,
                   "log_horas_semanais": np.log(hours[band]), "horas_semanais_grupo_num": hours[band]}
            if extra:
                row.update(extra)
            rows.append(row)
    scenarios = pd.DataFrame(rows)
    scenarios["categoria_grupo"] = pd.Categorical(scenarios["categoria_grupo"], categories=CATEGORY_ORDER)
    return scenarios


# Candidate predictors of the explanatory regression (readable name -> formula term), chosen a priori
REGRESSION_BLOCKS = {
    "Categoria do grupo": "C(categoria_grupo)",
    "Grande área do curso": "C(grande_area_curso)",
    "Horas semanais (log)": "log_horas_semanais",
    "Tempo no grupo": "C(tempo_grupo)",
    "Tempo de deslocamento (min)": "tempo_deslocamento_num",
}

REGRESSION_LABELS = {
    "Intercept": "Intercepto (Consultoria & Negócios com 1 h/semana; fora dos dados, só ancora a reta)",
    "C(categoria_grupo)[T.Engenharia]": "Engenharia (vs. Consultoria & Negócios)",
    "C(categoria_grupo)[T.Mercado Financeiro]": "Mercado Financeiro (vs. Consultoria & Negócios)",
    "log_horas_semanais": "ln(horas semanais)",
}

DECOMPOSITION = {
    "delta_preparo": "Ganho líquido",
    "preparo_disciplinas": "Preparo nas disciplinas",
    "preparo_extensao": "Preparo na extensão",
}

# Scheffé contrasts for P6: every goal of the high-importance block against every goal of the low block,
# the two within-block comparisons, and one summary contrast (block means)
_HIGH = ["Desempenho acadêmico", "Intercâmbio", "Iniciação científica"]
_LOW = ["Grupo de extensão", "Estágio"]
GOAL_CONTRASTS = {
    **{f"{a} − {b}": {a: 1, b: -1} for a in _HIGH for b in _LOW},
    "Grupo de extensão − Estágio": {"Grupo de extensão": 1, "Estágio": -1},
    "Intercâmbio − Desempenho acadêmico": {"Intercâmbio": 1, "Desempenho acadêmico": -1},
    "Iniciação científica − Desempenho acadêmico": {"Iniciação científica": 1, "Desempenho acadêmico": -1},
    "Intercâmbio − Iniciação científica": {"Intercâmbio": 1, "Iniciação científica": -1},
    "Média simples de {Intercâmbio, Iniciação científica, Desempenho} − de {Grupo, Estágio}": {
        **{a: 1 / 3 for a in _HIGH}, **{b: -1 / 2 for b in _LOW}},
}

FACTOR_LABELS = {
    "categoria_grupo": "Categoria do grupo",
    "grande_area_curso": "Grande área do curso",
    "horas_semanais_grupo": "Horas semanais no grupo",
    "tempo_grupo": "Tempo no grupo",
    "objetivo_faculdade": "Objetivo atual",
}


def group_composition(df: pd.DataFrame) -> pd.DataFrame:
    """Which extension groups make up each category (after merging Empreendedorismo)."""
    table = df.groupby(["categoria_grupo", "grupo_extensao"], observed=True).size().rename("n").reset_index()
    return table.rename(columns={"categoria_grupo": "Categoria do grupo", "grupo_extensao": "Grupo de extensão"}).set_index(
        ["Categoria do grupo", "Grupo de extensão"])


def other_engineering_courses(df: pd.DataFrame) -> pd.Series:
    """Courses grouped as 'Outras Engenharias'."""
    courses = df.loc[df["grande_area_curso"] == "Outras Engenharias", "curso"].astype(str).value_counts()
    return courses.rename("n").rename_axis("Cursos em 'Outras Engenharias'")


def hours_band_table(df: pd.DataFrame) -> pd.DataFrame:
    """Representative hours of each band and the mean net gain observed in it."""
    table = df.groupby("horas_semanais_grupo", observed=True).agg(
        horas_representativas=("horas_semanais_grupo_num", "first"),
        ln_horas=("log_horas_semanais", "first"),
        ganho_medio_observado=("delta_preparo", "mean"),
        n=("delta_preparo", "size"),
    ).round(2)
    return table.rename_axis("Faixa de horas").rename(columns={
        "horas_representativas": "Horas representativas (h/semana)", "ln_horas": "ln(horas)",
        "ganho_medio_observado": "Ganho líquido médio observado", "n": "n"})


def hours_share_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Distribution of weekly-hours bands within each group category (row percentages)."""
    table = pd.crosstab(df["categoria_grupo"], df["horas_semanais_grupo"], normalize="index") * 100
    return table.round(0).rename_axis(index="Categoria do grupo", columns="Horas semanais (% da categoria)")
