# server/tests/graphql/resolvers/test_items.py
import uuid
import pytest

from ...utils import generate_unique_name, graphql_post, assert_error_contains

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
    variables = {"input": {"name": generate_unique_name("ItemTypeOne"), "durability": 100}}

    data = await graphql_post(test_client, ITEMTYPE_CREATE_MUTATION, variables, auth_headers)
    
    result = data["data"]["itemType"]["create"]
    assert result["name"] == variables["input"]["name"]
    assert result["durability"] == variables["input"]["durability"]

@pytest.mark.asyncio
async def test_update_itemtype(test_client, auth_headers):
    create_vars = {"input": {"name": generate_unique_name("ItemTypeUpdate"), "durability": 50}}

    data = await graphql_post(test_client, ITEMTYPE_CREATE_MUTATION, create_vars, auth_headers)
    create_data = data["data"]["itemType"]["create"]

    update_vars = {
        "id": create_data["id"],
        "input": {"name": generate_unique_name("UpdatedItemType"), "durability": 75}
    }

    data = await graphql_post(test_client, ITEMTYPE_UPDATE_MUTATION, update_vars, auth_headers)
    update_data = data["data"]["itemType"]["update"]

    assert update_data["name"] == update_vars["input"]["name"]
    assert update_data["durability"] == update_vars["input"]["durability"]

@pytest.mark.asyncio
async def test_get_itemtype_by_id(test_client, auth_headers):
    create_vars = {"input": {"name": generate_unique_name("ItemTypeGet"), "durability": 30}}

    data = await graphql_post(test_client, ITEMTYPE_CREATE_MUTATION, create_vars, auth_headers)
    create_data = data["data"]["itemType"]["create"]

    query_vars = {"id": create_data["id"]}
    
    data = await graphql_post(test_client, ITEMTYPE_GET_BY_ID_QUERY, query_vars, auth_headers)
    get_data = data["data"]["itemType"]["byId"]

    assert get_data["id"] == create_data["id"]
    assert get_data["name"] == create_data["name"]

@pytest.mark.asyncio
async def test_get_all_itemtype(test_client, auth_headers):
    data = await graphql_post(test_client, ITEMTYPE_GET_ALL_QUERY, headers=auth_headers)

    data = data["data"]["itemType"]["all"]

    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_delete_itemtype(test_client, auth_headers):
    create_vars = {"input": {"name": generate_unique_name("ItemTypeDelete"), "durability": 10}}

    data = await graphql_post(test_client, ITEMTYPE_CREATE_MUTATION, create_vars, auth_headers)
    create_data = data["data"]["itemType"]["create"]

    delete_vars = {"id": create_data["id"]}
    
    data = await graphql_post(test_client, ITEMTYPE_DELETE_MUTATION, delete_vars, auth_headers)
    delete_data = data["data"]["itemType"]["delete"]

    assert delete_data is True

@pytest.mark.asyncio
async def test_create_itemtype_missing_fields(test_client, auth_headers):
    data = await graphql_post(test_client, ITEMTYPE_CREATE_MUTATION, {"input": {}}, auth_headers)
    
    assert_error_contains(data, "field")

@pytest.mark.asyncio
async def test_update_itemtype_invalid_id(test_client, auth_headers):
    fake_id = str(uuid.uuid4())
    update_vars = {
        "id": fake_id,
        "input": {
            "name": "FakeItem",
            "durability": 999
        }
    }

    data = await graphql_post(test_client, ITEMTYPE_UPDATE_MUTATION, update_vars, auth_headers)

    assert_error_contains(data, "not found")

@pytest.mark.asyncio
async def test_delete_itemtype_invalid_id(test_client, auth_headers):
    fake_id = str(uuid.uuid4())
    
    data = await graphql_post(test_client, ITEMTYPE_DELETE_MUTATION, {"id": fake_id}, auth_headers)
    
    assert_error_contains(data, "not found")

@pytest.mark.asyncio
async def test_get_itemtype_by_id_malformed_uuid(test_client, auth_headers):
    data = await graphql_post(test_client, ITEMTYPE_GET_BY_ID_QUERY, {"id": "not-a-uuid"}, auth_headers)

    assert_error_contains(data, "uuid")

@pytest.mark.asyncio
async def test_get_all_itemtype_unauthenticated(test_client):
    data = await graphql_post(test_client, ITEMTYPE_GET_ALL_QUERY)

    assert_error_contains(data, "authorization required")