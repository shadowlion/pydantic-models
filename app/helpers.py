import re
from enum import Enum
from typing import Any, Optional, Protocol, Union

import requests
from pydantic import BaseModel

from config import CLIENT_ID, DEVELOPER_API_KEY


class APIPayload(BaseModel):
    clientID: str
    developerAPIKey: str
    routingNumber: str


class APIResponse(Protocol):
    statusCode: str
    statusDesc: str
    accountDetails: Optional[str]


def api_call(method: str, endpoint: str, payload: Any = None):
    """Runs an API call to Transact API

    Args:
        method (str): HTTP method
        endpoint (str): url endpoint (see documentation)
        payload (Dict[str, Union[str, int, float]], optional): Data payload.
        Defaults to None.

    Returns:
        [Any]: JSON response from the Transact API servers
    """
    url = "https://api.norcapsecurities.com/tapiv3/index.php/v3/"
    r = requests.request(method, url + endpoint, data=payload)
    return r.json()


def validate_aba_routing_number(routing_number: str) -> APIResponse:
    """Validates an ABA routing number via Transact API.

    Reference: https://api.norcapsecurities.com/admin_v3/documentation?mid=MjU1

    Args:
        routing_number (str): Routing number

    Returns:
        APIResponse
    """
    payload = APIPayload(
        clientID=CLIENT_ID,
        developerAPIKey=DEVELOPER_API_KEY,
        routingNumber=routing_number,
    )
    return api_call("POST", "validateABARoutingnumber", payload.dict())


def spend_pool(
    annual_income: Union[int, float],
    net_worth: Union[int, float],
) -> Union[int, float]:
    """Calculates the spend capacity per annum of any single investor.

    Args:
        annual_income (Union[int, float]): Annual income
        net_worth (Union[int, float]): Net worth

    Returns:
        Union[int, float]: The amount an investor can invest per annum in equity
        crowdfunding
    """

    choice = min(annual_income, net_worth)
    minimum = 2200
    maximum = 107_000

    if choice < maximum:
        return max(minimum, choice * 0.05)
    else:
        return maximum if choice * 0.1 >= maximum else choice * 0.1


class CreditCardBrand(str, Enum):
    VISA = "VI"
    MASTERCARD = "MC"
    DISCOVER = "DI"
    AMERICAN_EXPRESS = "AM"


def credit_card_brand(n: str) -> CreditCardBrand:
    """Determines which company the credit card came from.

    Args:
        `n` (str): cardholder number

    Raises:
        ValueError: Invalid credit card number (doesn't match any supplied regex)

    Returns:
        str: One of the following: "VI", "DI", "MC", "AM"
    """
    visa_regex = r"^4[0-9]{12}(?:[0-9]{3})?$"
    discover_regex = r"^6(?:011|5[0-9]{2})[0-9]{12}$"
    mastercard_regex = r"^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$"  # noqa E501
    amex_regex = r"^3[47][0-9]{13}$"

    if re.match(visa_regex, n):
        return CreditCardBrand.VISA
    elif re.match(discover_regex, n):
        return CreditCardBrand.DISCOVER
    elif re.match(mastercard_regex, n):
        return CreditCardBrand.MASTERCARD
    elif re.match(amex_regex, n):
        return CreditCardBrand.AMERICAN_EXPRESS
    else:
        raise ValueError("Invalid credit card number.")
