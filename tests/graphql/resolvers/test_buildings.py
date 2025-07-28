# server/tests/graphql/resolvers/test_buildings.py
import pytest
import uuid

BUILDINGTYPE_CREATE_MUTATION = r"""
mutation CreateBuildingType($input: BuildingTypeInput!) {
  buildingType {
    create(input: $input) {
      id
      name
      health
    }
  }
}
"""

BUILDINGTYPE_UPDATE_MUTATION = r"""
mutation UpdateBuildingType($id: UUID!, $input: BuildingTypeInput!) {
  buildingType {
    update(id: $id, input: $input) {
      id
      name
      health
    }
  }
}
"""

BUILDINGTYPE_DELETE_MUTATION = r"""
mutation DeleteBuildingType($id: UUID!) {
  buildingType {
    delete(id: $id)
  }
}
"""

BUILDINGTYPE_GET_BY_ID_QUERY = r"""
query GetBuildingTypeById($id: UUID!) {
  buildingType {
    byId(id: $id) {
      id
      name
      health
    }
  }
}
"""

BUILDINGTYPE_GET_ALL_QUERY = r"""
query GetAllBuildingTypes {
  buildingType {
    all {
      id
      name
      health
    }
  }
}
"""

@pytest.mark.asyncio
async def test_create_buildingtype(test_client, auth_headers):
    variables = {
        "input": {
            "name": f"BuildingTypeOne_{uuid.uuid4().hex[:8]}",
            "health": 100,
            "buildingRecipes": []
        }
    }
    response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_CREATE_MUTATION, "variables": variables},
        headers=auth_headers
    )
    data = response.json()
    result = data["data"]["buildingType"]["create"]
    assert result["name"] == variables["input"]["name"]
    assert result["health"] == variables["input"]["health"]

@pytest.mark.asyncio
async def test_update_buildingtype(test_client, auth_headers):
    create_vars = {
        "input": {
            "name": f"BuildingTypeUpdate_{uuid.uuid4().hex[:8]}",
            "health": 80,
            "buildingRecipes": []
        }
    }
    create_response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers
    )
    created = create_response.json()["data"]["buildingType"]["create"]

    update_vars = {
        "id": created["id"],
        "input": {
            "name": f"UpdatedBuildingType_{uuid.uuid4().hex[:8]}",
            "health": 90,
            "buildingRecipes": []
        }
    }
    update_response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_UPDATE_MUTATION, "variables": update_vars},
        headers=auth_headers
    )
    update_data = update_response.json()["data"]["buildingType"]["update"]
    assert update_data["name"] == update_vars["input"]["name"]
    assert update_data["health"] == update_vars["input"]["health"]

@pytest.mark.asyncio
async def test_get_buildingtype_by_id(test_client, auth_headers):
    create_vars = {
        "input": {
            "name": f"BuildingTypeGet_{uuid.uuid4().hex[:8]}",
            "health": 70,
            "buildingRecipes": []
        }
    }
    create_response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers
    )
    created = create_response.json()["data"]["buildingType"]["create"]

    get_response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_GET_BY_ID_QUERY, "variables": {"id": created["id"]}},
        headers=auth_headers
    )
    get_data = get_response.json()["data"]["buildingType"]["byId"]
    assert get_data["id"] == created["id"]
    assert get_data["name"] == created["name"]

@pytest.mark.asyncio
async def test_get_all_buildingtype(test_client, auth_headers):
    response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_GET_ALL_QUERY},
        headers=auth_headers
    )
    data = response.json()["data"]["buildingType"]["all"]
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_delete_buildingtype(test_client, auth_headers):
    create_vars = {
        "input": {
            "name": f"BuildingTypeDelete_{uuid.uuid4().hex[:8]}",
            "health": 60,
            "buildingRecipes": []
        }
    }
    create_response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers
    )
    created = create_response.json()["data"]["buildingType"]["create"]

    delete_response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_DELETE_MUTATION, "variables": {"id": created["id"]}},
        headers=auth_headers
    )
    assert delete_response.json()["data"]["buildingType"]["delete"] is True

@pytest.mark.asyncio
async def test_create_buildingtype_missing_fields(test_client, auth_headers):
    response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_CREATE_MUTATION, "variables": {"input": {}}},
        headers=auth_headers
    )
    data = response.json()
    assert "errors" in data
    assert "field" in data["errors"][0]["message"].lower()

@pytest.mark.asyncio
async def test_update_buildingtype_invalid_id(test_client, auth_headers):
    fake_id = str(uuid.uuid4())
    update_vars = {
        "id": fake_id,
        "input": {
            "name": "InvalidUpdate",
            "health": 200,
            "buildingRecipes": []
        }
    }
    response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_UPDATE_MUTATION, "variables": update_vars},
        headers=auth_headers
    )
    data = response.json()
    assert "errors" in data
    assert "not found" in data["errors"][0]["message"].lower()

@pytest.mark.asyncio
async def test_delete_buildingtype_invalid_id(test_client, auth_headers):
    fake_id = str(uuid.uuid4())
    response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_DELETE_MUTATION, "variables": {"id": fake_id}},
        headers=auth_headers
    )
    data = response.json()
    assert "errors" in data
    assert "not found" in data["errors"][0]["message"].lower()

@pytest.mark.asyncio
async def test_get_buildingtype_by_id_malformed_uuid(test_client, auth_headers):
    response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_GET_BY_ID_QUERY, "variables": {"id": "not-a-uuid"}},
        headers=auth_headers
    )
    data = response.json()
    assert "errors" in data
    assert "uuid" in data["errors"][0]["message"].lower()

@pytest.mark.asyncio
async def test_get_all_buildingtypes_unauthenticated(test_client):
    response = await test_client.post(
        "/graphql",
        json={"query": BUILDINGTYPE_GET_ALL_QUERY}
    )
    data = response.json()
    assert "errors" in data
    assert "authorization required" in data["errors"][0]["message"].lower()