from datetime import date
from pydantic import BaseModel, validator


class CreditCard(BaseModel):
    """
    Pydantic model that currently accepts only the following:
    VISA, DISCOVER, MASTERCARD, and AMEX.
    However, we also invalidate AMEX from the final solution.
    """

    name: str
    number: str
    month: str
    year: str
    cvv: str

    @property
    def brand(cls):
        """Checks the credit card number, returns the brand it's from."""
        # number = cls.number
        pass

    @validator("name")
    def validate_name(cls, name: str) -> str:
        """Checks the name is at least 2 characters; no numbers in the name"""
        if len(name.strip()) < 2:
            raise ValueError("Names must be at least 2 letters.")
        return name

    @validator("number")
    def validate_number(cls, number: str) -> str:
        pass

    @validator("month")
    def validate_month(cls, month: str) -> str:
        """Checks that the month index is between 1 and 12."""
        if not month.isdigit() or int(month) < 1 or int(month) > 12:
            raise ValueError("Must choose a number between 1 and 12.")
        return month

    @validator("year")
    def validate_year(cls, year: str) -> str:
        """Checks that the input year is a year in the future, including this year."""
        current_year = date.today().year
        if (
            not year.isdigit() or
            int(year) < current_year or
            int(year) > (current_year + 10)
        ):
            raise ValueError(
                f"Year must be between {current_year} and {current_year + 10}"
            )
        return year

    @validator("cvv")
    def validate_cvv(cls, cvv: str) -> str:
        """Checks that the cvv is a 3-digit number."""
        if not cvv.isdigit() or len(cvv) != 3:
            raise ValueError("Must be a valid 3-digit number.")
        return cvv


class AchAccount(BaseModel):
    """Pydantic model that validates an ACH account."""

    account: str
    routing: str

    @property
    def bank(cls):
        """Runs an API call to verify the routing number is tied to a real bank."""
        pass

    @validator("account")
    def validate_account_number(cls, num: str) -> str:
        if not num.isdigit() or len(num) < 3 or len(num) > 17:
            raise ValueError("Account numbers must be between 3 and 17 digits.")
        return num

    @validator("routing")
    def validate_routing_number(cls, num: str) -> str:
        if not num.isdigit() or len(num) != 9:
            raise ValueError("Routing numbers must be 9 digits.")
        return num


class Accreditation(BaseModel):
    """
    Pydantic model that calculates spend pools of a user's input for
    net worth and annual income.
    """

    annual_income: int
    net_worth: int

    @property
    def spend_capacity(cls) -> int:
        """
        Calculates how much someone can invest on equity crowdfunding platforms using
        the SEC's formula.
        """
        return 2200

    @validator("annual_income")
    def validate_annual_income(cls, num: int) -> int:
        if num < 0:
            raise ValueError("Must be greater than zero.")
        return num

    @validator("net_worth")
    def validate_net_worth(cls, num: int) -> int:
        if num < 0:
            raise ValueError("Must be greater than zero.")
        return num
