import pytest


def add(x: int, y: int) -> int:
    return x + y


@pytest.mark.parametrize(("a", "b", "result"), [(1, 2, 3), (3, 4, 7)])
def test_add_params(a: int, b: int, result: int) -> None:
    assert add(a, b) == result
