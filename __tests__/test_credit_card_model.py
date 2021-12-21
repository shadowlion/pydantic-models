from datetime import date
from app.models import CreditCard


def test_instance():
    credit_card = CreditCard(
        name="Test",
        number="0000000000000000",
        month="01",
        year=str(date.today().year),
        cvv="000",
    )
    assert isinstance(credit_card, CreditCard)
