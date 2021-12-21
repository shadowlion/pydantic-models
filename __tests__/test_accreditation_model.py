import pytest
from pydantic import ValidationError

from app.models import Accreditation


def test_accredtiation_model_instance():
    accreditation = Accreditation()
    assert isinstance(accreditation, Accreditation)


def test_model_no_inputs():
    a = Accreditation()
    assert a.annual_income == 0
    assert a.net_worth == 0
    assert a.spend_capacity == 2_200
    assert a.accredited is False


def test_model_minimum_input():
    a = Accreditation(
        annual_income=0,
        net_worth=0,
    )
    assert a.annual_income == 0
    assert a.net_worth == 0
    assert a.spend_capacity == 2_200
    assert a.accredited is False


def test_model_annual_income_only():
    a = Accreditation(
        annual_income=1_000_000,
    )
    assert a.annual_income == 1_000_000
    assert a.net_worth == 0
    assert a.spend_capacity == 2_200
    assert a.accredited is False


def test_model_net_worth_only():
    a = Accreditation(
        net_worth=1_000_000,
    )
    assert a.annual_income == 0
    assert a.net_worth == 1_000_000
    assert a.spend_capacity == 2_200
    assert a.accredited is False


def test_model_below_minimum_annual_income():
    with pytest.raises(ValidationError):
        Accreditation(
            annual_income=-1,
        )


def test_model_below_minimum_net_worth():
    with pytest.raises(ValidationError):
        Accreditation(net_worth=-1)


def test_model_max_limits():
    a = Accreditation(
        annual_income=999_999_999,
        net_worth=999_999_999,
    )
    assert a.annual_income == 999_999_999
    assert a.net_worth == 999_999_999
    assert a.spend_capacity == 107_000
    assert a.accredited is True


def test_model_min_accredited_investor_limits():
    a = Accreditation(
        annual_income=200_000,
        net_worth=1_000_000,
    )
    assert a.annual_income == 200_000
    assert a.net_worth == 1_000_000
    assert a.spend_capacity == 20_000
    assert a.accredited is True


def test_model_just_below_min_accredited_investor_limits_annual_income():
    a = Accreditation(
        annual_income=199_999.99,
        net_worth=1_000_000,
    )
    assert a.annual_income == 199_999
    assert a.net_worth == 1_000_000
    assert a.spend_capacity == 19999.9
    assert a.accredited is False


def test_model_just_below_min_accredited_investor_limits_net_worth():
    a = Accreditation(
        annual_income=200_000,
        net_worth=999_999.99,
    )
    assert a.annual_income == 200_000
    assert a.net_worth == 999_999
    assert a.spend_capacity == 20_000
    assert a.accredited is False
