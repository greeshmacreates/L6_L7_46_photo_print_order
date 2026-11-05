import pytest

from photo_print_order import (
    extra_print_charge,
    order_valid,
    dispatch_status
)


# ==========================================
# EXTRA PRINT CHARGE - BRANCH COVERAGE
# ==========================================

def test_invalid_size():
    with pytest.raises(ValueError):
        extra_print_charge("10x12", 20, "matte", False)


def test_valid_size():
    assert extra_print_charge("4x6", 10, "matte", False) == 0


def test_negative_copies():
    with pytest.raises(ValueError):
        extra_print_charge("4x6", -1, "matte", False)


def test_valid_copies():
    assert extra_print_charge("4x6", 10, "matte", False) == 0


def test_member_non_8x10():
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_non_member():
    assert extra_print_charge("4x6", 30, "matte", False) == 40


def test_member_8x10():
    assert extra_print_charge("8x10", 20, "matte", True) == 40


def test_no_extra_prints():
    assert extra_print_charge("4x6", 20, "matte", False) == 0


def test_matte_finish():
    assert extra_print_charge("4x6", 30, "matte", False) == 40


def test_other_finish():
    assert extra_print_charge("4x6", 30, "glossy", False) == 70


def test_more_than_50_extra_canvas():
    assert extra_print_charge("4x6", 80, "canvas", False) == 840


def test_more_than_50_extra_glossy():
    assert extra_print_charge("4x6", 80, "glossy", False) == 540


# ==========================================
# ORDER VALIDATION - BRANCH COVERAGE
# ==========================================

def test_rush_order_valid():
    assert order_valid(10, 50, True) is True


def test_rush_order_invalid():
    assert order_valid(10, 51, True) is False


def test_normal_order_valid():
    assert order_valid(10, 500, False) is True


def test_file_size_exceeded():
    assert order_valid(26, 100, False) is False


def test_normal_copy_limit_exceeded():
    assert order_valid(10, 501, False) is False


# ==========================================
# DISPATCH STATUS - BRANCH COVERAGE
# ==========================================

def test_framed_order():
    assert dispatch_status(24, True, False) == "on_time"


def test_unframed_order():
    assert dispatch_status(12, False, False) == "on_time"


def test_international_order():
    assert dispatch_status(36, False, True) == "on_time"


def test_domestic_order():
    assert dispatch_status(12, False, False) == "on_time"


def test_on_time_status():
    assert dispatch_status(24, True, False) == "on_time"


def test_tight_status():
    assert dispatch_status(20, True, False) == "tight"


def test_missed_status():
    assert dispatch_status(17, True, False) == "missed"


def test_international_tight():
    assert dispatch_status(30, False, True) == "tight"


def test_international_missed():
    assert dispatch_status(29, False, True) == "missed"
