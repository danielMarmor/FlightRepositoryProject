import pytest


def capital_case(word):
    return word.capitalize()


@pytest.mark.set1
def test_positive_flow():
    is_capital_case = capital_case('hello') == 'Hello'
    assert is_capital_case


@pytest.mark.set1
def test_negative_flow():
    with pytest.raises(TypeError):
        capital_case()



