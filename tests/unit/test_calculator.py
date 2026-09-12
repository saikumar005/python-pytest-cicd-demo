import pytest
from src.calculator import add, subtract, multiply, divide

# --- Task 2.2: Parametrized Tests ---
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),        # Positive numbers
        (-1, -5, -6),     # Negative numbers
        (-1, 1, 0),       # Negative + Positive
        (0, 0, 0),        # Zeroes
        (1.5, 2.5, 4.0),  # Floats
    ],
)
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 4, 12),
        (5, 0, 0),
        (-2, 3, -6),
        (-4, -2, 8),
    ],
)
def test_multiply_parametrized(a, b, expected):
    assert multiply(a, b) == expected

# --- Task 2.1: Pytest Fixtures ---
@pytest.fixture
def sample_numbers():
    """Fixture providing reusable test input data."""
    return {"a": 20, "b": 5}

def test_add_with_fixture(sample_numbers):
    result = add(sample_numbers["a"], sample_numbers["b"])
    assert result == 25

def test_divide_with_fixture(sample_numbers):
    result = divide(sample_numbers["a"], sample_numbers["b"])
    assert result == 4.0

# --- Standard AAA Tests ---
def test_subtract():
    assert subtract(10, 4) == 6

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
