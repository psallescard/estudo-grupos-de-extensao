"""Front 3 (Carreira: trajetória & objetivos): data preparation, constants and scenario builder.

Analytical decisions (documented in the notebook, in the spec and in the changelog). Every merge is listed in
GROUPINGS, which is also exported as a table in the notebook:
- 'Empreendedorismo' (n = 8) merged into 'Consultoria & Negócios' in `categoria_grupo`, as in front 1;
- `area_grupo`: 'Consultoria' + 'Empreendedorismo', so that at most ~20% of the chi-square expected counts fall below 5;
- `motivacao_grupo`: 'Networking' (6) + 'Indicação de amigos' (1) -> 'Outros', left out of the P2 chi-square;
- `objetivo_grupo`: 'Desempenho acadêmico' + 'IC / Pesquisa' -> 'Desempenho & Pesquisa';
- `ano_poli_grupo`: years 3 to 5 merged (only 9 students in years 4-5);
- `estagio_ate_3ano`: binary intention to start the first internship up to the 3rd year ('Não pretendo' -> missing);
- `faixa_media`: 3 bands of the weighted average, for the ordinal check of P6.
"""

import numpy as np
import pandas as pd

EXPECTED_N = 187
SURVEY_YEAR = 2026

CATEGORY_ORDER = ["Consultoria & Negócios", "Engenharia", "Mercado Financeiro"]
AREA_ORDER = ["Civil & Ambiental", "Elétrica & Computação", "Mecânica, Mecatrônica & Naval", "Produção",
              "Outras Engenharias"]
CAREER_ORDER = ["Mercado Financeiro", "Consultoria", "Empreendedorismo", "Indústria/Engenharia", "Tecnologia",
                "Indefinido"]
CAREER_GROUP_ORDER = ["Mercado Financeiro", "Consultoria & Empreendedorismo", "Indústria/Engenharia", "Tecnologia",
                      "Indefinido"]
MOTIVATION_GROUP_ORDER = ["Adquirir experiência prática em projetos reais", "Aprendizado técnico (hardskills)",
                          "Desenvolvimento pessoal, comunicação e liderança (softskills)",
                          "Interesse pela temática e objetivos do grupo", "Outros"]
GOAL_GROUP_ORDER = ["Grupo de extensão", "Estágio", "Desempenho & Pesquisa", "Intercâmbio"]
YEAR_GROUP_ORDER = ["1º ano", "2º ano", "3º ano ou mais"]
INTERNSHIP_ORDER = ["Até o 3º ano", "4º ano ou depois"]
GRADE_BAND_ORDER = ["Abaixo de 7,0", "7,0 a 7,9", "8,0 ou mais"]
TIME_ORDER = ["Menos de 6 meses", "6 meses a 1 ano", "1 a 2 anos", "Mais de 2 anos"]

MAIN_VARIABLES = {
    "area_pretendida": "Área pretendida após a formatura",
    "estagio_antecipado": "Quando pretende fazer o 1º estágio",
    "objetivo_faculdade": "Objetivo principal atual na faculdade",
    "motivacao_grupo": "Motivação para entrar no grupo",
    "categoria_grupo": "Categoria do grupo de extensão",
    "ano_poli_grupo": "Ano na Poli",
}

# (source column, original levels, new category, reason): the single source of truth for every merge
GROUPINGS = [
    ("categoria_extensao", ["Consultoria & Negócios", "Empreendedorismo"], "Consultoria & Negócios",
     "Empreendedorismo tem n = 8; mesma decisão da Frente 1"),
    ("area_pretendida", ["Consultoria", "Empreendedorismo"], "Consultoria & Empreendedorismo",
     "Com 6 áreas, 28% das caselas da P1a ficam com esperado < 5; com 5 áreas, 20%"),
    ("motivacao_ingresso", ["Networking e contato com empresas", "Indicação ou influência de amigos"], "Outros",
     "n = 7; aparece na descritiva, mas fica fora do qui-quadrado da P2"),
    ("objetivo_faculdade", ["Desempenho acadêmico", "IC / Pesquisa"], "Desempenho & Pesquisa",
     "IC / Pesquisa tem n = 6; com 5 objetivos, 33% das caselas da P4 ficam com esperado < 5; com 4, 8%"),
    ("anos_de_poli", ["3", "4", "5"], "3º ano ou mais", "Só 9 alunos estão no 4º ou 5º ano"),
    ("momento_estagio", ["Antes do 3º ano", "No 3ºano"], "Até o 3º ano",
     "Corte da P3 e da P7; mede intenção, pois a maioria ainda não chegou ao 3º ano"),
    ("momento_estagio", ["No 4ºano", "A partir do 5ºano"], "4º ano ou depois", "Idem"),
    ("momento_estagio", ["Não pretendo realizar estágio"], "Excluído (sem valor)", "n = 1"),
    ("media_ponderada", ["Menor que 5.0", "5.0 a 5.9", "6.0 a 6.9"], "Abaixo de 7,0",
     "Checagem ordinal da P6: as faixas das pontas têm poucos alunos"),
    ("media_ponderada", ["8.0 a 8.9", "9.0 a 10.0"], "8,0 ou mais", "Idem"),
]


def _merge_map(source: str) -> dict:
    return {level: new for col, levels, new, _ in GROUPINGS if col == source for level in levels}


def _categorical(values, order, ordered=False) -> pd.Categorical:
    return pd.Categorical(values, categories=order, ordered=ordered)


def prepare_front_data(df: pd.DataFrame) -> pd.DataFrame:
    """Adds the derived columns of front 3 and fixes the category orders. Raises if the parquet is stale."""
    out = df.copy()
    if len(out) != EXPECTED_N:
        raise ValueError(f"Expected {EXPECTED_N} rows, got {len(out)}")
    if (out["anos_de_poli"] != SURVEY_YEAR - out["ano_ingresso"].astype(int) + 1).any():
        raise ValueError("anos_de_poli is inconsistent with ano_ingresso: regenerate clean_data.parquet with notebook 00")

    out["categoria_grupo"] = _categorical(
        out["categoria_extensao"].astype(str).replace(_merge_map("categoria_extensao")), CATEGORY_ORDER)
    out["grande_area_curso"] = _categorical(out["grande_area_curso"].astype(str), AREA_ORDER)
    out["area_pretendida"] = _categorical(out["area_pretendida"].astype(str), CAREER_ORDER)
    out["area_grupo"] = _categorical(
        out["area_pretendida"].astype(str).replace(_merge_map("area_pretendida")), CAREER_GROUP_ORDER)
    out["motivacao_grupo"] = _categorical(
        out["motivacao_ingresso"].astype(str).replace(_merge_map("motivacao_ingresso")), MOTIVATION_GROUP_ORDER)
    out["objetivo_grupo"] = _categorical(
        out["objetivo_faculdade"].astype(object).replace(_merge_map("objetivo_faculdade")), GOAL_GROUP_ORDER)
    out["ano_poli_grupo"] = _categorical(
        out["anos_de_poli"].clip(upper=3).map({1: "1º ano", 2: "2º ano", 3: "3º ano ou mais"}), YEAR_GROUP_ORDER,
        ordered=True)
    out["estagio_antecipado"] = _categorical(
        out["momento_estagio"].astype(str).replace(_merge_map("momento_estagio")), INTERNSHIP_ORDER)
    out["estagio_ate_3ano"] = (out["estagio_antecipado"] == INTERNSHIP_ORDER[0]).astype(float).where(
        out["estagio_antecipado"].notna())
    out["faixa_media"] = _categorical(
        out["media_ponderada"].astype(str).replace({**_merge_map("media_ponderada"), "7.0 a 7.9": "7,0 a 7,9"}),
        GRADE_BAND_ORDER, ordered=True)
    out["tempo_grupo"] = _categorical(out["tempo_grupo"].astype(str), TIME_ORDER, ordered=True)
    out["log_horas_semanais"] = np.log(out["horas_semanais_grupo_num"])

    # every merge must map all original answers: only the documented missing values are allowed
    for col in ["categoria_grupo", "grande_area_curso", "area_pretendida", "area_grupo", "motivacao_grupo",
                "ano_poli_grupo", "tempo_grupo"]:
        if out[col].isna().any():
            raise ValueError(f"{col} has unmapped values")
    if out["objetivo_grupo"].isna().sum() != out["objetivo_faculdade"].isna().sum():
        raise ValueError("objetivo_grupo has unmapped values")
    if out["estagio_antecipado"].isna().sum() != (out["momento_estagio"] == "Não pretendo realizar estágio").sum():
        raise ValueError("estagio_antecipado has unmapped values")
    return out


def analysis_sample(df: pd.DataFrame, columns: list, exclude: dict | None = None) -> pd.DataFrame:
    """Rows with no missing value in `columns`, minus the excluded levels ({column: [levels]}). Unused categories are
    removed, so crosstabs built from the sample have no empty rows or columns."""
    out = df.dropna(subset=columns).copy()
    for col, levels in (exclude or {}).items():
        out = out[~out[col].isin(levels)].copy()
    for col in columns:
        if isinstance(out[col].dtype, pd.CategoricalDtype):
            out[col] = out[col].cat.remove_unused_categories()
    return out


def category_distribution(df: pd.DataFrame, columns: dict) -> pd.DataFrame:
    """n and % of each level (missing answers shown as 'Sem resposta'); `columns` maps column -> label."""
    parts = {}
    for col, label in columns.items():
        values = df[col]
        if isinstance(values.dtype, pd.CategoricalDtype):
            order = list(values.cat.categories)
        else:
            order = sorted(values.dropna().unique())
        if values.isna().any():
            order.append("Sem resposta")
        counts = values.astype(object).fillna("Sem resposta").value_counts().reindex(order, fill_value=0)
        parts[label] = pd.DataFrame({"n": counts, "%": (counts / len(values) * 100).round(1)})
    return pd.concat(parts, names=["Variável", "Categoria"])


def grouping_table(df: pd.DataFrame) -> pd.DataFrame:
    """Every category merge of front 3, with the number of students affected and the reason."""
    rows = [{"Variável": col, "Categorias originais": " + ".join(levels), "Nova categoria": new,
             "n": int(df[col].astype(str).isin(levels).sum()), "Motivo": reason}
            for col, levels, new, reason in GROUPINGS]
    return pd.DataFrame(rows)


# P6: contrast defined before looking at the results (hypothesis of the analysis guide)
_TARGET_CAREERS = ["Mercado Financeiro", "Consultoria"]
_OTHER_CAREERS = ["Empreendedorismo", "Indústria/Engenharia", "Tecnologia", "Indefinido"]
CAREER_CONTRASTS = {
    "Média simples de {Mercado Financeiro, Consultoria} − das demais áreas": {
        **{a: 1 / 2 for a in _TARGET_CAREERS}, **{b: -1 / 4 for b in _OTHER_CAREERS}},
}

# P7: candidate predictors of the explanatory model (readable name -> formula term), chosen a priori
REGRESSION_BLOCKS = {
    "Categoria do grupo": "C(categoria_grupo)",
    "Grande área do curso": "C(grande_area_curso)",
    "Ano na Poli": "C(ano_poli_grupo)",
    "Objetivo atual": "C(objetivo_grupo)",
    "Tempo no grupo": "C(tempo_grupo)",
    "Horas semanais (log)": "log_horas_semanais",
}
REGRESSION_COLUMNS = ["estagio_ate_3ano", "categoria_grupo", "grande_area_curso", "ano_poli_grupo", "objetivo_grupo",
                      "tempo_grupo", "log_horas_semanais"]


def _level_labels(column: str, order: list, name: str) -> dict:
    return {f"C({column})[T.{level}]": f"{name}: {level} (vs. {order[0]})" for level in order[1:]}


REGRESSION_LABELS = {
    "Intercept": "Intercepto (perfil com todas as categorias de referência)",
    "log_horas_semanais": "ln(horas semanais)",
    **_level_labels("categoria_grupo", CATEGORY_ORDER, "Categoria"),
    **_level_labels("grande_area_curso", AREA_ORDER, "Área do curso"),
    **_level_labels("ano_poli_grupo", YEAR_GROUP_ORDER, "Ano"),
    **_level_labels("objetivo_grupo", GOAL_GROUP_ORDER, "Objetivo"),
    **_level_labels("tempo_grupo", TIME_ORDER, "Tempo no grupo"),
}

SCENARIO_HOURS_BAND = "11 a 20h"


def build_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """A-priori profiles for P7: every year group x course area. The other predictors are fixed at reference values
    (Consultoria & Negócios, 'Grupo de extensão', 6 meses a 1 ano, 11 a 20h); the final model ignores the ones it
    dropped."""
    hours = df.loc[df["horas_semanais_grupo"] == SCENARIO_HOURS_BAND, "horas_semanais_grupo_num"].iloc[0]
    rows = [{"Cenário": f"{year}, {area}", "ano_poli_grupo": year, "grande_area_curso": area,
             "categoria_grupo": CATEGORY_ORDER[0], "objetivo_grupo": GOAL_GROUP_ORDER[0],
             "tempo_grupo": "6 meses a 1 ano", "log_horas_semanais": np.log(hours)}
            for year in YEAR_GROUP_ORDER for area in AREA_ORDER]
    scenarios = pd.DataFrame(rows)
    for col, order, ordered in [("ano_poli_grupo", YEAR_GROUP_ORDER, True), ("grande_area_curso", AREA_ORDER, False),
                                ("categoria_grupo", CATEGORY_ORDER, False), ("objetivo_grupo", GOAL_GROUP_ORDER, False),
                                ("tempo_grupo", TIME_ORDER, True)]:
        scenarios[col] = _categorical(scenarios[col], order, ordered)
    return scenarios
