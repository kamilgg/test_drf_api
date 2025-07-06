from decimal import Decimal

import pytest

from wallets.models import Transaction


@pytest.mark.django_db
def test_create_wallet_via_api(api_client, headers):
    response = api_client.post(
        "/api/wallets/",
        {"data": {"type": "Wallet", "attributes": {"label": "API Wallet"}}},
        headers=headers,
        format="json",
    )
    assert response.status_code == 201
    assert response.json()
    assert "data" in response.json()

    data = response.json()["data"]

    assert data["attributes"]["label"] == "API Wallet"
    assert Decimal(data["attributes"]["balance"]) == Decimal("0.0")


@pytest.mark.django_db
def test_create_transaction_and_update_balance(api_client, headers, wallet):
    txid = "api-tx-001"
    amount = Decimal("150.0")

    response = api_client.post(
        "/api/transactions/",
        {
            "data": {
                "type": "Transaction",
                "attributes": {"txid": txid, "amount": str(amount)},
                "relationships": {
                    "wallet": {"data": {"type": "Wallet", "id": str(wallet.id)}}
                },
            }
        },
        headers=headers,
        format="json",
    )
    assert response.status_code == 201
    assert response.data

    wallet.refresh_from_db()
    assert wallet.balance == amount


@pytest.mark.django_db
def test_cannot_create_transaction_with_negative_balance(api_client, headers, wallet):
    response = api_client.post(
        "/api/transactions/",
        {
            "data": {
                "type": "Transaction",
                "attributes": {"txid": "api-tx-neg", "amount": "-50.0"},
                "relationships": {
                    "wallet": {"data": {"type": "Wallet", "id": str(wallet.id)}}
                },
            }
        },
        headers=headers,
        format="json",
    )
    assert response.status_code == 400
    assert response.data

    assert "balance" not in wallet.__dict__ or wallet.balance == Decimal("0.0")


@pytest.mark.django_db
def test_cannot_create_duplicate_txid(api_client, headers, wallet):
    txid = "api-dup-tx"
    Transaction.objects.create(wallet=wallet, txid=txid, amount=Decimal("10.0"))

    response = api_client.post(
        "/api/transactions/",
        {
            "data": {
                "type": "Transaction",
                "attributes": {"txid": txid, "amount": "5.0"},
                "relationships": {
                    "wallet": {"data": {"type": "Wallet", "id": str(wallet.id)}}
                },
            }
        },
        headers=headers,
        format="json",
    )
    assert response.status_code == 400
    assert response.data


@pytest.mark.django_db
def test_delete_transaction_restores_balance(api_client, headers, wallet):
    tx = Transaction.objects.create(
        wallet=wallet, txid="tx-delete", amount=Decimal("30.0")
    )
    wallet.refresh_from_db()
    assert wallet.balance == Decimal("30.0")

    url = f"/api/transactions/{tx.id}/"
    response = api_client.delete(url, headers=headers)
    assert response.status_code == 204

    wallet.refresh_from_db()
    assert wallet.balance == Decimal("0.0")
