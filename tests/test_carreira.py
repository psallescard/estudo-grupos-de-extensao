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
