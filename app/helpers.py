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
    url = "https://api.norcapsecurities.com/tapiv3/index.php/v3/"
    r = requests.request(method, url + endpoint, data=payload)
    return r.json()


def validate_aba_routing_number(routing_number: str) -> APIResponse:
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
