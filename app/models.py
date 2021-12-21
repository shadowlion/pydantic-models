from datetime import date
from typing import Union

from pydantic import BaseModel, validator

from app.helpers import spend_pool, validate_aba_routing_number


class CreditCard(BaseModel):
    """
    Credit Card pydantic model. Ccurrently accepts only the following:
    VISA, DISCOVER, MASTERCARD, and AMEX.
    However, we also invalidate AMEX from the final solution.
    """

    name: str
    number: str
    month: str
    year: str
    cvv: str

    @property
    def brand(cls) -> str:
        """Checks the credit card number, returns the brand it's from.

        Returns:
            str: credit card company (abbr)
        """
        pass

    @validator("name")
    def validate_name(cls, name: str) -> str:
        """Validates cardholder name

        Args:
            name (str): cardholder name

        Raises:
            ValueError: Name length must be greater than 1 character

        Returns:
            str: cardholder name
        """
        if len(name.strip()) < 2:
            raise ValueError("Names must be at least 2 letters.")
        return name

    @validator("number")
    def validate_number(cls, number: str) -> str:
        pass

    @validator("month")
    def validate_month(cls, month: str) -> str:
        """Validate expiry month

        Args:
            month (str): expiry month

        Raises:
            ValueError: Must be between 1 and 12

        Returns:
            str: expiry month
        """
        if not month.isdigit() or int(month) < 1 or int(month) > 12:
            raise ValueError("Must choose a number between 1 and 12.")
        return month

    @validator("year")
    def validate_year(cls, year: str) -> str:
        """Validate expiry year

        Args:
            year (str): expiry year

        Raises:
            ValueError: Year must be between {current year} and {current year + 10}

        Returns:
            str: expiry year
        """
        current_year = date.today().year
        if (
            not year.isdigit()
            or int(year) < current_year
            or int(year) > (current_year + 10)
        ):
            raise ValueError(
                f"Year must be between {current_year} and {current_year + 10}"
            )
        return year

    @validator("cvv")
    def validate_cvv(cls, cvv: str) -> str:
        """Validate cvv number

        Args:
            cvv (str): cvv number

        Raises:
            ValueError: Must be a valid 3-digit number

        Returns:
            str: cvv number
        """
        if not cvv.isdigit() or len(cvv) != 3:
            raise ValueError("Must be a valid 3-digit number.")
        return cvv


class AchAccount(BaseModel):
    """ACH Account pydantic model."""

    account: str
    routing: str

    @validator("account")
    def validate_account_number(cls, num: str) -> str:
        """Validate the account number input.

        Args:
            num (str): account number

        Raises:
            ValueError: Account numbers must be between 3 and 17 digits

        Returns:
            str: account number
        """
        if not num.isdigit() or len(num) < 3 or len(num) > 17:
            raise ValueError("Account numbers must be between 3 and 17 digits.")
        return num

    @validator("routing")
    def validate_routing_number(cls, num: str) -> str:
        """Validate the routing number input.

        Args:
            num (str): routing number

        Raises:
            ValueError: Routing numbers must be 9 digits
            ValueError: Routing number is invalid

        Returns:
            str: routing number
        """
        if not num.isdigit() or len(num) != 9:
            raise ValueError("Routing numbers must be 9 digits.")
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

        Args:
            num (int): annual income

        Raises:
            ValueError: Must be greater than 0

        Returns:
            int: annual income
        """
        if num < 0:
            raise ValueError("Must be greater than zero.")
        return num

    @validator("net_worth")
    def validate_net_worth(cls, num: int) -> int:
        """Validate net worth

        Args:
            num (int): net worth

        Raises:
            ValueError: Must be greater than 0

        Returns:
            int: net worth
        """
        if num < 0:
            raise ValueError("Must be greater than zero.")
        return num
