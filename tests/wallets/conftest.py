from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from wallets.models import Transaction, Wallet


@pytest.fixture
def api_client():
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }

    client = APIClient(headers=headers)

    return client


@pytest.fixture
def headers():
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }
    return headers


@pytest.fixture
def wallet():
    return Wallet.objects.create(label="Test Wallet")


@pytest.fixture
def create_transaction(wallet):
    def _create(txid: str, amount: Decimal):
        return Transaction.objects.create(wallet=wallet, txid=txid, amount=amount)

    return _create
