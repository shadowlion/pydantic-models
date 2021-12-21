import pytest

from pydantic import ValidationError

from app.models import AchAccount


def test_model_instance():
    ach = AchAccount(
        account="123456789",
        routing="021000021",
    )
    assert isinstance(ach, AchAccount)


def test_model_no_inputs():
    with pytest.raises(ValidationError):
        AchAccount()


def test_model_account_number_input_only():
    with pytest.raises(ValidationError):
        AchAccount(
            account="123",
        )


def test_model_routing_number_input_only():
    with pytest.raises(ValidationError):
        AchAccount(
            routing="123456789",
        )


def test_model_account_number_two_digits():
    with pytest.raises(ValidationError):
        AchAccount(
            account="12",
            routing="021000021"
        )


def test_model_account_number_three_digits():
    ach = AchAccount(
        account="123",
        routing="021000021",
    )
    assert ach.account == "123"
    assert ach.routing == "021000021"


def test_model_account_number_seventeen_digits():
    ach = AchAccount(
        account="123",
        routing="021000021",
    )
    assert ach.account == "123"
    assert ach.routing == "021000021"


def test_model_account_number_eighteen_digits():
    with pytest.raises(ValidationError):
        AchAccount(
            account="123456789012345678",
            routing="021000021",
        )


def test_model_routing_number_eight_digits():
    with pytest.raises(ValidationError):
        AchAccount(
            account="123",
            routing="02100002",
        )


def test_model_routing_number_nine_digits():
    routing_numbers = (
        "021000021",
        "011401533",
        "091000019",
    )
    for i, r in enumerate(routing_numbers):
        ach = AchAccount(
            account="123",
            routing=r,
        )
        assert len(ach.routing) == 9
        assert ach.account == "123"
        assert ach.routing == routing_numbers[i]


def test_model_routing_number_ten_digits():
    with pytest.raises(ValidationError):
        AchAccount(
            account="123",
            routing="0210000210",
        )
