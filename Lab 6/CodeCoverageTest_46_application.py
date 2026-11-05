import pytest

from photo_print_order import (
    extra_print_charge,
    order_valid,
    dispatch_status
)


# ==========================================
# EXTRA PRINT CHARGE TESTS
# ==========================================

def test_unknown_print_size():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("10x12", 30, "matte", False)


def test_negative_copies():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -5, "matte", False)


def test_within_included_prints():
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_exactly_included_prints():
    assert extra_print_charge("4x6", 20, "matte", False) == 0


def test_member_extra_prints():
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_member_8x10():
    assert extra_print_charge("8x10", 20, "matte", True) == 40


def test_non_member_extra_prints():
    assert extra_print_charge("4x6", 30, "matte", False) == 40


def test_glossy_finish():
    assert extra_print_charge("5x7", 20, "glossy", False) == 35


def test_large_canvas_order():
    assert extra_print_charge("4x6", 80, "canvas", False) == 840


def test_large_glossy_order():
    assert extra_print_charge("4x6", 80, "glossy", False) == 540


# ==========================================
# ORDER VALIDATION TESTS
# ==========================================

def test_valid_rush_order():
    assert order_valid(10, 40, True) is True


def test_invalid_rush_order():
    assert order_valid(10, 60, True) is False


def test_file_size_exceeds_limit():
    assert order_valid(30, 100, False) is False


def test_valid_normal_order():
    assert order_valid(10, 300, False) is True


def test_maximum_normal_copies():
    assert order_valid(25, 500, False) is True


def test_excessive_normal_copies():
    assert order_valid(10, 600, False) is False


# ==========================================
# DISPATCH STATUS TESTS
# ==========================================

def test_framed_on_time():
    assert dispatch_status(24, True, False) == "on_time"


def test_framed_tight():
    assert dispatch_status(20, True, False) == "tight"


def test_framed_missed():
    assert dispatch_status(17, True, False) == "missed"


def test_unframed_on_time():
    assert dispatch_status(12, False, False) == "on_time"


def test_international_on_time():
    assert dispatch_status(36, False, True) == "on_time"


def test_international_tight():
    assert dispatch_status(30, False, True) == "tight"


def test_international_missed():
    assert dispatch_status(29, False, True) == "missed"
