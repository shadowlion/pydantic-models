from typing import Any, Optional, Protocol
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
