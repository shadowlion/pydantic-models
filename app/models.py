from datetime import date
from typing import Union

from pydantic import BaseModel, validator, EmailStr

from app.helpers import (
    CreditCardBrand,
    credit_card_brand,
    spend_pool,
    validate_aba_routing_number,
)


class NewsletterSubscriptionSchema(BaseModel):
    """Newsletter Subscription Schema"""

    email: EmailStr


class CreditCard(BaseModel):
    """
    Credit Card pydantic model.

    Currently accepts only the following: VISA, DISCOVER, MASTERCARD, and AMEX.

    However, we also invalidate AMEX from the final solution.
    """

    name: str
    number: str
    month: str
    year: str
    cvv: str

    @property
    def brand(cls) -> CreditCardBrand:
        """Checks the credit card number, returns the brand it's from.

        Returns:
            str: credit card company (abbr)
        """
        return credit_card_brand(cls.number)

    @validator("name")
    def validate_name(cls, name: str) -> str:
        """Validates cardholder name

        Conditions:
            - Must be an alpha string.
            - Must be at least 2 letters long.
        """
        assert (
            name.isalpha() and len(name.strip()) > 1
        ), "Names must be at least 2 letters long."
        return name

    @validator("number")
    def validate_number(cls, number: str) -> str:
        """Validates the cardholder number

        Conditions:
            - Must be a number string.
            - Must be a 16-digit number.
        """
        assert number.strip().isdigit(), "Must be a number."
        assert (
            len(number.strip()) == 16
            or credit_card_brand(number) == CreditCardBrand.AMERICAN_EXPRESS
        ), "Must be a 16 digit number OR 15 digits if using Amex."
        return number

    @validator("month")
    def validate_month(cls, month: str) -> str:
        """Validate expiry month

        Conditions:
            - Must be a number string.
            - Must be between 1 and 12.
        """
        assert month.isdigit() and 1 <= int(month) <= 12, "Must be between 1 and 12."
        return month

    @validator("year")
    def validate_year(cls, year: str) -> str:
        """Validate expiry year

        Conditions:
            - Must be a number string.
            - Must be between this year and ten years to date.
        """
        current_year = date.today().year
        assert (
            year.isdigit() and current_year <= int(year) <= current_year + 10
        ), f"Year must be between {current_year} and {current_year + 10}."
        return year

    @validator("cvv")
    def validate_cvv(cls, cvv: str) -> str:
        """Validate cvv number

        Conditions:
            - Must be a number string.
            - Must be at least 3 digits.
        """
        assert cvv.isdigit() and len(cvv) == 3, "Must be a 3 digit number."
        return cvv


class AchAccount(BaseModel):
    """ACH Account pydantic model."""

    account: str
    routing: str

    @validator("account")
    def validate_account_number(cls, num: str) -> str:
        """Validate the account number input.

        Conditions:
            - Must be a number string.
            - Must be between 3 and 17 digits.
        """
        assert num.isdigit() and 3 <= len(num) <= 17, "Must be between 3 and 17 digits."
        return num

    @validator("routing")
    def validate_routing_number(cls, num: str) -> str:
        """Validate the routing number input.

        Conditions:
            - Must be a number string.
            - Must be exactly 9 digits.
        """
        assert (
            num.isdigit() and len(num) == 9
        ), "Accepted routing numbers must be exactly 9 digits."
        r = validate_aba_routing_number(num)
        if r.get("statusCode") == "215":
            raise ValueError("Invalid routing number")
        return num


class Accreditation(BaseModel):
    """
    Pydantic model that calculates spend pools of a user's input for
    net worth and annual income.
    """

    annual_income: Union[int, float] = 0
    net_worth: Union[int, float] = 0

    @property
    def accredited(cls) -> bool:
        """Check if the investor is accredited.

        Conditions:
            - Annual income is at least $200k
            - Net worth is at least $1M
        """
        return cls.annual_income >= 200_000 and cls.net_worth >= 1_000_000

    @property
    def spend_capacity(cls) -> int:
        """
        Calculates how much someone can invest on equity crowdfunding platforms using
        the SEC's formula.
        """
        return spend_pool(cls.annual_income, cls.net_worth)

    @validator("annual_income")
    def validate_annual_income(cls, num: int) -> int:
        """Validate annual income

        Conditions:
            - Number must be greater than or equal to zero.
        """
        assert num >= 0, "Must be greater than or equal to zero."
        return num

    @validator("net_worth")
    def validate_net_worth(cls, num: int) -> int:
        """Validate net worth

        Conditions:
            - Number must be greater than or equal to zero.
        """
        assert num >= 0, "Must be greater than or equal to zero."
        return num
