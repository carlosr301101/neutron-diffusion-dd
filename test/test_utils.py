"""Unit tests for utils module."""

import numpy as np
from core.utils import func_analitica, calcular_desvios_relativos


def test_func_analitica():
    """Test the analytical function."""
    # Test at x = 0
    result = func_analitica(0)
    expected = 1.705 * 1  # exp(0) = 1
    assert abs(result - expected) < 1e-10

    # Test at x = 1
    result = func_analitica(1)
    expected = 1.705 * 0.7408182206817179  # exp(-0.3)
    assert abs(result - expected) < 1e-10

    # Test at x = 5
    result = func_analitica(5)
    expected = 1.705 * 0.22313016014842982  # exp(-1.5)
    assert abs(result - expected) < 1e-10


def test_calcular_desvios_relativos():
    """Test relative deviation calculation."""
    # Test with simple arrays
    numeric = np.array([1.0, 2.0, 3.0])
    analytic = np.array([1.0, 2.0, 3.0])

    deviations = calcular_desvios_relativos(numeric, analytic)

    # When values are identical, deviations should be 0
    expected = np.array([0.0, 0.0, 0.0])
    np.testing.assert_array_almost_equal(deviations, expected)

    # Test with different values
    numeric = np.array([1.1, 2.1, 3.1])
    analytic = np.array([1.0, 2.0, 3.0])

    deviations = calcular_desvios_relativos(numeric, analytic)

    # Expected: abs((1.1-1.0)/1.0)*100 = 10%, etc.
    expected = np.array([10.0, 5.0, 3.33333333])
    np.testing.assert_array_almost_equal(deviations, expected, decimal=5)


def test_calcular_desvios_relativos_zero_analytical():
    """Test relative deviation calculation with zero analytical values."""
    # Test with zero analytical values (should not cause division by zero)
    numeric = np.array([1.0, 2.0, 0.1])
    analytic = np.array([0.0, 0.0, 0.0])

    deviations = calcular_desvios_relativos(numeric, analytic)

    # Should not be infinite due to the small value added to denominator
    assert not np.any(np.isinf(deviations))
    assert not np.any(np.isnan(deviations))

    # Values should be large but finite
    assert np.all(deviations >= 0)  # All deviations should be non-negative


def test_calcular_desvios_relativos_negative_values():
    """Test relative deviation calculation with negative values."""
    numeric = np.array([-1.0, -2.0, -3.0])
    analytic = np.array([-1.1, -2.1, -3.1])

    deviations = calcular_desvios_relativos(numeric, analytic)

    # Should work with negative values
    assert len(deviations) == 3
    assert np.all(deviations >= 0)  # Deviations should always be non-negative


def test_calcular_desvios_relativos_mixed_signs():
    """Test relative deviation calculation with mixed sign values."""
    numeric = np.array([1.0, -1.0, 0.0])
    analytic = np.array([-1.0, 1.0, 0.01])  # Last value is small but not zero

    deviations = calcular_desvios_relativos(numeric, analytic)

    # Should handle mixed signs properly
    assert len(deviations) == 3
    assert np.all(deviations >= 0)  # Deviations should always be non-negative
