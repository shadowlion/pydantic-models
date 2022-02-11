import pytest
from pydantic import ValidationError

from app.models import NewsletterSubscriptionSchema


def test_model_instance():
    ns = NewsletterSubscriptionSchema(email="test@email.com")
    assert isinstance(ns, NewsletterSubscriptionSchema)
    assert "errors" not in ns


def test_email_input_invalid():
    with pytest.raises(ValidationError):
        NewsletterSubscriptionSchema()
        NewsletterSubscriptionSchema(email="a")
        NewsletterSubscriptionSchema(email="a@")
        NewsletterSubscriptionSchema(email="a@email")
        NewsletterSubscriptionSchema(email="a@email.")
        NewsletterSubscriptionSchema(email="a@email.c")
        NewsletterSubscriptionSchema(email="a@email.c0")
