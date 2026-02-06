"""
Basic tests for CI/CD
"""

def test_always_passes():
    """Basic test that always passes."""
    assert True


def test_imports():
    """Test that core imports work."""
    try:
        import numpy
        import pandas
        assert True
    except ImportError:
        assert False, "Failed to import numpy or pandas"
