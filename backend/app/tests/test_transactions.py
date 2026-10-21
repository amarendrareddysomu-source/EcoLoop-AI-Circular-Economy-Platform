import pytest
from fastapi import status
from app.models.user import UserRole

def get_auth_token(client, email="tx_user@circulareconomy.org", role="user", full_name="Transaction User"):
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": full_name,
        "role": role
    })
    res = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    return res.json()["access_token"]

def create_test_item(client, headers, name="Solar Power Bank", qty=10, price=50.0):
    item_payload = {
        "item_name": name,
        "description": "Portable 20000mAh solar charger",
        "category": "Electronics",
        "quantity": qty,
        "unit": "pcs",
        "price": price,
        "condition": "New",
        "status": "Available"
    }
    r = client.post("/api/v1/inventory/", json=item_payload, headers=headers)
    assert r.status_code == status.HTTP_201_CREATED
    return r.json()["id"]

def test_transaction_crud_types_and_inventory_updates(client):
    token = get_auth_token(client, email="seller_tx@example.com", full_name="Seller User")
    headers = {"Authorization": f"Bearer {token}"}

    item_id = create_test_item(client, headers, name="Recyclable Plastic Container", qty=10, price=12.5)

    # 1. Test Sale: decreases stock from 10 to 6
    sale_payload = {
        "item_id": item_id,
        "transaction_type": "sale",
        "quantity": 4,
        "unit_price": 12.5,
        "notes": "Bulk container sale"
    }
    sale_res = client.post("/api/v1/transactions/", json=sale_payload, headers=headers)
    assert sale_res.status_code == status.HTTP_201_CREATED
    s_data = sale_res.json()
    assert s_data["transaction_type"] == "sale"
    assert s_data["quantity"] == 4
    assert s_data["total_amount"] == 50.0

    # Verify inventory item stock updated to 6
    inv_res1 = client.get(f"/api/v1/inventory/{item_id}", headers=headers)
    assert inv_res1.json()["quantity"] == 6

    # 2. Test Donation: decreases stock from 6 to 4
    donate_payload = {
        "item_id": item_id,
        "transaction_type": "donation",
        "quantity": 2,
        "notes": "Donate to local NGO"
    }
    don_res = client.post("/api/v1/transactions/", json=donate_payload, headers=headers)
    assert don_res.status_code == status.HTTP_201_CREATED

    inv_res2 = client.get(f"/api/v1/inventory/{item_id}", headers=headers)
    assert inv_res2.json()["quantity"] == 4

    # 3. Test Recycling zero stock transition
    recycle_payload = {
        "item_id": item_id,
        "transaction_type": "recycling",
        "quantity": 4,
        "notes": "Send remaining units to recycling center"
    }
    rec_res = client.post("/api/v1/transactions/", json=recycle_payload, headers=headers)
    assert rec_res.status_code == status.HTTP_201_CREATED

    # Verify stock reaches 0 and status becomes "Recycled"
    inv_res3 = client.get(f"/api/v1/inventory/{item_id}", headers=headers)
    assert inv_res3.json()["quantity"] == 0
    assert inv_res3.json()["status"] == "Recycled"

    # 4. Test Purchase: increases stock from 0 to 15, status resets to "Available"
    purch_payload = {
        "item_id": item_id,
        "transaction_type": "purchase",
        "quantity": 15,
        "unit_price": 10.0,
        "notes": "Restock inventory"
    }
    purch_res = client.post("/api/v1/transactions/", json=purch_payload, headers=headers)
    assert purch_res.status_code == status.HTTP_201_CREATED

    inv_res4 = client.get(f"/api/v1/inventory/{item_id}", headers=headers)
    assert inv_res4.json()["quantity"] == 15
    assert inv_res4.json()["status"] == "Available"

def test_transaction_insufficient_stock_validation(client):
    token = get_auth_token(client, email="stock_check@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    item_id = create_test_item(client, headers, name="Limited Edition Watch", qty=2, price=300.0)

    # Attempt to sell 5 units when only 2 available -> 400 Bad Request
    over_sale = {
        "item_id": item_id,
        "transaction_type": "sale",
        "quantity": 5,
        "unit_price": 300.0
    }
    res = client.post("/api/v1/transactions/", json=over_sale, headers=headers)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "Insufficient inventory stock" in res.json()["detail"]

    # Verify stock remains unchanged
    inv_res = client.get(f"/api/v1/inventory/{item_id}", headers=headers)
    assert inv_res.json()["quantity"] == 2

def test_transaction_non_existent_item_validation(client):
    token = get_auth_token(client, email="invalid_item@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "item_id": 99999,
        "transaction_type": "sale",
        "quantity": 1
    }
    res = client.post("/api/v1/transactions/", json=payload, headers=headers)
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_transaction_pydantic_validation(client):
    token = get_auth_token(client, email="pyd_tx@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    item_id = create_test_item(client, headers)

    # Invalid zero quantity
    res1 = client.post("/api/v1/transactions/", json={"item_id": item_id, "quantity": 0}, headers=headers)
    assert res1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Invalid negative unit price
    res2 = client.post("/api/v1/transactions/", json={"item_id": item_id, "unit_price": -10.0}, headers=headers)
    assert res2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_transaction_search_filters_pagination_sorting(client):
    token = get_auth_token(client, email="search_tx@example.com", full_name="Searcher Tx")
    headers = {"Authorization": f"Bearer {token}"}

    item_id1 = create_test_item(client, headers, name="Refurbished MacBook", qty=20, price=800.0)
    item_id2 = create_test_item(client, headers, name="Standing Desk", qty=15, price=400.0)

    # Create multiple transactions
    client.post("/api/v1/transactions/", json={"item_id": item_id1, "transaction_type": "sale", "quantity": 2, "unit_price": 800.0}, headers=headers)
    client.post("/api/v1/transactions/", json={"item_id": item_id1, "transaction_type": "donation", "quantity": 1, "unit_price": 0.0}, headers=headers)
    client.post("/api/v1/transactions/", json={"item_id": item_id2, "transaction_type": "purchase", "quantity": 5, "unit_price": 400.0}, headers=headers)

    # 1. Search by item name "MacBook"
    search_res = client.get("/api/v1/transactions/?search=MacBook", headers=headers)
    assert search_res.status_code == status.HTTP_200_OK
    assert search_res.json()["total_items"] == 2

    # 2. Filter by transaction_type
    filter_res = client.get("/api/v1/transactions/?transaction_type=sale", headers=headers)
    assert filter_res.status_code == status.HTTP_200_OK
    assert filter_res.json()["total_items"] == 1

    # 3. Pagination
    pag_res = client.get("/api/v1/transactions/?page=1&page_size=2", headers=headers)
    assert pag_res.status_code == status.HTTP_200_OK
    p_data = pag_res.json()
    assert len(p_data["items"]) == 2
    assert p_data["total_items"] == 3
    assert p_data["total_pages"] == 2

    # 4. Sorting by amount desc
    sort_res = client.get("/api/v1/transactions/?sort_by=amount&sort_order=desc", headers=headers)
    assert sort_res.status_code == status.HTTP_200_OK
    amounts = [t["total_amount"] for t in sort_res.json()["items"]]
    assert amounts == sorted(amounts, reverse=True)

def test_transaction_cancellation_restores_stock(client):
    token = get_auth_token(client, email="canceller@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    item_id = create_test_item(client, headers, name="Gaming Console", qty=5, price=500.0)

    # Sale of 2 consoles -> remaining stock 3
    tx_res = client.post("/api/v1/transactions/", json={"item_id": item_id, "transaction_type": "sale", "quantity": 2, "unit_price": 500.0}, headers=headers)
    tx_id = tx_res.json()["id"]

    inv_res1 = client.get(f"/api/v1/inventory/{item_id}", headers=headers)
    assert inv_res1.json()["quantity"] == 3

    # Delete / Cancel transaction -> stock restored to 5!
    del_res = client.delete(f"/api/v1/transactions/{tx_id}", headers=headers)
    assert del_res.status_code == status.HTTP_204_NO_CONTENT

    inv_res2 = client.get(f"/api/v1/inventory/{item_id}", headers=headers)
    assert inv_res2.json()["quantity"] == 5

def test_transaction_authorization(client):
    user1_token = get_auth_token(client, email="tx_user1@example.com", full_name="User 1")
    headers1 = {"Authorization": f"Bearer {user1_token}"}
    item_id = create_test_item(client, headers1)

    tx_res = client.post("/api/v1/transactions/", json={"item_id": item_id, "quantity": 1}, headers=headers1)
    tx_id = tx_res.json()["id"]

    # User 2 tries to access User 1's transaction -> 403 Forbidden
    user2_token = get_auth_token(client, email="tx_user2@example.com", full_name="User 2")
    headers2 = {"Authorization": f"Bearer {user2_token}"}

    get_forbidden = client.get(f"/api/v1/transactions/{tx_id}", headers=headers2)
    assert get_forbidden.status_code == status.HTTP_403_FORBIDDEN

    # Admin user accesses User 1's transaction -> 200 OK
    admin_token = get_auth_token(client, email="tx_admin@example.com", role=UserRole.ADMIN.value, full_name="Admin Tx")
    headers_admin = {"Authorization": f"Bearer {admin_token}"}

    get_admin = client.get(f"/api/v1/transactions/{tx_id}", headers=headers_admin)
    assert get_admin.status_code == status.HTTP_200_OK

    # Unauthenticated -> 401 Unauthorized
    unauth = client.get(f"/api/v1/transactions/{tx_id}")
    assert unauth.status_code == status.HTTP_401_UNAUTHORIZED
