# server/tests/graphql/resolvers/test_structures.py
import pytest
import uuid

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
    unique_name = f"ItemForStructure_{uuid.uuid4().hex[:8]}"
    variables = {"input": {"name": unique_name, "durability": 100}}
    response = await test_client.post(
        "/graphql",
        json={"query": ITEMTYPE_CREATE_MUTATION, "variables": variables},
        headers=auth_headers,
    )
    return response.json()["data"]["itemType"]["create"]["id"]

@pytest.mark.asyncio
async def test_create_structuretype(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    variables = {
        "input": {
            "name": f"StructureTypeOne_{uuid.uuid4().hex[:8]}",
            "health": 100,
            "itemTypeId": item_type_id,
            "maxItems": 5,
            "itemToEngageId": None,
        }
    }
    response = await test_client.post(
        "/graphql",
        json={"query": STRUCTURETYPE_CREATE_MUTATION, "variables": variables},
        headers=auth_headers,
    )
    data = response.json()
    result = data["data"]["structureType"]["create"]
    assert result["name"] == variables["input"]["name"]

@pytest.mark.asyncio
async def test_update_structuretype(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    create_vars = {
        "input": {
            "name": f"StructureTypeUpdate_{uuid.uuid4().hex[:8]}",
            "health": 80,
            "itemTypeId": item_type_id,
            "maxItems": 3,
            "itemToEngageId": None,
        }
    }
    create_response = await test_client.post(
        "/graphql",
        json={"query": STRUCTURETYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers,
    )
    created = create_response.json()["data"]["structureType"]["create"]

    update_vars = {
        "id": created["id"],
        "input": {
            "name": f"UpdatedStructureType_{uuid.uuid4().hex[:8]}",
            "health": 90,
            "itemTypeId": item_type_id,
            "maxItems": 6,
            "itemToEngageId": None,
        },
    }
    update_response = await test_client.post(
        "/graphql",
        json={"query": STRUCTURETYPE_UPDATE_MUTATION, "variables": update_vars},
        headers=auth_headers,
    )
    update_data = update_response.json()["data"]["structureType"]["update"]
    assert update_data["name"] == update_vars["input"]["name"]

@pytest.mark.asyncio
async def test_get_structuretype_by_id(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    create_vars = {
        "input": {
            "name": f"StructureTypeGet_{uuid.uuid4().hex[:8]}",
            "health": 70,
            "itemTypeId": item_type_id,
            "maxItems": 4,
            "itemToEngageId": None,
        }
    }
    create_response = await test_client.post(
        "/graphql",
        json={"query": STRUCTURETYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers,
    )
    created = create_response.json()["data"]["structureType"]["create"]

    get_response = await test_client.post(
        "/graphql",
        json={"query": STRUCTURETYPE_GET_BY_ID_QUERY, "variables": {"id": created["id"]}},
        headers=auth_headers,
    )
    get_data = get_response.json()["data"]["structureType"]["byId"]
    assert get_data["id"] == created["id"]

@pytest.mark.asyncio
async def test_get_all_structuretype(test_client, auth_headers):
    response = await test_client.post(
        "/graphql",
        json={"query": STRUCTURETYPE_GET_ALL_QUERY},
        headers=auth_headers,
    )
    data = response.json()["data"]["structureType"]["all"]
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_delete_structuretype(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    create_vars = {
        "input": {
            "name": f"StructureTypeDelete_{uuid.uuid4().hex[:8]}",
            "health": 60,
            "itemTypeId": item_type_id,
            "maxItems": 2,
            "itemToEngageId": None,
        }
    }
    create_response = await test_client.post(
        "/graphql",
        json={"query": STRUCTURETYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers,
    )
    created = create_response.json()["data"]["structureType"]["create"]

    delete_response = await test_client.post(
        "/graphql",
        json={"query": STRUCTURETYPE_DELETE_MUTATION, "variables": {"id": created["id"]}},
        headers=auth_headers,
    )
    assert delete_response.json()["data"]["structureType"]["delete"] is True
