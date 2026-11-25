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
