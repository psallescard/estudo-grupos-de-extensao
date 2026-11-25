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
