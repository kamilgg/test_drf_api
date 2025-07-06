from decimal import Decimal

import pytest


@pytest.mark.django_db
def test_filter_by_wallet(api_client, wallet, create_transaction):
    create_transaction("tx-wallet-1", Decimal("10"))
    create_transaction("tx-wallet-2", Decimal("20"))

    response = api_client.get(f"/api/transactions/?filter[wallet]={wallet.id}")

    assert response.status_code == 200
    assert response.json()
    assert "data" in response.json()

    data = response.json()["data"]

    assert len(data) == 2


@pytest.mark.django_db
def test_filter_by_txid_partial(api_client, wallet, create_transaction):
    create_transaction("test-apple-001", Decimal("100"))
    create_transaction("test-apple-002", Decimal("50"))
    create_transaction("banana-001", Decimal("75"))

    response = api_client.get("/api/transactions/?filter[txid]=apple")

    assert response.status_code == 200
    assert response.json()
    assert "data" in response.json()

    data = response.json()["data"]

    txids = [item["attributes"]["txid"] for item in data]

    assert all("apple" in tx for tx in txids)
    assert len(txids) == 2


@pytest.mark.django_db
def test_filter_by_amount_range(api_client, wallet, create_transaction):
    create_transaction("tx-a", Decimal("5"))
    create_transaction("tx-b", Decimal("15"))
    create_transaction("tx-c", Decimal("25"))

    response = api_client.get(
        "/api/transactions/?filter[amount_min]=10&filter[amount_max]=20"
    )

    assert response.status_code == 200
    assert response.json()
    assert "data" in response.json()

    data = response.json()["data"]

    txids = [tx["attributes"]["txid"] for tx in data]

    assert "tx-b" in txids
    assert "tx-a" not in txids
    assert "tx-c" not in txids


@pytest.mark.django_db
def test_ordering_by_amount(api_client, wallet, create_transaction):
    create_transaction("tx-1", Decimal("50"))
    create_transaction("tx-2", Decimal("10"))
    create_transaction("tx-3", Decimal("30"))

    response = api_client.get("/api/transactions/?sort=amount")

    assert response.status_code == 200
    assert response.json()
    assert "data" in response.json()

    data = response.json()["data"]

    amounts = [Decimal(tx["attributes"]["amount"]) for tx in data]

    assert amounts == sorted(amounts)


@pytest.mark.django_db
def test_ordering_by_created_at_desc(api_client, wallet, create_transaction):
    tx1 = create_transaction("t1", Decimal("10"))
    tx2 = create_transaction("t2", Decimal("20"))
    tx3 = create_transaction("t3", Decimal("30"))

    response = api_client.get("/api/transactions/?sort=-created_at")

    assert response.status_code == 200
    assert response.json()
    assert "data" in response.json()

    data = response.json()["data"]

    ids = [int(tx["id"]) for tx in data]

    assert ids == sorted(ids, reverse=True)
