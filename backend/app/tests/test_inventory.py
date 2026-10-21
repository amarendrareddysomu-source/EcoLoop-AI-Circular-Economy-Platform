import pytest
from fastapi import status
from app.models.user import UserRole
from app.models.organization import Organization

def get_auth_token(client, email="inv_user@circulareconomy.org", role="user", full_name="Inventory User"):
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": full_name,
        "role": role
    })
    res = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    return res.json()["access_token"]

def test_inventory_create_and_get(client):
    token = get_auth_token(client, email="creator@example.com", full_name="Creator User")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "item_name": "Ergonomic Office Chair",
        "description": "Adjustable mesh chair with lumbar support",
        "category": "Furniture",
        "quantity": 5,
        "unit": "pcs",
        "price": 149.99,
        "condition": "New",
        "status": "Available",
        "brand": "Herman Miller",
        "location": "Warehouse A"
    }

    response = client.post("/api/v1/inventory/", json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["item_name"] == "Ergonomic Office Chair"
    assert data["title"] == "Ergonomic Office Chair"
    assert data["category"] == "Furniture"
    assert data["quantity"] == 5
    assert data["unit"] == "pcs"
    assert data["price"] == 149.99
    assert data["condition"] == "New"
    assert data["status"] == "Available"
    item_id = data["id"]

    # Get single item
    get_res = client.get(f"/api/v1/inventory/{item_id}", headers=headers)
    assert get_res.status_code == status.HTTP_200_OK
    assert get_res.json()["id"] == item_id

def test_inventory_update_and_delete(client):
    token = get_auth_token(client, email="updator@example.com", full_name="Updator User")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "item_name": "Stainless Steel Water Bottle",
        "category": "Plastic",
        "quantity": 100,
        "unit": "units",
        "price": 15.0,
        "condition": "New",
        "status": "Available"
    }
    res = client.post("/api/v1/inventory/", json=payload, headers=headers)
    item_id = res.json()["id"]

    # Update item
    update_payload = {
        "item_name": "Insulated Hydro Flask",
        "quantity": 80,
        "price": 25.0,
        "status": "Reserved"
    }
    upd_res = client.put(f"/api/v1/inventory/{item_id}", json=update_payload, headers=headers)
    assert upd_res.status_code == status.HTTP_200_OK
    upd_data = upd_res.json()
    assert upd_data["item_name"] == "Insulated Hydro Flask"
    assert upd_data["quantity"] == 80
    assert upd_data["price"] == 25.0
    assert upd_data["status"] == "Reserved"

    # Delete item
    del_res = client.delete(f"/api/v1/inventory/{item_id}", headers=headers)
    assert del_res.status_code == status.HTTP_204_NO_CONTENT

    # Verify 404 on get
    get_res = client.get(f"/api/v1/inventory/{item_id}", headers=headers)
    assert get_res.status_code == status.HTTP_404_NOT_FOUND

def test_inventory_pydantic_validation(client):
    token = get_auth_token(client, email="validator@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Invalid negative price
    invalid_price = {
        "item_name": "Bad Price Item",
        "category": "Electronics",
        "price": -10.0
    }
    res1 = client.post("/api/v1/inventory/", json=invalid_price, headers=headers)
    assert res1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Invalid negative quantity
    invalid_qty = {
        "item_name": "Bad Qty Item",
        "category": "Electronics",
        "quantity": -5
    }
    res2 = client.post("/api/v1/inventory/", json=invalid_qty, headers=headers)
    assert res2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_inventory_search_filters_pagination_sorting(client):
    token = get_auth_token(client, email="searcher@example.com", full_name="Search User")
    headers = {"Authorization": f"Bearer {token}"}

    # Create multiple items
    items_to_create = [
        {"item_name": "Dell XPS 15 Laptop", "description": "High performance laptop", "category": "Electronics", "quantity": 3, "price": 1200.0, "condition": "Used", "status": "Available"},
        {"item_name": "MacBook Pro M2", "description": "Apple laptop with M2 silicon", "category": "Electronics", "quantity": 10, "price": 2000.0, "condition": "New", "status": "Available"},
        {"item_name": "Logitech Wireless Mouse", "description": "Ergonomic computer peripheral", "category": "Electronics", "quantity": 50, "price": 30.0, "condition": "New", "status": "Available"},
        {"item_name": "Recycled Paper Notebooks", "description": "Eco friendly stationery", "category": "Paper", "quantity": 200, "price": 5.0, "condition": "Recycled", "status": "Sold"},
        {"item_name": "Wooden Dining Table", "description": "Solid pine wood dining set", "category": "Furniture", "quantity": 2, "price": 450.0, "condition": "Used", "status": "Reserved"},
    ]

    for item in items_to_create:
        r = client.post("/api/v1/inventory/", json=item, headers=headers)
        assert r.status_code == status.HTTP_201_CREATED

    # 1. Partial case-insensitive search
    search_res = client.get("/api/v1/inventory/?search=LAPTOP", headers=headers)
    assert search_res.status_code == status.HTTP_200_OK
    search_data = search_res.json()
    assert search_data["total_items"] == 2
    assert all("laptop" in i["item_name"].lower() or "laptop" in i["description"].lower() for i in search_data["items"])

    # 2. Filter by category
    cat_res = client.get("/api/v1/inventory/?category=Electronics", headers=headers)
    assert cat_res.status_code == status.HTTP_200_OK
    assert cat_res.json()["total_items"] == 3

    # 3. Filter by condition
    cond_res = client.get("/api/v1/inventory/?condition=Recycled", headers=headers)
    assert cond_res.status_code == status.HTTP_200_OK
    assert cond_res.json()["total_items"] == 1
    assert cond_res.json()["items"][0]["item_name"] == "Recycled Paper Notebooks"

    # 4. Filter by status
    stat_res = client.get("/api/v1/inventory/?status=Reserved", headers=headers)
    assert stat_res.status_code == status.HTTP_200_OK
    assert stat_res.json()["total_items"] == 1
    assert stat_res.json()["items"][0]["item_name"] == "Wooden Dining Table"

    # 5. Price range filter
    price_res = client.get("/api/v1/inventory/?min_price=100&max_price=1500", headers=headers)
    assert price_res.status_code == status.HTTP_200_OK
    assert price_res.json()["total_items"] == 2 # Dell XPS 15 (1200) & Wooden Dining Table (450)

    # 6. Quantity range filter
    qty_res = client.get("/api/v1/inventory/?min_quantity=10&max_quantity=100", headers=headers)
    assert qty_res.status_code == status.HTTP_200_OK
    assert qty_res.json()["total_items"] == 2 # MacBook (10) & Mouse (50)

    # 7. Pagination
    page_res = client.get("/api/v1/inventory/?page=1&page_size=2", headers=headers)
    assert page_res.status_code == status.HTTP_200_OK
    p_data = page_res.json()
    assert len(p_data["items"]) == 2
    assert p_data["page"] == 1
    assert p_data["page_size"] == 2
    assert p_data["total_items"] == 5
    assert p_data["total_pages"] == 3

    # 8. Sorting by price asc
    sort_res = client.get("/api/v1/inventory/?sort_by=price&sort_order=asc", headers=headers)
    assert sort_res.status_code == status.HTTP_200_OK
    prices = [i["price"] for i in sort_res.json()["items"]]
    assert prices == sorted(prices)

    # 9. Sorting by price desc
    sort_desc_res = client.get("/api/v1/inventory/?sort_by=price&sort_order=desc", headers=headers)
    assert sort_desc_res.status_code == status.HTTP_200_OK
    prices_desc = [i["price"] for i in sort_desc_res.json()["items"]]
    assert prices_desc == sorted(prices_desc, reverse=True)

def test_inventory_authorization(client):
    # User 1 creates item
    user1_token = get_auth_token(client, email="user1@example.com", full_name="User One")
    headers1 = {"Authorization": f"Bearer {user1_token}"}

    item_payload = {
        "item_name": "User 1 Private Asset",
        "category": "Electronics",
        "price": 500.0
    }
    r = client.post("/api/v1/inventory/", json=item_payload, headers=headers1)
    item_id = r.json()["id"]

    # User 2 tries to access User 1's item -> 403 Forbidden
    user2_token = get_auth_token(client, email="user2@example.com", full_name="User Two")
    headers2 = {"Authorization": f"Bearer {user2_token}"}

    forbidden_get = client.get(f"/api/v1/inventory/{item_id}", headers=headers2)
    assert forbidden_get.status_code == status.HTTP_403_FORBIDDEN

    forbidden_put = client.put(f"/api/v1/inventory/{item_id}", json={"price": 600.0}, headers=headers2)
    assert forbidden_put.status_code == status.HTTP_403_FORBIDDEN

    forbidden_del = client.delete(f"/api/v1/inventory/{item_id}", headers=headers2)
    assert forbidden_del.status_code == status.HTTP_403_FORBIDDEN

    # Admin user can access User 1's item -> 200 OK
    admin_token = get_auth_token(client, email="admin_inv@example.com", role=UserRole.ADMIN.value, full_name="Admin User")
    headers_admin = {"Authorization": f"Bearer {admin_token}"}

    admin_get = client.get(f"/api/v1/inventory/{item_id}", headers=headers_admin)
    assert admin_get.status_code == status.HTTP_200_OK
    assert admin_get.json()["id"] == item_id

    # Unauthenticated request -> 401 Unauthorized
    unauth_res = client.get(f"/api/v1/inventory/{item_id}")
    assert unauth_res.status_code == status.HTTP_401_UNAUTHORIZED
