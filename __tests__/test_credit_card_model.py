import pytest

from pydantic import ValidationError
from datetime import date

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


def test_model_cardholder_number_is_discover():
    pass


def test_model_cardholder_number_is_mastercard():
    pass


def test_model_cardholder_number_is_american_express():
    pass


def test_model_cardholder_number_is_invalid_card():
    pass


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


def test_model_cvv_four_digits():
    with pytest.raises(ValidationError):
        CreditCard(
            name="Test",
            number="4242424242424242",
            month="01",
            year=str(date.today().year),
            cvv="1234",
        )
