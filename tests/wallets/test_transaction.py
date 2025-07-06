from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from wallets.models import Transaction


@pytest.mark.django_db
def test_wallet_starts_with_zero_balance(wallet):
    assert wallet.balance == Decimal("0.0")


@pytest.mark.django_db
def test_transaction_increases_balance(wallet, create_transaction):
    create_transaction("tx-001", Decimal("100.0"))
    wallet.refresh_from_db()
    assert wallet.balance == Decimal("100.0")


@pytest.mark.django_db
def test_transaction_decreases_balance(wallet, create_transaction):
    create_transaction("tx-002", Decimal("200.0"))
    create_transaction("tx-003", Decimal("-50.0"))
    wallet.refresh_from_db()
    assert wallet.balance == Decimal("150.0")


@pytest.mark.django_db
def test_transaction_update_changes_balance(wallet, create_transaction):
    tx = create_transaction("tx-004", Decimal("50.0"))
    tx.amount = Decimal("80.0")
    tx.save()
    wallet.refresh_from_db()
    assert wallet.balance == Decimal("80.0")


@pytest.mark.django_db
def test_transaction_delete_restores_balance(wallet, create_transaction):
    tx = create_transaction("tx-005", Decimal("60.0"))
    tx.delete()
    wallet.refresh_from_db()
    assert wallet.balance == Decimal("0.0")


@pytest.mark.django_db
def test_transaction_negative_balance_prevented(wallet):
    with pytest.raises(ValidationError):
        Transaction.objects.create(
            wallet=wallet, txid="tx-fail", amount=Decimal("-5.0")
        )


@pytest.mark.django_db
def test_duplicate_txid_not_allowed(wallet, create_transaction):
    create_transaction("tx-dup", Decimal("10.0"))
    with pytest.raises(Exception):
        Transaction.objects.create(wallet=wallet, txid="tx-dup", amount=Decimal("5.0"))
