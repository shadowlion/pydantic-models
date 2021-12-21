from app.models import AchAccount


def test_instance():
    ach_account = AchAccount(
        account="123",
        routing="123456789",
    )
    assert isinstance(ach_account, AchAccount)
