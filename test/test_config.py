"""Unit tests for Config class in core.algoritm module."""

import numpy as np
import pytest
from core.algoritm import Config


def test_config_manual_initialization():
    """Test Config initialization with manual input mode (mocked)."""
    # Since manual input requires user input, we'll test with auto_input instead
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [100],  # 100 celdas en región 1
        "HR": [100.0],  # Espesor de 100 cm
        "IZL": [1],  # Región 1 usa zona 1
        "SCT": [1.0],  # Sigma total = 1.0
        "SCS": [0.97],  # Sigma scattering = 0.97
        "Q": [1.0],  # Fuente = 1.0
        "N": 2,  # Orden S2
        "bound_left": [0.0],  # Required for non-reflective boundaries
        "bound_right": [0.0],  # Required for non-reflective boundaries
    }

    config = Config(manual=False, **config_dict)

    assert config.num_regions == 1
    assert config.num_zones == 1
    assert config.N == 2
    assert config.N_HALF == 1
    assert len(config.NC) == 1
    assert len(config.HR) == 1
    assert len(config.IZL) == 1
    assert len(config.SCT) == 1
    assert len(config.SCS) == 1
    assert len(config.Q) == 1
    assert config.NTC == 100  # Total celdas
    assert config.NTP == 101  # Total nodos (celdas + 1)


def test_config_auto_input_basic():
    """Test basic auto_input functionality."""
    config_dict = {
        "num_regions": 2,
        "num_zones": 2,
        "NC": [50, 30],  # 50 celdas en región 1, 30 en región 2
        "HR": [50.0, 30.0],  # Espesores
        "IZL": [1, 2],  # Región 1 usa zona 1, región 2 usa zona 2
        "SCT": [1.0, 0.8],  # Sigma total por zona
        "SCS": [0.9, 0.7],  # Sigma scattering por zona
        "Q": [1.0, 0.5],  # Fuentes por región
        "N": 4,  # Orden S4
        "bound_left": [
            0.0,
            0.0,
        ],  # Required for non-reflective boundaries (2 directions for S4)
        "bound_right": [
            0.0,
            0.0,
        ],  # Required for non-reflective boundaries (2 directions for S4)
    }

    config = Config(manual=False, **config_dict)

    assert config.num_regions == 2
    assert config.num_zones == 2
    assert config.N == 4
    assert config.N_HALF == 2
    np.testing.assert_array_equal(config.NC, [50, 30])
    np.testing.assert_array_equal(config.HR, [50.0, 30.0])
    np.testing.assert_array_equal(config.IZL, [1, 2])
    np.testing.assert_array_equal(config.SCT, [1.0, 0.8])
    np.testing.assert_array_equal(config.SCS, [0.9, 0.7])
    np.testing.assert_array_equal(config.Q, [1.0, 0.5])


def test_config_missing_required_fields():
    """Test that auto_input raises error when required fields are missing."""
    # Missing NC field
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "HR": [100.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.97],
        "Q": [1.0],
        "N": 2,
    }

    with pytest.raises(ValueError, match="Campo obligatorio ausente: 'NC'"):
        Config(manual=False, **config_dict)


def test_config_invalid_zone_count():
    """Test that auto_input raises error when number of zones > regions."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 2,  # More zones than regions
        "NC": [100],
        "HR": [100.0],
        "IZL": [1],
        "SCT": [1.0, 0.8],  # Need 2 zones
        "SCS": [0.9, 0.7],  # Need 2 zones
        "Q": [1.0],
        "N": 2,
    }

    with pytest.raises(
        ValueError, match="Número de zonas no puede ser mayor que el número de regiones"
    ):
        Config(manual=False, **config_dict)


def test_config_odd_quadrature_order():
    """Test that auto_input raises error when quadrature order is odd."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [100],
        "HR": [100.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.97],
        "Q": [1.0],
        "N": 3,  # Odd number
    }

    with pytest.raises(
        ValueError, match="El orden de la cuadratura debe ser un número par"
    ):
        Config(manual=False, **config_dict)


def test_config_dimension_validation():
    """Test dimension validation for arrays."""
    # NC array has wrong length
    config_dict = {
        "num_regions": 2,  # Expecting 2 elements
        "num_zones": 1,
        "NC": [100],  # Only 1 element provided
        "HR": [100.0, 50.0],
        "IZL": [1, 1],
        "SCT": [1.0],
        "SCS": [0.97],
        "Q": [1.0, 0.5],
        "N": 2,
    }

    with pytest.raises(ValueError, match="NC debe tener 2 elementos"):
        Config(manual=False, **config_dict)


def test_config_zone_index_validation():
    """Test validation of zone indices."""
    config_dict = {
        "num_regions": 2,
        "num_zones": 2,
        "NC": [50, 30],
        "HR": [50.0, 30.0],
        "IZL": [1, 3],  # Zone 3 doesn't exist (max is 2)
        "SCT": [1.0, 0.8],
        "SCS": [0.9, 0.7],
        "Q": [1.0, 0.5],
        "N": 4,
        "bound_left": [0.0, 0.0],  # Required for non-reflective boundaries
        "bound_right": [0.0, 0.0],  # Required for non-reflective boundaries
    }

    with pytest.raises(ValueError, match="IZL debe contener valores entre 1 y 2"):
        Config(manual=False, **config_dict)


def test_config_weights_directions():
    """Test that weights and directions are loaded correctly."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [100],
        "HR": [100.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.97],
        "Q": [1.0],
        "N": 2,  # S2
        "bound_left": [0.0],  # Required for non-reflective boundaries
        "bound_right": [0.0],  # Required for non-reflective boundaries
    }

    config = Config(manual=False, **config_dict)

    # For S2, should have 1 direction and weight
    assert len(config.miu_m) == 1
    assert len(config.omega_m) == 1
    assert config.miu_m[0] == 0.577350269189626
    assert config.omega_m[0] == 1.0


def test_config_vectorization():
    """Test that properties are correctly vectorized per cell."""
    config_dict = {
        "num_regions": 2,
        "num_zones": 2,
        "NC": [2, 3],  # 2 celdas en región 1, 3 en región 2
        "HR": [10.0, 15.0],  # Espesores
        "IZL": [1, 2],  # Región 1 usa zona 1, región 2 usa zona 2
        "SCT": [1.0, 0.8],  # Sigma total por zona
        "SCS": [0.9, 0.7],  # Sigma scattering por zona
        "Q": [1.0, 0.5],  # Fuentes por región
        "N": 2,
        "bound_left": [0.0],  # Required for non-reflective boundaries
        "bound_right": [0.0],  # Required for non-reflective boundaries
    }

    config = Config(manual=False, **config_dict)

    # Should have 5 total cells (2 + 3)
    assert config.NTC == 5
    assert config.NTP == 6

    # Check that vectorized properties are correct
    # First 2 cells should have properties of zone 1, last 3 of zone 2
    expected_sigma_t = np.array([1.0, 1.0, 0.8, 0.8, 0.8])  # From zones 1,1,2,2,2
    expected_sigma_s = np.array([0.9, 0.9, 0.7, 0.7, 0.7])  # From zones 1,1,2,2,2
    expected_q_ext = np.array([1.0, 1.0, 0.5, 0.5, 0.5])  # From regions 1,1,2,2,2

    np.testing.assert_array_almost_equal(config.sigma_t_vec, expected_sigma_t)
    np.testing.assert_array_almost_equal(config.sigma_s_vec, expected_sigma_s)
    np.testing.assert_array_almost_equal(config.q_ext_vec, expected_q_ext)

    # Check dx values (HR[i]/NC[i])
    expected_dx = np.array(
        [5.0, 5.0, 5.0, 5.0, 5.0]
    )  # 10/2=5 for first 2, 15/3=5 for next 3
    np.testing.assert_array_almost_equal(config.dx_vec, expected_dx)


def test_config_with_boundary_conditions():
    """Test Config with boundary conditions."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [100],
        "HR": [100.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.97],
        "Q": [1.0],
        "N": 4,  # S4 has 2 half directions
        "bound_left": [0.1, 0.2],
        "bound_right": [0.3, 0.4],
        "reflex_izq": False,
        "reflex_der": False,
    }

    config = Config(manual=False, **config_dict)

    np.testing.assert_array_equal(config.bound_left, [0.1, 0.2])
    np.testing.assert_array_equal(config.bound_right, [0.3, 0.4])
    assert config.reflex_izq == False
    assert config.reflex_der == False


def test_config_reflective_boundaries():
    """Test Config with reflective boundaries."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [100],
        "HR": [100.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.97],
        "Q": [1.0],
        "N": 2,
        "reflex_izq": True,
        "reflex_der": True,
        "bound_left": [0.0],  # Still need to provide bounds even for reflective
        "bound_right": [0.0],
    }

    config = Config(manual=False, **config_dict)

    assert config.reflex_izq
    assert config.reflex_der
