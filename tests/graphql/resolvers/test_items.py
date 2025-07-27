# server/tests/graphql/resolvers/test_items.py
import uuid
import pytest

ITEMTYPE_CREATE_MUTATION = r"""
mutation CreateItemType($input: ItemTypeInput!) {
  itemType {
    create(input: $input) {
      id
      name
      durability
    }
  }
}
"""

ITEMTYPE_UPDATE_MUTATION = r"""
mutation UpdateItemType($id: UUID!, $input: ItemTypeInput!) {
  itemType {
    update(id: $id, input: $input) {
      id
      name
      durability
    }
  }
}
"""

ITEMTYPE_DELETE_MUTATION = r"""
mutation DeleteItemType($id: UUID!) {
  itemType {
    delete(id: $id)
  }
}
"""

ITEMTYPE_GET_BY_ID_QUERY = r"""
query GetItemTypeById($id: UUID!) {
  itemType {
    byId(id: $id) {
      id
      name
      durability
    }
  }
}
"""

ITEMTYPE_GET_ALL_QUERY = r"""
query GetAllItemTypes {
  itemType {
    all {
      id
      name
      durability
    }
  }
}
"""


@pytest.mark.asyncio
async def test_create_itemtype(test_client, auth_headers):
    variables = {"input": {"name": f"ItemTypeOne_{uuid.uuid4().hex[:8]}", "durability": 100}}
    response = await test_client.post(
        "/graphql",
        json={"query": ITEMTYPE_CREATE_MUTATION, "variables": variables},
        headers=auth_headers
    )
    data = response.json()
    result = data["data"]["itemType"]["create"]
    assert result["name"] == variables["input"]["name"]
    assert result["durability"] == variables["input"]["durability"]


@pytest.mark.asyncio
async def test_update_itemtype(test_client, auth_headers):
    create_vars = {"input": {"name": f"ItemTypeUpdate_{uuid.uuid4().hex[:8]}", "durability": 50}}
    create_response = await test_client.post(
        "/graphql",
        json={"query": ITEMTYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers
    )
    create_data = create_response.json()["data"]["itemType"]["create"]

    update_vars = {
        "id": create_data["id"],
        "input": {"name": f"UpdatedItemType_{uuid.uuid4().hex[:8]}", "durability": 75}
    }
    update_response = await test_client.post(
        "/graphql",
        json={"query": ITEMTYPE_UPDATE_MUTATION, "variables": update_vars},
        headers=auth_headers
    )
    update_data = update_response.json()["data"]["itemType"]["update"]

    assert update_data["name"] == update_vars["input"]["name"]
    assert update_data["durability"] == update_vars["input"]["durability"]


@pytest.mark.asyncio
async def test_get_itemtype_by_id(test_client, auth_headers):
    create_vars = {"input": {"name": f"ItemTypeGet_{uuid.uuid4().hex[:8]}", "durability": 30}}
    create_response = await test_client.post(
        "/graphql",
        json={"query": ITEMTYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers
    )
    created = create_response.json()["data"]["itemType"]["create"]

    query_vars = {"id": created["id"]}
    get_response = await test_client.post(
        "/graphql",
        json={"query": ITEMTYPE_GET_BY_ID_QUERY, "variables": query_vars},
        headers=auth_headers
    )
    get_data = get_response.json()["data"]["itemType"]["byId"]

    assert get_data["id"] == created["id"]
    assert get_data["name"] == created["name"]


@pytest.mark.asyncio
async def test_get_all_itemtype(test_client, auth_headers):
    response = await test_client.post(
        "/graphql",
        json={"query": ITEMTYPE_GET_ALL_QUERY},
        headers=auth_headers
    )
    data = response.json()["data"]["itemType"]["all"]
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_delete_itemtype(test_client, auth_headers):
    create_vars = {"input": {"name": f"ItemTypeDelete_{uuid.uuid4().hex[:8]}", "durability": 10}}
    create_response = await test_client.post(
        "/graphql",
        json={"query": ITEMTYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers
    )
    created = create_response.json()["data"]["itemType"]["create"]

    delete_vars = {"id": created["id"]}
    delete_response = await test_client.post(
        "/graphql",
        json={"query": ITEMTYPE_DELETE_MUTATION, "variables": delete_vars},
        headers=auth_headers
    )
    delete_data = delete_response.json()["data"]["itemType"]["delete"]

    assert delete_data is True
