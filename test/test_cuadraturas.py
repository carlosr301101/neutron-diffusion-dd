"""Unit tests for cuadraturas module."""
import numpy as np
import pandas as pd
from core.cuadraturas import DATA


def test_cuadraturas_data_structure():
    """Test that the DATA structure has the expected format."""
    assert isinstance(DATA, dict)
    assert "N" in DATA
    assert "m" in DATA
    assert "mu_m" in DATA
    assert "omega_m" in DATA
    
    # Check that all arrays have the same length
    n_len = len(DATA["N"])
    m_len = len(DATA["m"])
    mu_len = len(DATA["mu_m"])
    omega_len = len(DATA["omega_m"])
    
    assert n_len == m_len == mu_len == omega_len


def test_cuadraturas_values():
    """Test that cuadraturas values are reasonable."""
    # Check that mu_m values are between 0 and 1 (direction cosines)
    for mu in DATA["mu_m"]:
        assert 0 < mu <= 1.0
    
    # Check that omega_m values are positive
    for omega in DATA["omega_m"]:
        assert omega > 0.0
    
    # Check that N values are even numbers (as required by the algorithm)
    for n in DATA["N"]:
        assert n % 2 == 0


def test_cuadraturas_ordering():
    """Test that cuadraturas data is properly organized by N."""
    df = pd.DataFrame(DATA)
    
    # Group by N and verify that each group has the expected number of directions
    for n_val in df["N"].unique():
        subset = df[df["N"] == n_val]
        # For order N, we expect N/2 directions (half angles)
        expected_dirs = n_val // 2
        assert len(subset) == expected_dirs, f"N={n_val} should have {expected_dirs} directions, got {len(subset)}"


def test_specific_cuadrature_values():
    """Test specific known cuadrature values."""
    df = pd.DataFrame(DATA)
    
    # Test S2 values (N=2)
    s2_data = df[df["N"] == 2]
    assert len(s2_data) == 1  # S2 should have 1 direction
    assert abs(s2_data.iloc[0]["mu_m"] - 0.577350269189626) < 1e-10
    assert abs(s2_data.iloc[0]["omega_m"] - 1.0) < 1e-10
    
    # Test S4 values (N=4)
    s4_data = df[df["N"] == 4]
    assert len(s4_data) == 2  # S4 should have 2 directions
    expected_mu_vals = [0.861136311594053, 0.339981043584856]
    expected_omega_vals = [0.347854845137454, 0.652145154862546]
    
    for i, row in s4_data.iterrows():
        # Check that the values match expected ones (order might vary)
        assert any(abs(row["mu_m"] - mu) < 1e-10 for mu in expected_mu_vals)
        assert any(abs(row["omega_m"] - omega) < 1e-10 for omega in expected_omega_vals)


def test_dataframe_creation():
    """Test that DATA can be converted to a proper DataFrame."""
    df = pd.DataFrame(DATA)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) == 4  # N, m, mu_m, omega_m
    assert len(df) > 0  # Should have some data
    assert list(df.columns) == ["N", "m", "mu_m", "omega_m"]
    
    # Check data types
    assert df["N"].dtype in [np.int64, np.int32, int]
    assert df["m"].dtype in [np.int64, np.int32, int]
    assert df["mu_m"].dtype in [np.float64, np.float32, float]
    assert df["omega_m"].dtype in [np.float64, np.float32, float]