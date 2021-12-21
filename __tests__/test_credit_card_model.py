from datetime import date

import pytest
from pydantic import ValidationError

from app.helpers import CreditCardBrand
from app.models import CreditCard


def test_model_instance():
    cc = CreditCard(
        name="Test",
        number="4242424242424242",
        month="01",
        year=str(date.today().year),
        cvv="000",
    )
    assert isinstance(cc, CreditCard)


def test_model_no_inputs():
    with pytest.raises(ValidationError):
        CreditCard()


def test_model_cardholder_name_too_short():
    with pytest.raises(ValidationError):
        CreditCard(
            name="T",
            number="4242424242424242",
            month="01",
            year=str(date.today().year),
            cvv="000",
        )


def test_model_has_number_in_cardholder_name():
    with pytest.raises(ValidationError):
        CreditCard(
            name="T2",
            number="4242424242424242",
            month="01",
            year=str(date.today().year),
            cvv="000",
        )


def test_model_cardholder_number_has_fifteen_digits():
    with pytest.raises(ValidationError):
        CreditCard(
            name="Test",
            number="424242424242424",
            month="01",
            year=str(date.today().year),
            cvv="000",
        )


def test_model_cardholder_number_has_sixteen_digits():
    cc = CreditCard(
        name="Test",
        number="4242424242424242",
        month="01",
        year=str(date.today().year),
        cvv="123",
    )
    assert cc.name == "Test"
    assert cc.number == "4242424242424242"
    assert cc.month == "01"
    assert cc.year == str(date.today().year)
    assert cc.cvv == "123"
    assert cc.brand == CreditCardBrand.VISA


def test_model_cardholder_number_has_seventeen_digits():
    with pytest.raises(ValidationError):
        CreditCard(
            name="Test",
            number="42424242424242424",
            month="01",
            year=str(date.today().year),
            cvv="000",
        )


def test_model_cardholder_number_is_visa():
    test_numbers = [
        "4242424242424242",
        "4000056655665556",
        "4012888888881881",
    ]
    for num in test_numbers:
        cc = CreditCard(
            name="Test",
            number=num,
            month="01",
            year=str(date.today().year),
            cvv="123",
        )
        assert cc.name == "Test"
        assert cc.number == num
        assert cc.month == "01"
        assert cc.year == str(date.today().year)
        assert cc.cvv == "123"
        assert cc.brand == CreditCardBrand.VISA


def test_model_cardholder_number_is_discover():
    test_numbers = [
        "6011111111111117",
        "6011000990139424",
        "6011000990139424",
    ]
    for num in test_numbers:
        cc = CreditCard(
            name="Test",
            number=num,
            month="01",
            year=str(date.today().year),
            cvv="123",
        )
        assert cc.name == "Test"
        assert cc.number == num
        assert cc.month == "01"
        assert cc.year == str(date.today().year)
        assert cc.cvv == "123"
        assert cc.brand == CreditCardBrand.DISCOVER


def test_model_cardholder_number_is_mastercard():
    test_numbers = [
        "5555555555554444",
        "2223003122003222",
        "5200828282828210",
        "5105105105105100",
    ]
    for num in test_numbers:
        cc = CreditCard(
            name="Test",
            number=num,
            month="01",
            year=str(date.today().year),
            cvv="123",
        )
        assert cc.name == "Test"
        assert cc.number == num
        assert cc.month == "01"
        assert cc.year == str(date.today().year)
        assert cc.cvv == "123"
        assert cc.brand == CreditCardBrand.MASTERCARD


def test_model_cardholder_number_is_american_express():
    test_numbers = [
        "378282246310005",
        "371449635398431",
        "371449635398431",
    ]
    for num in test_numbers:
        cc = CreditCard(
            name="Test",
            number=num,
            month="01",
            year=str(date.today().year),
            cvv="123",
        )
        assert cc.name == "Test"
        assert cc.number == num
        assert cc.month == "01"
        assert cc.year == str(date.today().year)
        assert cc.cvv == "123"
        assert cc.brand == CreditCardBrand.AMERICAN_EXPRESS


def test_model_cardholder_number_is_invalid_card():
    with pytest.raises(ValidationError):
        test_numbers = [
            "38520000023237",  # Diners Club
            "3056930009020004",  # Diners Club
            "36227206271667",  # Diners Club (14 digit)
            "3566002020360505",  # JCB
            "3566002020360505",  # JCB
            "6200000000000005",  # UnionPay
        ]
        for num in test_numbers:
            CreditCard(
                name="Test",
                number=num,
                month="01",
                year=str(date.today().year),
                cvv="123",
            )


def test_model_expiry_month_below_min_limit():
    with pytest.raises(ValidationError):
        CreditCard(
            name="Test",
            number="4242424242424242",
            month="00",
            year=str(date.today().year),
            cvv="000",
        )


def test_model_expiry_month_at_min_limit():
    cc = CreditCard(
        name="Test",
        number="4242424242424242",
        month="01",
        year=str(date.today().year),
        cvv="123",
    )
    assert cc.name == "Test"
    assert cc.number == "4242424242424242"
    assert cc.month == "01"
    assert cc.year == str(date.today().year)
    assert cc.cvv == "123"
    assert cc.brand == CreditCardBrand.VISA


def test_model_expiry_month_above_min_limit():
    cc = CreditCard(
        name="Test",
        number="4242424242424242",
        month="02",
        year=str(date.today().year),
        cvv="123",
    )
    assert cc.name == "Test"
    assert cc.number == "4242424242424242"
    assert cc.month == "02"
    assert cc.year == str(date.today().year)
    assert cc.cvv == "123"
    assert cc.brand == CreditCardBrand.VISA


def test_model_expiry_month_below_max_limit():
    cc = CreditCard(
        name="Test",
        number="4242424242424242",
        month="11",
        year=str(date.today().year),
        cvv="123",
    )
    assert cc.name == "Test"
    assert cc.number == "4242424242424242"
    assert cc.month == "11"
    assert cc.year == str(date.today().year)
    assert cc.cvv == "123"
    assert cc.brand == CreditCardBrand.VISA


def test_model_expiry_month_at_max_limit():
    cc = CreditCard(
        name="Test",
        number="4242424242424242",
        month="12",
        year=str(date.today().year),
        cvv="123",
    )
    assert cc.name == "Test"
    assert cc.number == "4242424242424242"
    assert cc.month == "12"
    assert cc.year == str(date.today().year)
    assert cc.cvv == "123"
    assert cc.brand == CreditCardBrand.VISA


def test_model_expiry_month_above_max_limit():
    with pytest.raises(ValidationError):
        CreditCard(
            name="Test",
            number="4242424242424242",
            month="13",
            year=str(date.today().year),
            cvv="000",
        )


def test_model_expiry_year_previous_year():
    with pytest.raises(ValidationError):
        CreditCard(
            name="Test",
            number="4242424242424242",
            month="01",
            year=str(date.today().year - 1),
            cvv="000",
        )


def test_model_expiry_year_current_year():
    cc = CreditCard(
        name="Test",
        number="4242424242424242",
        month="01",
        year=str(date.today().year),
        cvv="123",
    )
    assert cc.name == "Test"
    assert cc.number == "4242424242424242"
    assert cc.month == "01"
    assert cc.year == str(date.today().year)
    assert cc.cvv == "123"
    assert cc.brand == CreditCardBrand.VISA


def test_model_expiry_year_ten_years_from_now():
    cc = CreditCard(
        name="Test",
        number="4242424242424242",
        month="01",
        year=str(date.today().year + 10),
        cvv="123",
    )
    assert cc.name == "Test"
    assert cc.number == "4242424242424242"
    assert cc.month == "01"
    assert cc.year == str(date.today().year + 10)
    assert cc.cvv == "123"
    assert cc.brand == CreditCardBrand.VISA


def test_model_expiry_year_eleven_years_from_now():
    with pytest.raises(ValidationError):
        CreditCard(
            name="Test",
            number="4242424242424242",
            month="01",
            year=str(date.today().year + 11),
            cvv="000",
        )


def test_model_cvv_two_digits():
    with pytest.raises(ValidationError):
        CreditCard(
            name="Test",
            number="4242424242424242",
            month="01",
            year=str(date.today().year),
            cvv="12",
        )


def test_model_cvv_three_digits():
    cc = CreditCard(
        name="Test",
        number="4242424242424242",
        month="01",
        year=str(date.today().year),
        cvv="123",
    )
    assert cc.name == "Test"
    assert cc.number == "4242424242424242"
    assert cc.month == "01"
    assert cc.year == str(date.today().year)
    assert cc.cvv == "123"
    assert cc.brand == CreditCardBrand.VISA


def test_model_cvv_four_digits():
    with pytest.raises(ValidationError):
        CreditCard(
            name="Test",
            number="4242424242424242",
            month="01",
            year=str(date.today().year),
            cvv="1234",
        )
