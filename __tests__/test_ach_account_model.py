from app.models import AchAccount


def test_instance():
    ach_account = AchAccount(
        account="1234",
        routing="021000021",
    )
    assert isinstance(ach_account, AchAccount)


def test_ach_account_valid_account_number_edge_cases():
    ach_account_three_digits = AchAccount(
        account="123",
        routing="021000021",
    )
    assert len(ach_account_three_digits.account) == 3

    ach_account_seventeen_digits = AchAccount(
        account="12345678901234567",
        routing="021000021",
    )
    assert len(ach_account_seventeen_digits.account) == 17


def test_ach_account_different_routing_numbers():
    routing_numbers = [
        "021000021",
        "011401533",
        "091000019",
    ]
    for r in routing_numbers:
        ach_account = AchAccount(
            account="123",
            routing=r,
        )
        assert len(ach_account.routing) == 9
