from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db.models import Sum

from wallets.models import Transaction, Wallet


@pytest.mark.django_db
def test_wallet_creation(wallet):
    assert isinstance(wallet, Wallet)
    assert wallet.label == "Test Wallet"
    assert wallet.balance == Decimal("0.0")


@pytest.mark.django_db
def test_wallet_str(wallet):
    assert str(wallet) == f"Wallet({wallet.label})"


@pytest.mark.django_db
def test_wallet_balance_accumulates(create_transaction, wallet):
    create_transaction("tx-w-001", Decimal("10.0"))
    create_transaction("tx-w-002", Decimal("20.5"))
    create_transaction("tx-w-003", Decimal("-5.0"))

    wallet.refresh_from_db()
    assert wallet.balance == Decimal("25.5")


@pytest.mark.django_db
def test_wallet_balance_matches_aggregated_amount(wallet, create_transaction):
    create_transaction("tx-a-1", Decimal("100.0"))
    create_transaction("tx-a-2", Decimal("-30.0"))
    create_transaction("tx-a-3", Decimal("25.5"))

    wallet.refresh_from_db()

    aggregated = wallet.transactions.aggregate(total=Sum("amount"))["total"] or Decimal(
        "0"
    )
    assert wallet.balance == aggregated


@pytest.mark.django_db
def test_wallet_balance_with_no_transactions(wallet):
    assert wallet.transactions.count() == 0
    assert wallet.balance == Decimal("0.0")


@pytest.mark.django_db
def test_cannot_create_transaction_that_causes_negative_balance(wallet):
    with pytest.raises(ValidationError):
        Transaction.objects.create(
            wallet=wallet, txid="tx-neg-1", amount=Decimal("-10.0")
        )


@pytest.mark.django_db
def test_cannot_update_transaction_to_cause_negative_balance(
    wallet, create_transaction
):
    tx = create_transaction("tx-neg-2", Decimal("50.0"))

    tx.amount = Decimal("-100.0")
    with pytest.raises(ValidationError):
        tx.save()


@pytest.mark.django_db
def test_delete_raises_if_result_balance_negative(wallet, create_transaction):
    tx1 = create_transaction("t1", Decimal("50.0"))  # +50
    tx2 = create_transaction("t2", Decimal("-40.0"))  # -40
    tx3 = create_transaction("t3", Decimal("-10.0"))  # -10

    wallet.refresh_from_db()
    assert wallet.balance == Decimal("0.0")

    with pytest.raises(ValidationError):
        tx1.delete()


@pytest.mark.django_db
def test_wallet_transaction_relation(wallet, create_transaction):
    tx1 = create_transaction("tx-w-004", Decimal("100.0"))
    tx2 = create_transaction("tx-w-005", Decimal("-25.0"))

    related = wallet.transactions.all()
    assert tx1 in related
    assert tx2 in related
    assert related.count() == 2
