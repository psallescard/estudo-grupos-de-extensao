# Frente 3 (Carreira): plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** produzir a análise da Frente 3 (Carreira: trajetória & objetivos) do projeto PRO3201: notebook legível, funções em `src/`, tabelas e figuras `f3_`, resumo para o relatório e changelog.

**Architecture:** repete o desenho da Frente 1. A lógica fica em `src/carreira.py` (preparação, constantes, cenários) e `src/plotting/plots_carreira.py` (gráficos). Os testes da disciplina vêm de `src/stats_tests.py`, que ganha 2 funções, e de `src/regression.py`, sem mudanças. O notebook `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb` só chama funções e explica cada método.

**Tech Stack:** Python 3.12, uv, pandas, scipy, statsmodels, matplotlib/seaborn e Jupyter. pytest e nbconvert entram via `uv run --with`, sem alterar o `pyproject.toml`.

**Spec:** `docs/superpowers/specs/2026-11-25-frente-3-carreira-design.md`. Leia a spec antes de qualquer tarefa.

## Global Constraints

- **Só métodos da disciplina:**
  - qui-quadrado de associação com V de Cramér;
  - ANOVA de 1 fator com Bartlett, η² e Scheffé;
  - regressão linear múltipla com F parcial.

  Nada de regressão logística, bootstrap, validação cruzada, Wilcoxon ou correção de Holm.
- α = 0,05. Cada pergunta é registrada nos itens (a) a (e) do guia.
- **Validade do qui-quadrado:** no máximo cerca de 20% das caselas com esperado abaixo de 5.
- **Idioma:** código, nomes e comentários em EN-US; markdown, títulos de gráficos, cabeçalhos de tabelas e changelog em PT-BR.
- **Linguagem associativa, não causal.** `momento_estagio` mede **intenção**.
- **Artefatos:**
  - `output/tables/f3_tabNN_<nome>.csv` e `output/figures/f3_figNN_<nome>.png`, numerados na ordem em que aparecem;
  - `output/f3_resumo_para_relatorio.md`.
- **Dados:** `data/clean_data.parquet`, gerado de novo em 25/11 (n = 187; `anos_de_poli` == 2026 − `ano_ingresso` + 1). Nunca editar os dados à mão.
- **Execução:** sempre a partir da raiz do repositório.
  - testes: `uv run --with pytest python -m pytest tests -q`;
  - notebook: `cd notebooks && uv run --with nbconvert jupyter nbconvert --to notebook --execute --inplace 02_Carreira_Trajetoria_Objetivos.ipynb`.
- Trabalhar na branch `frente-3-carreira`, nunca direto na `main`.

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `src/stats_tests.py` (alterar) | + `standardized_residuals`, + `row_percentages` |
| `src/carreira.py` (criar) | Ordens de categorias, tabela de agrupamentos, `prepare_front_data`, `analysis_sample`, `category_distribution`, `grouping_table`, contrastes da P6, blocos, rótulos e cenários da P7 |
| `src/plotting/plots_carreira.py` (criar) | `plot_category_distribution`, `plot_stacked_shares`, `plot_means_panels`, `plot_scenario_probabilities`; reexporta `plot_residual_diagnostics` |
| `tests/test_stats_tests.py`, `tests/test_carreira.py`, `tests/test_plots_carreira.py` (criar) | Testes unitários e de fumaça |
| `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb` (criar) | Análise |
| `output/f3_resumo_para_relatorio.md`, `.changelog/YYYYMMDD-frente-3-carreira.md` (criar) | Texto para o relatório e registro da sessão |

Não há pasta `tests/` no repositório; ela é criada na Task 1. `python -m pytest` coloca a raiz no `sys.path`, então `from src... import` funciona sem `conftest.py`.

## Valores de referência (pré-checagem de 25/11 com o parquet novo)

Se um número do notebook se afastar muito destes, revise a preparação antes de escrever o texto.

| Análise | Referência |
|---|---|
| P1a `area_grupo` × `categoria_grupo` | χ²(8) = 95,0; V = 0,50; 20% de caselas com esperado abaixo de 5 |
| P1b `area_grupo` × `grande_area_curso`, sem Indefinido | χ²(12) = 60,4; V = 0,35; 10% |
| P2 `motivacao_grupo`, sem Outros, × `area_grupo` | χ²(12) = 22,2; p = 0,035; V = 0,20; 20% |
| P3 `categoria_grupo` × `estagio_antecipado` | χ²(2) = 3,8; p = 0,15; 0% |
| P4 `objetivo_grupo` × `ano_poli_grupo` | χ²(6) = 28,0; p < 0,001; V = 0,28; 8% |
| P6 ANOVA da importância por `area_pretendida` | F(5; 181) = 2,74; p = 0,021; η² = 0,07; Bartlett p = 0,43 |
| P6 contraste {MF, Consultoria} − demais | −0,45, IC de Scheffé [−0,98; 0,07], p = 0,14 |
| P6 ANOVA de `media_ponderada_num` | F(5; 178) = 0,34; p = 0,89 |
| P6 ordinal `faixa_media` × `area_grupo` | χ²(8) = 8,43; p = 0,39; 7% |
| P7 eliminação (n = 179) | sai Objetivo, depois Tempo, depois Categoria (p = 0,089), depois Horas (p = 0,051); ficam Grande área e Ano; R² = 0,264 |
| P7 proporção "até o 3º ano" | 1º ano 75%, 2º ano 53%, 3º ano ou mais 14% |

---

### Task 1: branch, pasta de testes e funções novas em `stats_tests.py`

**Files:**
- Modify: `src/stats_tests.py` (inserir depois de `chi_square_association`, antes do bloco `# ANOVA`)
- Create: `tests/test_stats_tests.py`

**Interfaces:**
- Consumes: nada.
- Produces:
  - `standardized_residuals(observed: pd.DataFrame) -> pd.DataFrame`: mesma forma e mesmos rótulos de `observed`, valores arredondados em 2 casas;
  - `row_percentages(observed: pd.DataFrame) -> pd.DataFrame`: % por linha, arredondado em 1 casa.

- [ ] **Step 1: criar a branch**

```bash
git checkout -b frente-3-carreira
```

- [ ] **Step 2: escrever o teste que falha**

`tests/test_stats_tests.py`:

```python
import numpy as np
import pandas as pd
from scipy import stats

from src.stats_tests import row_percentages, standardized_residuals


def _table():
    return pd.DataFrame([[10, 20], [30, 40]], index=["a", "b"], columns=["x", "y"])


def test_standardized_residuals_known_2x2():
    res = standardized_residuals(_table())
    # E[a,x] = 30*40/100 = 12; adjusted residual = (10-12)/sqrt(12*0.7*0.6) = -0.89
    assert res.loc["a", "x"] == -0.89
    assert res.loc["a", "y"] == 0.89
    assert list(res.index) == ["a", "b"] and list(res.columns) == ["x", "y"]


def test_standardized_residual_squared_equals_chi_square_in_2x2():
    chi2 = stats.chi2_contingency(_table(), correction=False).statistic
    raw = standardized_residuals(_table()).loc["a", "x"]
    assert np.isclose(raw**2, chi2, atol=0.02)


def test_row_percentages_sum_to_100():
    pct = row_percentages(_table())
    assert pct.loc["a", "x"] == 33.3
    assert np.allclose(pct.sum(axis=1), 100, atol=0.1)
```

- [ ] **Step 3: rodar e ver falhar**

Run: `uv run --with pytest python -m pytest tests/test_stats_tests.py -q`
Expected: FAIL com `ImportError: cannot import name 'row_percentages'`

- [ ] **Step 4: implementar**

Inserir em `src/stats_tests.py`, logo depois de `chi_square_association`:

```python
def standardized_residuals(observed: pd.DataFrame) -> pd.DataFrame:
    """Adjusted standardized residuals of a contingency table: (O - E) / sqrt(E * (1 - row share) * (1 - column share)).
    Under H0 each one is approximately N(0, 1), so |residual| > 2 flags the cells that drive the association."""
    o = observed.to_numpy(dtype=float)
    n = o.sum()
    row = o.sum(axis=1, keepdims=True)
    col = o.sum(axis=0, keepdims=True)
    expected = row @ col / n
    adjusted = (o - expected) / np.sqrt(expected * (1 - row / n) * (1 - col / n))
    return pd.DataFrame(adjusted, index=observed.index, columns=observed.columns).round(2)


def row_percentages(observed: pd.DataFrame) -> pd.DataFrame:
    """Share of each column within each row of a contingency table, in %."""
    return (observed.div(observed.sum(axis=1), axis=0) * 100).round(1)
```

Atualizar a docstring do módulo (linha 3) para "Covered: descriptive summaries, paired t-test, chi-square test of association (with adjusted residuals), …".

- [ ] **Step 5: rodar e ver passar**

Run: `uv run --with pytest python -m pytest tests/test_stats_tests.py -q`
Expected: `3 passed`

- [ ] **Step 6: commit**

```bash
git add src/stats_tests.py tests/test_stats_tests.py docs/superpowers/specs/2026-11-25-frente-3-carreira-design.md docs/superpowers/plans/2026-11-25-frente-3-carreira.md
git commit -m "Adiciona resíduos padronizados e % por linha ao qui-quadrado (Frente 3)"
```

---

### Task 2: `src/carreira.py`: preparação, amostras, agrupamentos e cenários

**Files:**
- Create: `src/carreira.py`
- Create: `tests/test_carreira.py`

**Interfaces:**
- Consumes: `src.regression.fit_ols(df, response, terms)` (só nos testes).
- Produces (usado pelas Tasks 3 a 8):
  - constantes `CATEGORY_ORDER`, `AREA_ORDER`, `CAREER_ORDER`, `CAREER_GROUP_ORDER`, `MOTIVATION_GROUP_ORDER`, `GOAL_GROUP_ORDER`, `YEAR_GROUP_ORDER`, `INTERNSHIP_ORDER`, `GRADE_BAND_ORDER`, `TIME_ORDER`, `MAIN_VARIABLES`, `GROUPINGS`, `CAREER_CONTRASTS`, `REGRESSION_BLOCKS`, `REGRESSION_COLUMNS`, `REGRESSION_LABELS`;
  - `prepare_front_data(df) -> pd.DataFrame`, que acrescenta `categoria_grupo`, `area_grupo`, `motivacao_grupo`, `objetivo_grupo`, `ano_poli_grupo`, `estagio_antecipado` (categórica), `estagio_ate_3ano` (float 0/1/NaN), `faixa_media` e `log_horas_semanais`, e reordena `area_pretendida`, `grande_area_curso` e `tempo_grupo`;
  - `analysis_sample(df, columns: list[str], exclude: dict | None = None) -> pd.DataFrame`;
  - `category_distribution(df, columns: dict) -> pd.DataFrame`, com índice (Variável, Categoria) e colunas `n` e `%`;
  - `grouping_table(df) -> pd.DataFrame`, com as colunas Variável, Categorias originais, Nova categoria, n e Motivo;
  - `build_scenarios(df) -> pd.DataFrame`: 15 linhas, coluna `Cenário` mais todas as colunas de `REGRESSION_BLOCKS`.

- [ ] **Step 1: escrever os testes que falham**

`tests/test_carreira.py`:

```python
from pathlib import Path

import pandas as pd
import pytest

from src.carreira import (REGRESSION_BLOCKS, REGRESSION_COLUMNS, analysis_sample, build_scenarios,
                          category_distribution, grouping_table, prepare_front_data)
from src.regression import fit_ols

DATA = Path(__file__).resolve().parents[1] / "data" / "clean_data.parquet"
pytestmark = pytest.mark.skipif(not DATA.exists(), reason="data/clean_data.parquet not available")


@pytest.fixture(scope="module")
def raw():
    return pd.read_parquet(DATA)


@pytest.fixture(scope="module")
def df(raw):
    return prepare_front_data(raw)


def test_rejects_stale_year_column(raw):
    stale = raw.copy()
    stale.loc[0, "anos_de_poli"] += 1
    with pytest.raises(ValueError, match="anos_de_poli"):
        prepare_front_data(stale)


def test_internship_binary(df):
    assert df["estagio_ate_3ano"].value_counts().to_dict() == {0.0: 104, 1.0: 82}
    assert df["estagio_ate_3ano"].isna().sum() == 1
    assert (df["estagio_antecipado"] == "Até o 3º ano").sum() == 82


def test_groupings_counts(df):
    assert df["area_grupo"].value_counts()["Consultoria & Empreendedorismo"] == 52
    assert df["motivacao_grupo"].value_counts()["Outros"] == 7
    assert df["objetivo_grupo"].value_counts()["Desempenho & Pesquisa"] == 33
    assert df["objetivo_grupo"].isna().sum() == 7
    assert df["ano_poli_grupo"].value_counts().to_dict() == {"1º ano": 31, "2º ano": 93, "3º ano ou mais": 63}
    assert df["categoria_grupo"].value_counts()["Consultoria & Negócios"] == 108
    assert df["faixa_media"].value_counts().to_dict() == {"Abaixo de 7,0": 71, "7,0 a 7,9": 72, "8,0 ou mais": 41}


def test_analysis_sample_drops_level_and_unused_category(df):
    sample = analysis_sample(df, ["motivacao_grupo", "area_grupo"], exclude={"motivacao_grupo": ["Outros"]})
    assert len(sample) == 180
    assert "Outros" not in sample["motivacao_grupo"].cat.categories


def test_category_distribution_includes_missing(df):
    table = category_distribution(df, {"objetivo_grupo": "Objetivo"})
    assert table.loc[("Objetivo", "Sem resposta"), "n"] == 7
    assert table["n"].sum() == 187


def test_grouping_table_counts(df):
    table = grouping_table(df)
    assert table.loc[table["Nova categoria"] == "Consultoria & Empreendedorismo", "n"].item() == 52
    assert table.loc[table["Nova categoria"] == "3º ano ou mais", "n"].item() == 63


def test_scenarios_predict_with_full_model(df):
    data = analysis_sample(df, REGRESSION_COLUMNS)
    assert len(data) == 179
    model = fit_ols(data, "estagio_ate_3ano", REGRESSION_BLOCKS)
    prediction = model.predict(build_scenarios(df))
    assert len(prediction) == 15 and prediction.notna().all()
```

- [ ] **Step 2: rodar e ver falhar**

Run: `uv run --with pytest python -m pytest tests/test_carreira.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'src.carreira'`

- [ ] **Step 3: implementar `src/carreira.py`**

```python
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
```

- [ ] **Step 4: rodar e ver passar**

Run: `uv run --with pytest python -m pytest tests -q`
Expected: `10 passed`

Se `test_groupings_counts` falhar em `motivacao_grupo` ou `area_grupo`, confira se as strings de `GROUPINGS` batem exatamente com `df[col].unique()`. `prepare_front_data` também levanta `"... has unmapped values"` nesse caso.

- [ ] **Step 5: commit**

```bash
git add src/carreira.py tests/test_carreira.py
git commit -m "Adiciona preparação de dados e constantes da Frente 3"
```

---

### Task 3: `src/plotting/plots_carreira.py`

**Files:**
- Create: `src/plotting/plots_carreira.py`
- Create: `tests/test_plots_carreira.py`

**Interfaces:**
- Consumes:
  - `src.plotting.plots_formacao`: `_save`, `COLOR_EXT`, `COLOR_NEUTRAL`, `plot_residual_diagnostics(model, path=None)`;
  - `stats_tests.group_means(...)`, que devolve uma tabela com colunas `n`, `Média`, `IC 95% inf` e `IC 95% sup`, indexada pelos níveis.
- Produces:
  - `plot_category_distribution(df, panels: list[tuple[str, str]], path=None)`: `panels` = [(coluna, título)];
  - `plot_stacked_shares(observed: pd.DataFrame, title: str, legend_title: str, path=None)`;
  - `plot_means_panels(panels: list[tuple[pd.DataFrame, list, str, str, tuple]], path=None)`: cada painel = (tabela de médias, ordem, título, rótulo do eixo x, xlim);
  - `plot_scenario_probabilities(model, scenarios: pd.DataFrame, path=None)`;
  - `plot_residual_diagnostics`, reexportada.

- [ ] **Step 1: escrever o teste de fumaça que falha**

`tests/test_plots_carreira.py`:

```python
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import pandas as pd
import pytest

from src.carreira import (AREA_ORDER, REGRESSION_BLOCKS, REGRESSION_COLUMNS, analysis_sample, build_scenarios,
                          prepare_front_data)
from src.plotting.plots_carreira import (plot_category_distribution, plot_means_panels, plot_residual_diagnostics,
                                         plot_scenario_probabilities, plot_stacked_shares)
from src.regression import fit_ols
from src.stats_tests import group_means

DATA = Path(__file__).resolve().parents[1] / "data" / "clean_data.parquet"
pytestmark = pytest.mark.skipif(not DATA.exists(), reason="data/clean_data.parquet not available")


@pytest.fixture(scope="module")
def df():
    return prepare_front_data(pd.read_parquet(DATA))


def test_all_figures_are_written(df, tmp_path):
    plot_category_distribution(df, [("area_pretendida", "Área"), ("estagio_antecipado", "Estágio")], tmp_path / "a.png")
    plot_stacked_shares(pd.crosstab(df["categoria_grupo"], df["area_grupo"]), "Título", "Legenda", tmp_path / "b.png")
    means = group_means(df, "importancia_media", "grande_area_curso")
    plot_means_panels([(means, AREA_ORDER, "Painel", "Eixo x", (1, 5))], tmp_path / "c.png")
    model = fit_ols(analysis_sample(df, REGRESSION_COLUMNS), "estagio_ate_3ano", REGRESSION_BLOCKS)
    plot_scenario_probabilities(model, build_scenarios(df), tmp_path / "d.png")
    plot_residual_diagnostics(model, tmp_path / "e.png")
    assert all((tmp_path / f"{name}.png").stat().st_size > 0 for name in "abcde")
```

- [ ] **Step 2: rodar e ver falhar**

Run: `uv run --with pytest python -m pytest tests/test_plots_carreira.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'src.plotting.plots_carreira'`

- [ ] **Step 3: implementar**

`src/plotting/plots_carreira.py`:

```python
"""Figures for front 3 (Carreira: trajetória & objetivos). Titles and labels in PT-BR, as required by the README."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.plotting.plots_formacao import COLOR_EXT, COLOR_NEUTRAL, _save, plot_residual_diagnostics

__all__ = ["plot_category_distribution", "plot_stacked_shares", "plot_means_panels", "plot_scenario_probabilities",
           "plot_residual_diagnostics"]


def plot_category_distribution(df, panels, path=None):
    """Horizontal bars with the % of valid answers in each level; `panels` is a list of (categorical column, title)."""
    fig, axes = plt.subplots(1, len(panels), figsize=(5.6 * len(panels), 4.4))
    for ax, (col, title) in zip(np.atleast_1d(axes), panels):
        order = list(df[col].cat.categories)
        counts = df[col].value_counts().reindex(order, fill_value=0)
        share = counts / counts.sum() * 100
        y = np.arange(len(order))
        bars = ax.barh(y, share.values, color=COLOR_EXT)
        ax.bar_label(bars, labels=[f"{v:.0f}% (n={n})" for v, n in zip(share.values, counts.values)], fontsize=8,
                     padding=2)
        ax.set_yticks(y)
        ax.set_yticklabels(order)
        ax.invert_yaxis()
        ax.set(xlim=(0, share.max() * 1.4), xlabel="% das respostas válidas", title=title)
        sns.despine(ax=ax)
    _save(fig, path)


def plot_stacked_shares(observed, title, legend_title, path=None):
    """100% stacked horizontal bars of a contingency table (rows = groups, columns = answers); n of each row in its
    label. Segments below 7% are left without a number to keep the bars readable."""
    shares = observed.div(observed.sum(axis=1), axis=0) * 100
    colors = sns.color_palette("tab10", n_colors=shares.shape[1])
    fig, ax = plt.subplots(figsize=(10, 0.6 * len(shares) + 1.8))
    y = np.arange(len(shares))
    left = np.zeros(len(shares))
    for color, col in zip(colors, shares.columns):
        values = shares[col].to_numpy()
        bars = ax.barh(y, values, left=left, color=color, label=str(col))
        ax.bar_label(bars, labels=[f"{v:.0f}%" if v >= 7 else "" for v in values], label_type="center", fontsize=8,
                     color="white")
        left += values
    ax.set_yticks(y)
    ax.set_yticklabels([f"{level} (n={n})" for level, n in zip(shares.index, observed.sum(axis=1))])
    ax.invert_yaxis()
    ax.set(xlim=(0, 100), xlabel="% dentro de cada linha", title=title)
    ax.legend(title=legend_title, frameon=False, bbox_to_anchor=(1.01, 1), loc="upper left")
    sns.despine(ax=ax)
    _save(fig, path)


def plot_means_panels(panels, path=None):
    """Dot plots of group means with t confidence intervals, one panel per (means table, order, title, xlabel, xlim).
    The tables come from stats_tests.group_means."""
    fig, axes = plt.subplots(1, len(panels), figsize=(6.8 * len(panels), 4.2))
    for ax, (table, order, title, xlabel, xlim) in zip(np.atleast_1d(axes), panels):
        t = table.reindex(order)
        y = np.arange(len(t))
        ax.errorbar(t["Média"], y, xerr=[t["Média"] - t["IC 95% inf"], t["IC 95% sup"] - t["Média"]], fmt="o",
                    color=COLOR_EXT, capsize=4)
        for yi, m in enumerate(t["Média"]):
            ax.annotate(f"{m:.2f}", (m, yi), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
        ax.set_yticks(y)
        ax.set_yticklabels([f"{level} (n={int(n)})" for level, n in zip(t.index, t["n"])])
        ax.invert_yaxis()
        ax.set(xlim=xlim, xlabel=xlabel, title=title)
        sns.despine(ax=ax)
    _save(fig, path)


def plot_scenario_probabilities(model, scenarios, path=None):
    """Estimated probability (%) of planning the first internship up to the 3rd year for each a-priori profile, with
    the 95% confidence interval of the mean. Values outside 0-100% are a known limitation of the linear model."""
    pred = model.get_prediction(scenarios).summary_frame(alpha=0.05) * 100
    y = np.arange(len(scenarios))
    fig, ax = plt.subplots(figsize=(9, 0.35 * len(scenarios) + 1.8))
    ax.errorbar(pred["mean"], y, xerr=[pred["mean"] - pred["mean_ci_lower"], pred["mean_ci_upper"] - pred["mean"]],
                fmt="o", color=COLOR_EXT, capsize=3)
    for limit in (0, 100):
        ax.axvline(limit, color=COLOR_NEUTRAL, lw=0.8, ls="--")
    ax.set_yticks(y)
    ax.set_yticklabels(scenarios["Cenário"])
    ax.invert_yaxis()
    ax.set(xlabel="Probabilidade estimada de pretender o 1º estágio até o 3º ano (%; IC 95% da média)",
           title="Perfis definidos a priori: intenção de antecipar o estágio (modelo final)")
    sns.despine(ax=ax)
    _save(fig, path)
```

- [ ] **Step 4: rodar e ver passar**

Run: `uv run --with pytest python -m pytest tests -q`
Expected: `11 passed`

- [ ] **Step 5: abrir as 5 figuras do teste e conferir à vista**

Rode o teste com `--basetemp=/tmp/f3plots` e abra os PNGs. Confira:
- nenhum rótulo cortado;
- as barras empilhadas somam 100%;
- as legendas estão fora das barras.

Corrija `figsize` se algo estiver cortado.

- [ ] **Step 6: commit**

```bash
git add src/plotting/plots_carreira.py tests/test_plots_carreira.py
git commit -m "Adiciona gráficos da Frente 3"
```

---

### Task 4: notebook, partes 0 a 2 (apresentação, preparação, dados e descritiva)

**Files:**
- Create: `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb`

**Interfaces:**
- Consumes: tudo da Task 2 e da Task 3; `stats_tests.chi_square_association`.
- Produces:
  - variáveis `df`, `TAB_DIR` e `FIG_DIR` no notebook;
  - artefatos `f3_tab01_descritiva.csv`, `f3_tab02_agrupamentos.csv` e `f3_fig01_distribuicao_variaveis_principais.png`.

Crie o arquivo vazio com `uv run --with nbformat python -c "import nbformat; nb = nbformat.v4.new_notebook(); nb.metadata['kernelspec'] = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}; nbformat.write(nb, 'notebooks/02_Carreira_Trajetoria_Objetivos.ipynb')"` e acrescente as células em ordem (pela ferramenta NotebookEdit ou pelo Jupyter).

- [ ] **Step 1: célula markdown de apresentação**

```markdown
# Frente 3 — Carreira: trajetória e objetivos

**PRO3201 — Estatística e Aplicações · Grupo 10 (J)**

**Pergunta da frente:** como a vivência no grupo de extensão se conecta ao horizonte profissional de curto prazo (estágio e objetivo atual) e de médio prazo (área pretendida após a formatura)?

### Como ler este notebook

- **Leia como um artigo.** As células de código só chamam funções com nomes autoexplicativos (em inglês, pela convenção do README). A lógica fica em `src/`:
  - `stats_tests.py`: testes da disciplina;
  - `regression.py`: regressão linear múltipla;
  - `carreira.py`: preparação dos dados e agrupamentos;
  - `plotting/plots_carreira.py`: gráficos.
- **Cada pergunta segue os itens (a) a (e) do guia:** hipóteses; teste e premissas; resultado; gráfico ou tabela; conclusão para o relatório.
- **Métodos:** só os da disciplina (qui-quadrado, ANOVA com Bartlett e Scheffé, regressão linear com F parcial), α = 5%.
- **Perguntas do guia cortadas:**
  - P5 (o estágio derruba as horas no grupo): praticamente ninguém da amostra está estagiando;
  - P8 (prever a área pretendida): com 6 áreas, n = 187 e sem regressão logística, a previsão não se sustenta.
```

- [ ] **Step 2: célula markdown "## 0. Preparação" e célula de código de carga**

Markdown: `## 0. Preparação` + `*Célula técnica: só carrega as funções e os dados. Pode ser pulada na leitura.*`

Código:

```python
%load_ext autoreload
%autoreload 2

import sys
from pathlib import Path

ROOT_DIR = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
DATA_DIR, FIG_DIR, TAB_DIR = ROOT_DIR / "data", ROOT_DIR / "output" / "figures", ROOT_DIR / "output" / "tables"
FIG_DIR.mkdir(parents=True, exist_ok=True)
TAB_DIR.mkdir(parents=True, exist_ok=True)
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import pandas as pd

from src.carreira import (AREA_ORDER, CAREER_CONTRASTS, CAREER_GROUP_ORDER, CAREER_ORDER, MAIN_VARIABLES,
                          REGRESSION_BLOCKS, REGRESSION_COLUMNS, REGRESSION_LABELS, YEAR_GROUP_ORDER, analysis_sample,
                          build_scenarios, category_distribution, grouping_table, prepare_front_data)
from src.plotting.plots_carreira import (plot_category_distribution, plot_means_panels, plot_residual_diagnostics,
                                         plot_scenario_probabilities, plot_stacked_shares)
from src.regression import (backward_elimination, coefficient_table, fit_ols, joint_partial_f_test, model_summary,
                            predict_scenarios)
from src.stats_tests import (chi_square_association, group_means, one_way_anova, row_percentages, scheffe_contrasts,
                             standardized_residuals)

pd.set_option("display.max_columns", None)
df = prepare_front_data(pd.read_parquet(DATA_DIR / "clean_data.parquet"))
print(f"{len(df)} alunos carregados.")
```

- [ ] **Step 3: markdown "## 1. Dados e cuidados gerais"**

```markdown
## 1. Dados e cuidados gerais

- **Base:** `clean_data.parquet` gerado de novo em 25/11, com 187 alunos da Poli, todos participantes de grupos de extensão. Na versão de 24/11, a coluna `anos_de_poli` estava desalinhada para 30 alunos. A preparação confere que ela bate com o ano de ingresso e interrompe a execução se receber um arquivo antigo.
- **A amostra é jovem:** 31 alunos no 1º ano, 93 no 2º e 63 no 3º ano ou depois (só 9 no 4º ou 5º). Por isso, **o momento do estágio mede intenção**, não um fato. A maioria ainda não chegou à idade de estagiar.
- **Agrupamentos (tabela abaixo):** o teste qui-quadrado só é confiável quando poucas caselas têm frequência esperada abaixo de 5. Usamos o mesmo critério da Frente 1: no máximo cerca de 20% das caselas. Cada agrupamento foi escolhido para cumprir esse critério, e o motivo aparece na tabela.
- **Exclusões feitas teste a teste, sem apagar linhas da base:**
  - "Outros" na motivação (n = 7) fica fora do qui-quadrado da P2;
  - "Indefinido" na área pretendida (n = 20) fica fora só da P1b;
  - as 7 respostas sem objetivo ficam fora dos testes que usam objetivo;
  - a única resposta "Não pretendo realizar estágio" fica fora da P3 e da P7.

> **Conceito — linguagem associativa.** Todos os alunos da amostra fazem extensão, e não há grupo de controle. Os testes mostram **associações** ("quem está no grupo X tende a mirar a área Y"), não efeitos causais ("o grupo X leva a mirar Y"). Também pode ser que o aluno escolha o grupo por já mirar a área.
```

- [ ] **Step 4: código da tabela de agrupamentos**

```python
groupings = grouping_table(df)
groupings.to_csv(TAB_DIR / "f3_tab02_agrupamentos.csv", index=False)
groupings
```

- [ ] **Step 5: markdown "## 2. Diagnóstico descritivo" e código**

```python
descriptive = category_distribution(df, MAIN_VARIABLES)
descriptive.to_csv(TAB_DIR / "f3_tab01_descritiva.csv")
descriptive
```

```python
plot_category_distribution(df, [("area_pretendida", "(a) Área pretendida após a formatura"),
                                ("estagio_antecipado", "(b) Quando pretende fazer o 1º estágio"),
                                ("objetivo_grupo", "(c) Objetivo principal atual")],
                           FIG_DIR / "f3_fig01_distribuicao_variaveis_principais.png")
```

A tabela descritiva é a `f3_tab01`, mesmo aparecendo depois da `f3_tab02`. Assim a numeração bate com a ordem de leitura do relatório, que começa pela descritiva. A ordem das células acima é intencional: os cuidados com os dados vêm antes.

- [ ] **Step 6: executar o notebook e escrever a "Leitura" da descritiva**

Run: `cd notebooks && uv run --with nbconvert jupyter nbconvert --to notebook --execute --inplace 02_Carreira_Trajetoria_Objetivos.ipynb`
Expected: termina sem erro e imprime "187 alunos carregados."

Acrescente uma célula markdown `**Leitura.**` com 3 a 4 itens, usando os números impressos. Esperado:
- Mercado Financeiro é a área mais citada (49; 26%), seguida de Indústria/Engenharia (42);
- 82 de 186 (44%) pretendem estagiar até o 3º ano;
- "Grupo de extensão" é o objetivo mais comum (77 de 180).

- [ ] **Step 7: commit**

```bash
git add notebooks/02_Carreira_Trajetoria_Objetivos.ipynb output/tables/f3_tab01_descritiva.csv output/tables/f3_tab02_agrupamentos.csv output/figures/f3_fig01_distribuicao_variaveis_principais.png
git commit -m "Adiciona preparação e descritiva da Frente 3"
```

---

### Task 5: notebook, P1 e P2 (área pretendida × grupo, curso e motivação)

**Files:**
- Modify: `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb` (acrescentar ao final)

**Interfaces:**
- Consumes: `df`, `TAB_DIR`, `FIG_DIR`, `analysis_sample`, `chi_square_association`, `standardized_residuals`, `row_percentages`, `plot_stacked_shares`.
- Produces:
  - tabelas `f3_tab03_p1_area_x_categoria.csv`, `f3_tab04_p1_area_x_grande_area.csv`, `f3_tab05_p1_qui_quadrado.csv`, `f3_tab06_p1a_residuos.csv`, `f3_tab07_p1b_residuos.csv`, `f3_tab08_p2_motivacao_x_area.csv`, `f3_tab09_p2_qui_quadrado.csv`, `f3_tab10_p2_residuos.csv`;
  - figuras `f3_fig02_p1_area_por_categoria.png`, `f3_fig03_p1_area_por_grande_area.png`, `f3_fig04_p2_area_por_motivacao.png`.

- [ ] **Step 1: markdown da P1, itens (a) e (b)**

```markdown
## 3. P1 — A área pretendida está associada ao grupo de extensão e ao curso?

**(a) Pergunta e hipóteses.** Dois testes de associação.

- **P1a** — área pretendida × categoria do grupo:
  - $H_0$: a área pretendida é independente da categoria do grupo;
  - $H_1$: há associação.
- **P1b** — área pretendida × grande área do curso:
  - $H_0$: a área pretendida é independente da grande área do curso;
  - $H_1$: há associação.

**(b) Teste e premissas.** Qui-quadrado de associação. As premissas são duas: observações independentes (um aluno por linha) e no máximo cerca de 20% das caselas com frequência esperada abaixo de 5.

- Na P1a, Consultoria e Empreendedorismo foram somadas como área pretendida (tabela de agrupamentos).
- Na P1b, os 20 alunos "Indefinido" ficam de fora. Com eles, 28% das caselas ficam abaixo de 5; sem eles, 10%.

> **Conceito — resíduo padronizado ajustado.** O qui-quadrado diz *se* há associação, mas não *onde*. Para cada casela, o resíduo ajustado compara o observado com o esperado sob independência, em unidades de desvio-padrão: $r = (O - E) / \sqrt{E (1 - p_{\text{linha}})(1 - p_{\text{coluna}})}$. Sob $H_0$, ele segue aproximadamente uma normal padrão. Por isso, $|r| > 2$ indica uma casela com bem mais (r positivo) ou bem menos (r negativo) alunos do que o esperado.
>
> **Conceito — V de Cramér.** $V = \sqrt{\chi^2 / (n \cdot k)}$, com $k$ = min(linhas, colunas) − 1. Vai de 0 (nenhuma associação) a 1 (associação total). Referências usuais para $k = 2$: 0,07 fraca, 0,21 moderada e 0,35 forte.
```

- [ ] **Step 2: código da P1a e da P1b**

```python
p1a_sample = analysis_sample(df, ["area_grupo", "categoria_grupo"])
p1a_observed, p1a_result = chi_square_association(p1a_sample, "categoria_grupo", "area_grupo")
p1b_sample = analysis_sample(df, ["area_grupo", "grande_area_curso"], exclude={"area_grupo": ["Indefinido"]})
p1b_observed, p1b_result = chi_square_association(p1b_sample, "grande_area_curso", "area_grupo")

p1_results = pd.concat({"P1a: área pretendida × categoria do grupo": p1a_result.iloc[:, 0],
                        "P1b: área pretendida × grande área do curso (sem Indefinido)": p1b_result.iloc[:, 0]},
                       axis=1).T.rename_axis("Teste")
p1a_observed.to_csv(TAB_DIR / "f3_tab03_p1_area_x_categoria.csv")
p1b_observed.to_csv(TAB_DIR / "f3_tab04_p1_area_x_grande_area.csv")
p1_results.to_csv(TAB_DIR / "f3_tab05_p1_qui_quadrado.csv")
p1_results
```

```python
print("P1a — contagens e % por categoria do grupo")
display(p1a_observed)
display(row_percentages(p1a_observed))
print("P1a — resíduos padronizados ajustados (|r| > 2 em destaque na leitura)")
p1a_residuals = standardized_residuals(p1a_observed)
p1a_residuals.to_csv(TAB_DIR / "f3_tab06_p1a_residuos.csv")
p1a_residuals
```

```python
print("P1b — contagens e % por grande área do curso")
display(p1b_observed)
display(row_percentages(p1b_observed))
p1b_residuals = standardized_residuals(p1b_observed)
p1b_residuals.to_csv(TAB_DIR / "f3_tab07_p1b_residuos.csv")
p1b_residuals
```

```python
plot_stacked_shares(p1a_observed, "Área pretendida após a formatura, por categoria do grupo de extensão",
                    "Área pretendida", FIG_DIR / "f3_fig02_p1_area_por_categoria.png")
plot_stacked_shares(p1b_observed, "Área pretendida após a formatura, por grande área do curso (sem Indefinido)",
                    "Área pretendida", FIG_DIR / "f3_fig03_p1_area_por_grande_area.png")
```

- [ ] **Step 3: markdown da P2, itens (a) e (b), e código**

```markdown
## 4. P2 — A motivação para entrar no grupo se reflete na área pretendida?

**(a) Pergunta e hipóteses.**

- $H_0$: a área pretendida é independente da motivação de ingresso;
- $H_1$: há associação.

**(b) Teste e premissas.** Qui-quadrado de associação, com resíduos ajustados.

- "Outros" (Networking, 6, e Indicação de amigos, 1) fica fora do teste: com essa linha, 40% das caselas ficam abaixo de 5; sem ela, 20%. Por isso n = 180.
- Consultoria e Empreendedorismo continuam somadas, como na P1.
```

```python
p2_sample = analysis_sample(df, ["motivacao_grupo", "area_grupo"], exclude={"motivacao_grupo": ["Outros"]})
p2_observed, p2_result = chi_square_association(p2_sample, "motivacao_grupo", "area_grupo")
p2_observed.to_csv(TAB_DIR / "f3_tab08_p2_motivacao_x_area.csv")
p2_result.to_csv(TAB_DIR / "f3_tab09_p2_qui_quadrado.csv")
display(p2_observed)
display(row_percentages(p2_observed))
p2_result
```

```python
p2_residuals = standardized_residuals(p2_observed)
p2_residuals.to_csv(TAB_DIR / "f3_tab10_p2_residuos.csv")
display(p2_residuals)
plot_stacked_shares(p2_observed, "Área pretendida após a formatura, por motivação para entrar no grupo",
                    "Área pretendida", FIG_DIR / "f3_fig04_p2_area_por_motivacao.png")
```

- [ ] **Step 4: executar e conferir com as referências**

Run: `cd notebooks && uv run --with nbconvert jupyter nbconvert --to notebook --execute --inplace 02_Carreira_Trajetoria_Objetivos.ipynb`
Expected:
- P1a χ² ≈ 95,0 com 8 gl, V ≈ 0,50, 20% de caselas abaixo de 5;
- P1b χ² ≈ 60,4 com 12 gl, V ≈ 0,35, 10%;
- P2 χ² ≈ 22,2 com 12 gl, p ≈ 0,035, V ≈ 0,20, 20%.

- [ ] **Step 5: escrever os itens (c), (d) e (e) da P1 e da P2**

Para cada pergunta, uma célula markdown com:
- **(c) Resultado:** χ², gl, p, V de Cramér (com a referência de força), % de caselas abaixo de 5 e as caselas com |r| > 2, citando o % da linha (por exemplo, "65% dos alunos de grupos de Mercado Financeiro miram Mercado Financeiro, r = …");
- **(d):** os nomes das figuras e tabelas;
- **(e) Conclusão para o relatório:** 3 a 4 linhas, linguagem associativa.

Na P1, comente o possível viés de autosseleção: o aluno pode escolher o grupo pela área que já mirava. Na P2, destaque que o efeito é fraco (V ≈ 0,20) e que p ≈ 0,035 fica perto do limite.

- [ ] **Step 6: commit**

```bash
git add notebooks/02_Carreira_Trajetoria_Objetivos.ipynb output/tables/f3_tab0[3-9]_*.csv output/tables/f3_tab10_*.csv output/figures/f3_fig0[2-4]_*.png
git commit -m "Adiciona P1 e P2 da Frente 3 (área pretendida)"
```

---

### Task 6: notebook, P3 e P4 (intenção de antecipar o estágio; objetivo × ano)

**Files:**
- Modify: `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb`

**Interfaces:**
- Consumes: os mesmos da Task 5.
- Produces:
  - tabelas `f3_tab11_p3_categoria_x_estagio.csv`, `f3_tab12_p3_qui_quadrado.csv`, `f3_tab13_p4_objetivo_x_ano.csv`, `f3_tab14_p4_qui_quadrado.csv`, `f3_tab15_p4_residuos.csv`;
  - figuras `f3_fig05_p3_estagio_por_categoria.png`, `f3_fig06_p4_objetivo_por_ano.png`.

- [ ] **Step 1: markdown e código da P3**

```markdown
## 5. P3 — Alunos de alguma categoria de grupo pretendem antecipar o 1º estágio?

**(a) Pergunta e hipóteses.**

- $H_0$: pretender o 1º estágio até o 3º ano é independente da categoria do grupo;
- $H_1$: há associação.

**(b) Teste e premissas.** Qui-quadrado de associação numa tabela 3 × 2 (n = 186, sem a resposta "Não pretendo realizar estágio"). Nenhuma casela tem esperado abaixo de 5.

**Atenção:** como a maioria ainda está no 1º ou 2º ano, a variável mede **intenção**. A pergunta é "quem *pretende* estagiar mais cedo", não "quem estagiou mais cedo".
```

```python
p3_sample = analysis_sample(df, ["categoria_grupo", "estagio_antecipado"])
p3_observed, p3_result = chi_square_association(p3_sample, "categoria_grupo", "estagio_antecipado")
p3_observed.to_csv(TAB_DIR / "f3_tab11_p3_categoria_x_estagio.csv")
p3_result.to_csv(TAB_DIR / "f3_tab12_p3_qui_quadrado.csv")
display(p3_observed)
display(row_percentages(p3_observed))
display(p3_result)
plot_stacked_shares(p3_observed, "Quando pretende fazer o 1º estágio, por categoria do grupo de extensão",
                    "1º estágio", FIG_DIR / "f3_fig05_p3_estagio_por_categoria.png")
```

- [ ] **Step 2: markdown e código da P4**

```markdown
## 6. P4 — O objetivo principal muda ao longo da graduação?

**(a) Pergunta e hipóteses.**

- $H_0$: o objetivo principal atual é independente do ano na Poli;
- $H_1$: há associação.

**(b) Teste e premissas.** Qui-quadrado de associação (n = 180, sem os 7 objetivos ausentes), com resíduos ajustados.

- Os anos 3, 4 e 5 foram somados, porque só 9 alunos estão no 4º ou 5º ano.
- "Desempenho acadêmico" e "Iniciação científica" foram somados (n = 6 em Iniciação científica). Com 5 objetivos, 33% das caselas ficam abaixo de 5; com 4, 8%.

**Atenção:** os dados são de um único momento. Compararam-se **turmas diferentes** (quem está hoje no 1º, no 2º e no 3º ano), não as mesmas pessoas ao longo do tempo. A "migração" é uma leitura entre turmas.
```

```python
p4_sample = analysis_sample(df, ["objetivo_grupo", "ano_poli_grupo"])
p4_observed, p4_result = chi_square_association(p4_sample, "ano_poli_grupo", "objetivo_grupo")
p4_observed.to_csv(TAB_DIR / "f3_tab13_p4_objetivo_x_ano.csv")
p4_result.to_csv(TAB_DIR / "f3_tab14_p4_qui_quadrado.csv")
display(p4_observed)
display(row_percentages(p4_observed))
p4_result
```

```python
p4_residuals = standardized_residuals(p4_observed)
p4_residuals.to_csv(TAB_DIR / "f3_tab15_p4_residuos.csv")
display(p4_residuals)
plot_stacked_shares(p4_observed, "Objetivo principal atual, por ano na Poli", "Objetivo atual",
                    FIG_DIR / "f3_fig06_p4_objetivo_por_ano.png")
```

- [ ] **Step 3: executar e conferir**

Run: `cd notebooks && uv run --with nbconvert jupyter nbconvert --to notebook --execute --inplace 02_Carreira_Trajetoria_Objetivos.ipynb`
Expected:
- P3: χ² ≈ 3,8 com 2 gl, p ≈ 0,15, 0% de caselas abaixo de 5;
- P4: χ² ≈ 28,0 com 6 gl, p < 0,001, V ≈ 0,28, 8%.

- [ ] **Step 4: escrever os itens (c), (d) e (e) da P3 e da P4**

**P3:**
- é "não rejeita $H_0$": não há evidência de diferença entre as categorias;
- cite as 3 proporções de "até o 3º ano";
- deixe claro que ausência de evidência não é evidência de ausência, e que o resultado fala de intenção.

**P4:**
- cite as caselas com |r| > 2. A expectativa é que "Grupo de extensão" pese mais no 1º e 2º ano e "Estágio" no 3º ano ou mais; confira na tabela;
- conclusão entre turmas, com a ressalva de que não é acompanhamento das mesmas pessoas;
- mencione que, com a coluna `anos_de_poli` antiga (desalinhada), o teste daria p ≈ 0,095. Esse é o motivo de o parquet ter sido gerado de novo.

- [ ] **Step 5: commit**

```bash
git add notebooks/02_Carreira_Trajetoria_Objetivos.ipynb output/tables/f3_tab1[1-5]_*.csv output/figures/f3_fig0[5-6]_*.png
git commit -m "Adiciona P3 e P4 da Frente 3 (estágio e objetivo por ano)"
```

---

### Task 7: notebook, P6 (área pretendida × importância da média e × média ponderada)

**Files:**
- Modify: `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb`

**Interfaces:**
- Consumes: `one_way_anova`, `group_means`, `scheffe_contrasts`, `CAREER_CONTRASTS`, `CAREER_ORDER`, `plot_means_panels`, `chi_square_association`, `analysis_sample`.
- Produces:
  - tabelas `f3_tab16_p6_anova.csv`, `f3_tab17_p6_medias.csv`, `f3_tab18_p6_scheffe.csv`, `f3_tab19_p6_ordinal.csv`;
  - figura `f3_fig07_p6_medias_por_area.png`.

- [ ] **Step 1: markdown da P6, itens (a) e (b)**

```markdown
## 7. P6 — Quem mira Mercado Financeiro ou Consultoria valoriza mais a média e tem média maior?

**(a) Pergunta e hipóteses.** Seja $\mu_j$ a média da variável entre os alunos que pretendem a área $j$ (6 áreas, sem agrupar: a ANOVA não tem a restrição de caselas do qui-quadrado). Duas ANOVAs:

- **importância da média ponderada** (escala 1–5): $H_0$: $\mu_1 = \dots = \mu_6$; $H_1$: ao menos uma média difere;
- **média ponderada** (ponto médio da faixa): mesmas hipóteses.

A hipótese do guia vira um **contraste definido antes de ver os resultados**: a média simples de {Mercado Financeiro, Consultoria} menos a média simples das outras 4 áreas. $H_1$ do guia: o contraste é positivo.

**(b) Teste e premissas.** ANOVA de 1 fator, com:

- teste de Bartlett para a igualdade das variâncias;
- η² como tamanho de efeito;
- Scheffé para o contraste e para todos os pares (só na importância da média).

Regra 3 do guia: a média ponderada numérica é uma aproximação pelo ponto médio das faixas. Por isso, o resultado é checado também na versão ordinal, com um qui-quadrado de 3 faixas (abaixo de 7,0; 7,0 a 7,9; 8,0 ou mais) × área agrupada.

A Frente 1 (P6) já mostrou que o **objetivo atual** explica 27% da variação da importância dada à média. Aqui a pergunta é se a **área pretendida** acrescenta algo, olhada sozinha.

> **Conceito — contraste de Scheffé.** Um contraste é uma combinação das médias com pesos que somam zero, por exemplo $L = \tfrac{1}{2}\mu_{MF} + \tfrac{1}{2}\mu_{C} - \tfrac{1}{4}(\mu_{E} + \mu_{I} + \mu_{T} + \mu_{Ind})$. O teste de Scheffé controla o erro para qualquer quantidade de contrastes, inclusive os escolhidos depois de olhar os dados. Por isso ele também é usado nos pares.
```

- [ ] **Step 2: código das ANOVAs e das médias**

```python
p6_outcomes = {"importancia_media": "Importância da média ponderada (1–5)",
               "media_ponderada_num": "Média ponderada (ponto médio da faixa)"}
p6_anova = pd.concat([one_way_anova(df, col, "area_pretendida", title=f"ANOVA de 1 fator: {label} por área pretendida")
                      for col, label in p6_outcomes.items()], axis=1).T
p6_anova.to_csv(TAB_DIR / "f3_tab16_p6_anova.csv")
p6_anova
```

```python
p6_means = {label: group_means(df, col, "area_pretendida", "Área pretendida") for col, label in p6_outcomes.items()}
pd.concat(p6_means, axis=1).to_csv(TAB_DIR / "f3_tab17_p6_medias.csv")
plot_means_panels([(p6_means[p6_outcomes["importancia_media"]], CAREER_ORDER, "(a) Importância da média ponderada",
                    "Média e IC 95% (escala 1–5)", (1, 5)),
                   (p6_means[p6_outcomes["media_ponderada_num"]], CAREER_ORDER, "(b) Média ponderada",
                    "Média e IC 95% (nota 0–10)", (5.5, 9))],
                  FIG_DIR / "f3_fig07_p6_medias_por_area.png")
pd.concat(p6_means, axis=1)
```

- [ ] **Step 3: código do Scheffé e da checagem ordinal**

```python
p6_scheffe = pd.concat({
    "Importância da média — contraste a priori": scheffe_contrasts(df, "importancia_media", "area_pretendida",
                                                                    CAREER_CONTRASTS),
    "Média ponderada — contraste a priori": scheffe_contrasts(df, "media_ponderada_num", "area_pretendida",
                                                              CAREER_CONTRASTS),
    "Importância da média — todos os pares": scheffe_contrasts(df, "importancia_media", "area_pretendida"),
}, names=["Análise", "Contraste"])
p6_scheffe.to_csv(TAB_DIR / "f3_tab18_p6_scheffe.csv")
p6_scheffe
```

```python
p6_ordinal_sample = analysis_sample(df, ["area_grupo", "faixa_media"])
p6_ordinal_observed, p6_ordinal_result = chi_square_association(p6_ordinal_sample, "area_grupo", "faixa_media")
p6_ordinal_result.to_csv(TAB_DIR / "f3_tab19_p6_ordinal.csv")
display(p6_ordinal_observed)
p6_ordinal_result
```

- [ ] **Step 4: executar e conferir**

Run: `cd notebooks && uv run --with nbconvert jupyter nbconvert --to notebook --execute --inplace 02_Carreira_Trajetoria_Objetivos.ipynb`
Expected:
- importância: F(5; 181) ≈ 2,74, p ≈ 0,021, η² ≈ 0,07, Bartlett p ≈ 0,43;
- contraste ≈ −0,45, IC [−0,98; 0,07], p ≈ 0,14;
- média ponderada: F(5; 178) ≈ 0,34, p ≈ 0,89;
- ordinal: χ²(8) ≈ 8,43, p ≈ 0,39.

- [ ] **Step 5: escrever os itens (c), (d) e (e) da P6**

O resultado **contraria a hipótese do guia**:
- a área se associa de forma fraca à importância da média (η² ≈ 0,07);
- mas Mercado Financeiro tem a **menor** média (≈ 2,59) e Indústria/Engenharia a maior (≈ 3,29);
- o contraste a priori sai negativo e não significativo;
- diga quais pares, se algum, o Scheffé aponta.

Na média ponderada, não há diferença, nem na versão numérica nem na ordinal. Conclua com uma possível leitura, sem afirmar causa: quem mira Mercado Financeiro pode apostar mais em experiência e processos seletivos do que na nota. Compare com o η² ≈ 0,27 do objetivo atual na Frente 1.

- [ ] **Step 6: commit**

```bash
git add notebooks/02_Carreira_Trajetoria_Objetivos.ipynb output/tables/f3_tab1[6-9]_*.csv output/figures/f3_fig07_*.png
git commit -m "Adiciona P6 da Frente 3 (área pretendida e média)"
```

---

### Task 8: notebook, P7 (modelo explicativo da intenção de antecipar o estágio)

**Files:**
- Modify: `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb`

**Interfaces:**
- Consumes:
  - `analysis_sample`, `REGRESSION_COLUMNS`, `REGRESSION_BLOCKS`, `REGRESSION_LABELS`, `build_scenarios`;
  - de `src.regression`: `backward_elimination(df, response, blocks) -> (steps, final_model, kept)`, `fit_ols`, `joint_partial_f_test(full, reduced, name)`, `model_summary`, `coefficient_table(model, labels)`, `predict_scenarios(model, scenarios)`;
  - `plot_scenario_probabilities`, `plot_residual_diagnostics`.
- Produces:
  - tabelas `f3_tab20_p7_eliminacao_f_parcial.csv`, `f3_tab21_p7_coeficientes.csv`, `f3_tab22_p7_cenarios.csv`;
  - figuras `f3_fig08_p7_cenarios.png`, `f3_fig09_p7_residuos.png`.

**Armadilha:** `backward_elimination` só descarta linhas sem resposta. Se um preditor tiver valor ausente (`objetivo_grupo` tem 7), os modelos comparados pelo F parcial teriam n diferentes e o teste ficaria inválido. Por isso a amostra é filtrada **antes**, com `analysis_sample(df, REGRESSION_COLUMNS)` (n = 179).

- [ ] **Step 1: markdown da P7**

```markdown
## 8. P7 — Modelo explicativo: o que se associa à intenção de antecipar o 1º estágio?

**(a) Objetivo e hipóteses.** A resposta é $Y$ = 1 se o aluno pretende fazer o 1º estágio até o 3º ano, e 0 se pretende no 4º ano ou depois. O modelo completo foi definido antes de ver os resultados, com 6 blocos de preditores: categoria do grupo, grande área do curso, ano na Poli, objetivo atual, tempo no grupo e ln(horas semanais).

- Para cada bloco: $H_0$: os coeficientes do bloco são todos zero (dados os demais); $H_1$: ao menos um é diferente de zero.

**(b) Método e premissas.** Regressão linear múltipla de uma resposta 0/1, chamada **modelo de probabilidade linear**: o valor previsto é lido como uma probabilidade, e cada β é uma diferença em **pontos percentuais**. Etapas:

1. eliminação para trás por F parcial: a cada passo, sai o bloco de maior p, se p ≥ 0,05;
2. F parcial conjunto entre o modelo completo e o final;
3. coeficientes com IC 95%;
4. perfis definidos a priori (cada ano × cada grande área).

O método tem limitações conhecidas, que são declaradas:

- as previsões podem sair do intervalo de 0 a 100%;
- a variância dos resíduos não é constante por construção, já que $Y$ só vale 0 ou 1;
- os resíduos não são normais.

Com n = 179, os testes F continuam aproximadamente válidos. A regressão logística seria o modelo natural, mas está fora dos métodos da disciplina.

> **Conceito — efeito mecânico do ano.** Quem já está no 3º ano e ainda não estagiou não pode mais "pretender estagiar antes do 3º ano". O ano entra no modelo principalmente como **controle** dessa restrição. A pergunta de interesse é se grupo, curso e objetivo acrescentam algo **dado o ano**.
```

- [ ] **Step 2: código da eliminação e do F conjunto**

```python
p7_data = analysis_sample(df, REGRESSION_COLUMNS)
print(f"n do modelo: {len(p7_data)}")
print("Proporção que pretende estagiar até o 3º ano, por ano na Poli:")
display(p7_data.groupby("ano_poli_grupo", observed=True)["estagio_ate_3ano"].agg(["mean", "size"]).round(2))

p7_steps, p7_final, p7_kept = backward_elimination(p7_data, "estagio_ate_3ano", REGRESSION_BLOCKS)
p7_steps.to_csv(TAB_DIR / "f3_tab20_p7_eliminacao_f_parcial.csv")
p7_steps
```

```python
p7_full = fit_ols(p7_data, "estagio_ate_3ano", REGRESSION_BLOCKS)
display(joint_partial_f_test(p7_full, p7_final, "Modelo completo vs. modelo final"))
print("Blocos mantidos:", p7_kept)
model_summary(p7_final)
```

- [ ] **Step 3: código dos coeficientes, dos cenários e dos resíduos**

```python
p7_coefficients = coefficient_table(p7_final, REGRESSION_LABELS)
p7_coefficients.to_csv(TAB_DIR / "f3_tab21_p7_coeficientes.csv")
p7_coefficients
```

```python
p7_scenarios = build_scenarios(df)
p7_predictions = predict_scenarios(p7_final, p7_scenarios)
p7_predictions.to_csv(TAB_DIR / "f3_tab22_p7_cenarios.csv")
plot_scenario_probabilities(p7_final, p7_scenarios, FIG_DIR / "f3_fig08_p7_cenarios.png")
p7_predictions
```

```python
plot_residual_diagnostics(p7_final, FIG_DIR / "f3_fig09_p7_residuos.png")
```

- [ ] **Step 4: executar e conferir**

Run: `cd notebooks && uv run --with nbconvert jupyter nbconvert --to notebook --execute --inplace 02_Carreira_Trajetoria_Objetivos.ipynb`
Expected:
- n = 179;
- ordem de saída: Objetivo, Tempo, Categoria (p ≈ 0,089), Horas (p ≈ 0,051);
- ficam Grande área (p ≈ 0,010) e Ano;
- R² ≈ 0,264;
- β(3º ano ou mais vs. 1º ano) ≈ −0,62;
- β(Mecânica, Mecatrônica & Naval vs. Civil & Ambiental) ≈ −0,23. O valor exato depende da categoria de referência; confira na tabela.

- [ ] **Step 5: escrever os itens (c), (d) e (e) da P7**

- Cite a ordem de eliminação, o F conjunto, o R² e os β em pontos percentuais.
- Destaque que a categoria do grupo **não** se mantém depois de controlar o ano e o curso (p ≈ 0,089), o que é coerente com a P3.
- Horas ficam no limite (p ≈ 0,051). Diga isso sem forçar a interpretação.
- Explique o efeito mecânico do ano.
- Comente a figura de resíduos à luz das limitações declaradas: duas faixas de pontos, o que é esperado com $Y$ 0/1.
- Diga se alguma previsão dos cenários saiu de [0, 100%].

- [ ] **Step 6: commit**

```bash
git add notebooks/02_Carreira_Trajetoria_Objetivos.ipynb output/tables/f3_tab2[0-2]_*.csv output/figures/f3_fig0[8-9]_*.png
git commit -m "Adiciona P7 da Frente 3 (modelo explicativo do estágio)"
```

---

### Task 9: síntese, resumo para o relatório, changelog e revisão de legibilidade

**Files:**
- Modify: `notebooks/02_Carreira_Trajetoria_Objetivos.ipynb` (seção final)
- Create: `output/f3_resumo_para_relatorio.md`
- Create: `.changelog/YYYYMMDD-frente-3-carreira.md`, com a data do dia da implementação

**Interfaces:**
- Consumes: os números finais impressos no notebook (Tasks 4 a 8).
- Produces: os textos finais.

- [ ] **Step 1: seção "## 9. Síntese da frente e limitações" no notebook**

Markdown com:
- **Síntese:** 4 a 6 itens, um por pergunta, cada um com o número principal;
- **Limitações:**
  - não há grupo de controle;
  - momento do estágio = intenção;
  - comparação entre turmas, não acompanhamento;
  - agrupamentos feitos para cumprir o critério do qui-quadrado;
  - modelo de probabilidade linear;
  - média ponderada aproximada pelo ponto médio das faixas;
  - n pequeno em Mercado Financeiro (34 alunos) e em Indefinido (20).

- [ ] **Step 2: escrever `output/f3_resumo_para_relatorio.md`**

Mesma estrutura de `output/f1_resumo_para_relatorio.md`:
1. título;
2. parágrafo de origem;
3. "Sugestão de montagem (~6 páginas)": tabela de página, conteúdo e `f3_` figura/tabela;
4. "4.3 Frente 3 — Carreira: trajetória e objetivos": objetivo, base e agrupamentos;
5. uma subseção por pergunta (P1, P2, P3, P4, P6, Modelo explicativo), cada uma com (a)–(e) resumidos;
6. "Síntese da frente";
7. "Limitações".

Os números são copiados do notebook executado, nunca da tabela de referência deste plano.

- [ ] **Step 3: escrever o changelog**

`.changelog/YYYYMMDD-frente-3-carreira.md`, no formato do `20261125-frente-1-metodos-da-disciplina.md`, com as seções Objetivo, O que foi feito, Decisões analíticas, Resultados e Pontos de atenção. Ele deve registrar:
- a nova geração do `clean_data.parquet` em 25/11:
  - `anos_de_poli` estava errado para 30 alunos;
  - mudaram só arredondamentos em `media_ponderada_num` (4,64 → 4,65; 9,42 → 9,41) e `horas_semanais_grupo_num` (70,37 → 70,36);
  - as outras frentes devem usar o arquivo novo, e a Frente 2 é afetada nas perguntas 5 e 7;
- todos os agrupamentos (a tabela `f3_tab02`) e as exclusões feitas em cada teste;
- as perguntas cortadas (P5 e P8) e o motivo;
- as funções novas em `stats_tests.py`;
- os resultados finais de cada pergunta.

- [ ] **Step 4: rodar os testes e o notebook do zero**

Run: `uv run --with pytest python -m pytest tests -q`
Expected: `11 passed`

Run: `cd notebooks && uv run --with nbconvert jupyter nbconvert --to notebook --execute --inplace 02_Carreira_Trajetoria_Objetivos.ipynb`
Expected: termina sem erro. Também `ls output/tables/f3_* | wc -l` = 22 e `ls output/figures/f3_* | wc -l` = 9.

- [ ] **Step 5: revisão de legibilidade**

Peça a um revisor independente (um subagente sem contexto, ou um colega do grupo) para ler o notebook **sem ler Python** e responder:
- dá para entender cada pergunta, o teste, o resultado e a conclusão só pelo texto, pelas tabelas e pelos gráficos?
- algum cabeçalho de tabela ou rótulo está em inglês ou é um nome de coluna cru?
- os números do texto batem com as tabelas impressas?

Corrija o que for apontado e execute de novo.

- [ ] **Step 6: commit**

```bash
git add notebooks/02_Carreira_Trajetoria_Objetivos.ipynb output/f3_resumo_para_relatorio.md .changelog/*-frente-3-carreira.md
git commit -m "Adiciona síntese, resumo para o relatório e changelog da Frente 3"
```
