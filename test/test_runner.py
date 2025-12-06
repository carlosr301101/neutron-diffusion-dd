"""Unit tests for Runner class in core.algoritm module."""
import numpy as np
import pytest
from core.algoritm import Config, Runner


def test_runner_initialization():
    """Test basic Runner initialization."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [10],
        "HR": [10.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.9],
        "Q": [1.0],
        "N": 2,
        "bound_left": [0.0],  # Required for non-reflective boundaries
        "bound_right": [0.0],  # Required for non-reflective boundaries
    }
    
    config = Config(manual=False, **config_dict)
    runner = Runner(config)
    
    assert runner.config == config
    assert runner.iteration == 0
    assert runner.converged == False
    assert runner.PSI_RIGHT.shape == (11, 1)  # (NTP, N_HALF)
    assert runner.PSI_LEFT.shape == (11, 1)   # (NTP, N_HALF)
    assert runner.scalar_flux.shape == (10,)  # NTC
    assert runner.total_source.shape == (10,) # NTC


def test_runner_with_reflective_boundaries():
    """Test Runner initialization with reflective boundaries."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [10],
        "HR": [10.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.9],
        "Q": [1.0],
        "N": 2,
        "reflex_izq": True,
        "reflex_der": False
    }
    
    config = Config(manual=False, **config_dict)
    runner = Runner(config)
    
    assert runner.reflex_izq == True
    assert runner.reflex_der == False


def test_runner_sweep_basic():
    """Test basic sweep functionality."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [2],  # 2 celdas
        "HR": [2.0],  # 2cm total
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.0],  # No scattering
        "Q": [1.0],
        "N": 2,  # S2
        "bound_left": [0.0],  # Required for non-reflective boundaries
        "bound_right": [0.0],  # Required for non-reflective boundaries
    }
    
    config = Config(manual=False, **config_dict)
    runner = Runner(config)
    
    # Initialize with some values
    runner.PSI_RIGHT[0, 0] = 1.0  # Left boundary incoming
    runner.PSI_LEFT[-1, 0] = 0.0  # Right boundary incoming
    
    # Run one sweep
    runner.sweep()
    
    # Check that values have been propagated
    # PSI_RIGHT should have values > 0 after sweep
    assert runner.PSI_RIGHT[1, 0] > 0  # First cell right exit
    assert runner.PSI_RIGHT[2, 0] > 0  # Second cell right exit
    
    # PSI_LEFT should have values (after left sweep)
    assert runner.PSI_LEFT[0, 0] >= 0  # First cell left exit
    assert runner.PSI_LEFT[1, 0] >= 0  # Second to last cell left exit


def test_calculo_flujo():
    """Test scalar flux calculation."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [2],
        "HR": [2.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.0],
        "Q": [1.0],
        "N": 2,
        "bound_left": [0.0],  # Required for non-reflective boundaries
        "bound_right": [0.0],  # Required for non-reflective boundaries
    }
    
    config = Config(manual=False, **config_dict)
    runner = Runner(config)
    
    # Set some test values for angular fluxes
    runner.PSI_RIGHT[:, 0] = 1.0  # All right-going fluxes = 1.0
    runner.PSI_LEFT[:, 0] = 0.5   # All left-going fluxes = 0.5
    
    # Calculate scalar flux
    old_flux = runner.calculo_flujo()
    
    # Scalar flux should be calculated as weighted sum of angular fluxes
    # With S2: 1 angular direction with weight 1.0
    # psi_avg_der = 0.5 * (PSI_RIGHT[k] + PSI_RIGHT[k+1])
    # psi_avg_izq = 0.5 * (PSI_LEFT[k] + PSI_LEFT[k+1])
    # scalar_flux[k] = weight * (psi_avg_der + psi_avg_izq)
    
    # For cell 0: psi_avg_der = 0.5*(1.0 + 1.0) = 1.0, psi_avg_izq = 0.5*(0.5 + 0.5) = 0.5
    # scalar_flux[0] = 1.0 * (1.0 + 0.5) = 1.5
    expected_value = 1.0 * (0.5 * (1.0 + 1.0) + 0.5 * (0.5 + 0.5))  # = 1.5
    assert runner.scalar_flux[0] == expected_value


def test_check_convergence():
    """Test convergence checking."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [5],
        "HR": [5.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.0],
        "Q": [1.0],
        "N": 2,
        "bound_left": [0.0],  # Required for non-reflective boundaries
        "bound_right": [0.0],  # Required for non-reflective boundaries
    }
    
    config = Config(manual=False, **config_dict)
    runner = Runner(config)
    
    # Set initial flux
    runner.scalar_flux = np.ones(5)
    
    # Test convergence when flux doesn't change
    old_flux = np.ones(5)
    is_converged = runner.check_convergence(old_flux)
    assert is_converged == True  # Same flux means converged
    
    # Test convergence when flux changes significantly
    old_flux = np.zeros(5)
    is_converged = runner.check_convergence(old_flux)
    assert is_converged == False  # Different flux means not converged


def test_update_reflective_boundaries():
    """Test reflective boundary updates."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [5],
        "HR": [5.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.0],
        "Q": [1.0],
        "N": 2,
        "reflex_izq": True,
        "reflex_der": True
    }
    
    config = Config(manual=False, **config_dict)
    runner = Runner(config)
    
    # Set some test values
    runner.PSI_LEFT[0, 0] = 0.8  # What goes out left boundary
    runner.PSI_RIGHT[-1, 0] = 0.6  # What goes out right boundary
    
    # Update reflective boundaries
    runner.update_reflective_boundaries_left()
    runner.update_reflective_boundaries_right()
    
    # After reflection: what goes out should come back in
    # Left: what goes out left (PSI_LEFT[0]) should become right-going at left boundary
    assert runner.PSI_RIGHT[0, 0] == 0.8
    
    # Right: what goes out right (PSI_RIGHT[-1]) should become left-going at right boundary
    assert runner.PSI_LEFT[-1, 0] == 0.6


def test_runner_call_basic():
    """Test the full runner call (iteration loop)."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [3],
        "HR": [3.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.0],
        "Q": [0.0],
        "N": 2,
        "epsilon": 1e-3,  # Larger epsilon for faster convergence
        "max_iter": 10,
    }
    
    config = Config(manual=False, **config_dict)
    runner = Runner(config)
    
    # Run the full calculation
    result = runner()
    
    # Check that result has expected structure
    assert "scalar_flux" in result
    assert "iteration" in result
    assert "PSI_RIGHT" in result
    assert "PSI_LEFT" in result
    assert "converged" in result
    assert "dataframe" in result
    
    # Check shapes
    assert result["scalar_flux"].shape == (3,)  # 3 cells
    assert result["PSI_RIGHT"].shape == (4, 1)  # (4 nodes, 1 direction)
    assert result["PSI_LEFT"].shape == (4, 1)   # (4 nodes, 1 direction)
    
    # Check that iteration count is reasonable
    assert 0 < result["iteration"] <= config.max_iter


def test_calculo_fugas():
    """Test leakage calculation."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [5],
        "HR": [5.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.0],
        "Q": [0.0],
        "N": 2,
    }
    
    config = Config(manual=False, **config_dict)
    runner = Runner(config)
    
    # Set test values for angular fluxes at boundaries
    runner.PSI_LEFT[0, :] = 0.5  # Left boundary outgoing
    runner.PSI_RIGHT[-1, :] = 0.3  # Right boundary outgoing
    
    # Test different leakage calculation modes
    left_leak, right_leak = runner.calculo_fugas(0)  # Only left
    assert right_leak == 0.0
    assert left_leak >= 0.0  # Should be positive
    
    left_leak, right_leak = runner.calculo_fugas(1)  # Only right
    assert left_leak == 0.0
    assert right_leak >= 0.0  # Should be positive
    
    left_leak, right_leak = runner.calculo_fugas(2)  # Both
    assert left_leak >= 0.0 and right_leak >= 0.0


def test_runner_with_boundary_conditions():
    """Test runner with specified boundary conditions."""
    config_dict = {
        "num_regions": 1,
        "num_zones": 1,
        "NC": [5],
        "HR": [5.0],
        "IZL": [1],
        "SCT": [1.0],
        "SCS": [0.0],
        "Q": [0.0],
        "N": 4,  # S4 - 2 directions
        "bound_left": [0.1, 0.2],
        "bound_right": [0.3, 0.4],
        "reflex_izq": False,
        "reflex_der": False
    }
    
    config = Config(manual=False, **config_dict)
    runner = Runner(config)
    
    # Check that boundary conditions were set properly
    assert runner.PSI_RIGHT[0, 0] == 0.1
    assert runner.PSI_RIGHT[0, 1] == 0.2
    assert runner.PSI_LEFT[-1, 0] == 0.3
    assert runner.PSI_LEFT[-1, 1] == 0.4