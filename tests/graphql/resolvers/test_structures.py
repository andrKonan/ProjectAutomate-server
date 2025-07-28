# server/tests/graphql/resolvers/test_structures.py
import pytest
import uuid

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

STRUCTURETYPE_CREATE_MUTATION = r"""
mutation CreateStructureType($input: StructureTypeInput!) {
  structureType {
    create(input: $input) {
      id
      name
      health
      itemTypeId
      maxItems
      itemToEngageId
    }
  }
}
"""

STRUCTURETYPE_UPDATE_MUTATION = r"""
mutation UpdateStructureType($id: UUID!, $input: StructureTypeInput!) {
  structureType {
    update(id: $id, input: $input) {
      id
      name
      health
      itemTypeId
      maxItems
      itemToEngageId
    }
  }
}
"""

STRUCTURETYPE_DELETE_MUTATION = r"""
mutation DeleteStructureType($id: UUID!) {
  structureType {
    delete(id: $id)
  }
}
"""

STRUCTURETYPE_GET_BY_ID_QUERY = r"""
query GetStructureTypeById($id: UUID!) {
  structureType {
    byId(id: $id) {
      id
      name
      health
      itemTypeId
      maxItems
      itemToEngageId
    }
  }
}
"""

STRUCTURETYPE_GET_ALL_QUERY = r"""
query GetAllStructureTypes {
  structureType {
    all {
      id
      name
      health
      itemTypeId
      maxItems
      itemToEngageId
    }
  }
}
"""

async def create_item_type(test_client, auth_headers):
    unique_name = generate_unique_name("ItemForStructure")
    variables = {"input": {"name": unique_name, "durability": 100}}

    data = await graphql_post(test_client, ITEMTYPE_CREATE_MUTATION, variables, auth_headers)

    return data["data"]["itemType"]["create"]["id"]

@pytest.mark.asyncio
async def test_create_structuretype(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    variables = {
        "input": {
            "name": generate_unique_name("StructureTypeOne"),
            "health": 100,
            "itemTypeId": item_type_id,
            "maxItems": 5,
            "itemToEngageId": None,
        }
    }

    data = await graphql_post(test_client, STRUCTURETYPE_CREATE_MUTATION, variables, auth_headers)
    result = data["data"]["structureType"]["create"]

    assert result["name"] == variables["input"]["name"]

@pytest.mark.asyncio
async def test_update_structuretype(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    create_vars = {
        "input": {
            "name": generate_unique_name("StructureTypeUpdate"),
            "health": 80,
            "itemTypeId": item_type_id,
            "maxItems": 3,
            "itemToEngageId": None,
        }
    }
    
    data = await graphql_post(test_client, STRUCTURETYPE_CREATE_MUTATION, create_vars, auth_headers)
    created = data["data"]["structureType"]["create"]

    update_vars = {
        "id": created["id"],
        "input": {
            "name": generate_unique_name("UpdatedStructureType"),
            "health": 90,
            "itemTypeId": item_type_id,
            "maxItems": 6,
            "itemToEngageId": None,
        },
    }

    data = await graphql_post(test_client, STRUCTURETYPE_UPDATE_MUTATION, update_vars, auth_headers)
    update_data = data["data"]["structureType"]["update"]

    assert update_data["name"] == update_vars["input"]["name"]

@pytest.mark.asyncio
async def test_get_structuretype_by_id(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    create_vars = {
        "input": {
            "name": generate_unique_name("StructureTypeGet"),
            "health": 70,
            "itemTypeId": item_type_id,
            "maxItems": 4,
            "itemToEngageId": None,
        }
    }

    data = await graphql_post(test_client, STRUCTURETYPE_CREATE_MUTATION, create_vars, auth_headers)
    created = data["data"]["structureType"]["create"]

    data = await graphql_post(test_client, STRUCTURETYPE_GET_BY_ID_QUERY, {"id": created["id"]}, auth_headers)
    get_data = data["data"]["structureType"]["byId"]

    assert get_data["id"] == created["id"]

@pytest.mark.asyncio
async def test_get_all_structuretype(test_client, auth_headers):
    response = await graphql_post(test_client, STRUCTURETYPE_GET_ALL_QUERY, headers=auth_headers)
    data = response["data"]["structureType"]["all"]
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_delete_structuretype(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    create_vars = {
        "input": {
            "name": generate_unique_name("StructureTypeDelete"),
            "health": 60,
            "itemTypeId": item_type_id,
            "maxItems": 2,
            "itemToEngageId": None,
        }
    }

    data = await graphql_post(test_client, STRUCTURETYPE_CREATE_MUTATION, create_vars, auth_headers)
    created = data["data"]["structureType"]["create"]

    data = await graphql_post(test_client, STRUCTURETYPE_DELETE_MUTATION, {"id": created["id"]}, auth_headers)
    delete_response = data["data"]["structureType"]["delete"]

    assert delete_response is True

@pytest.mark.asyncio
async def test_create_structuretype_missing_fields(test_client, auth_headers):
    data = await graphql_post(test_client, STRUCTURETYPE_CREATE_MUTATION, {"input": {}}, auth_headers)

    assert_error_contains(data, "field")

@pytest.mark.asyncio
async def test_update_structuretype_invalid_id(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    fake_id = str(uuid.uuid4())
    update_vars = {
        "id": fake_id,
        "input": {
            "name": "GhostStructure",
            "health": 80,
            "itemTypeId": item_type_id,
            "maxItems": 2,
            "itemToEngageId": None
        }
    }

    data = await graphql_post(test_client, STRUCTURETYPE_UPDATE_MUTATION, update_vars, auth_headers)
    
    assert_error_contains(data, "not found")

@pytest.mark.asyncio
async def test_delete_structuretype_invalid_id(test_client, auth_headers):
    fake_id = str(uuid.uuid4())

    data = await graphql_post(test_client, STRUCTURETYPE_DELETE_MUTATION, {"id": fake_id}, auth_headers)

    assert_error_contains(data, "not found")

@pytest.mark.asyncio
async def test_get_structuretype_by_id_malformed_uuid(test_client, auth_headers):
    data = await graphql_post(test_client, STRUCTURETYPE_GET_BY_ID_QUERY, {"id": "invalid-uuid"}, auth_headers)
    
    assert_error_contains(data, "uuid")


@pytest.mark.asyncio
async def test_get_all_structuretypes_unauthenticated(test_client):
    data = await graphql_post(test_client, STRUCTURETYPE_GET_ALL_QUERY)
    
    assert_error_contains(data, "authorization required")
