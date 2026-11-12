
import pytest
from hypothesis import given, settings, strategies as st

from photo_print_order import parse_order, file_size_average, payable_amount


TEXT = st.text(max_size=60)


# PARSE ORDER TESTS

@given(
    size=st.text(
        alphabet=st.characters(
            blacklist_characters=":",
            blacklist_categories=("Cs",)
        ),
        max_size=25
    ),
    copies=st.integers()
)
@settings(max_examples=150)
def test_parse_order_valid(size, copies):
    result_size, result_copies = parse_order(f" {size} : {copies} ")

    assert result_size == size.strip().upper()
    assert result_copies == copies


@given(text=TEXT.filter(lambda x: ":" not in x))
@settings(max_examples=100)
def test_parse_order_missing_separator(text):
    with pytest.raises(ValueError):
        parse_order(text)


@given(size=st.text(max_size=20))
@settings(max_examples=100)
def test_parse_order_invalid_copies(size):
    with pytest.raises(ValueError):
        parse_order(f"{size}:abc")


# FILE SIZE AVERAGE TESTS

@given(values=st.lists(st.integers(), min_size=1, max_size=30))
@settings(max_examples=150)
def test_file_size_average_valid(values):
    csv_text = ",".join(map(str, values))

    assert file_size_average(csv_text) == sum(values) // len(values)


@given(value=st.integers())
def test_file_size_average_single_value(value):
    assert file_size_average(str(value)) == value


@given(text=st.sampled_from(["", " ", ",", "1,,2", "one,2", "1,2.5"]))
def test_file_size_average_invalid(text):
    with pytest.raises((ValueError, ZeroDivisionError)):
        file_size_average(text)


# PAYABLE AMOUNT TESTS

@given(
    amount=st.floats(
        allow_nan=False,
        allow_infinity=False,
        min_value=-100000,
        max_value=100000
    ),
    discount=st.floats(
        allow_nan=False,
        allow_infinity=False,
        min_value=-100000,
        max_value=100000
    )
)
@settings(max_examples=150)
def test_payable_amount_valid(amount, discount):
    expected = max(amount * 1.18 - discount, 0)

    assert payable_amount(
        f"{amount}|{discount}"
    ) == pytest.approx(expected)


@given(text=TEXT.filter(lambda x: "|" not in x))
@settings(max_examples=100)
def test_payable_amount_missing_separator(text):
    with pytest.raises(ValueError):
        payable_amount(text)


@given(discount=st.integers())
def test_payable_amount_invalid_amount(discount):
    with pytest.raises(ValueError):
        payable_amount(f"abc|{discount}")


@given(amount=st.integers())
def test_payable_amount_invalid_discount(amount):
    with pytest.raises(ValueError):
        payable_amount(f"{amount}|abc")

@given(amount=st.integers(min_value=-10000, max_value=10000))
def test_payable_amount_zero_floor(amount):
    assert payable_amount(f"{amount}|1000000") == 0
