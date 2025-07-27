# server/tests/graphql/resolvers/test_bots.py
import uuid
import pytest

BOTTYPE_CREATE_MUTATION = r"""
mutation CreateBotType($input: BotTypeInput!) {
  botType {
    create(input: $input) {
      id
      name
      health
      strength
      speed
      vision
    }
  }
}
"""

BOTTYPE_UPDATE_MUTATION = r"""
mutation UpdateBotType($id: UUID!, $input: BotTypeInput!) {
  botType {
    update(id: $id, input: $input) {
      id
      name
      health
      strength
      speed
      vision
    }
  }
}
"""

BOTTYPE_DELETE_MUTATION = r"""
mutation DeleteBotType($id: UUID!) {
  botType {
    delete(id: $id)
  }
}
"""

BOTTYPE_GET_BY_ID_QUERY = r"""
query GetBotTypeById($id: UUID!) {
  botType {
    byId(id: $id) {
      id
      name
      health
      strength
      speed
      vision
    }
  }
}
"""

BOTTYPE_GET_ALL_QUERY = r"""
query GetAllBotTypes {
  botType {
    all {
      id
      name
      health
      strength
      speed
      vision
    }
  }
}
"""


@pytest.mark.asyncio
async def test_create_bottype(test_client, auth_headers):
    variables = {
        "input": {
            "name": f"BotTypeOne_{uuid.uuid4().hex[:8]}",
            "health": 100,
            "strength": 50,
            "speed": 20,
            "vision": 10
        }
    }
    response = await test_client.post(
        "/graphql",
        json={"query": BOTTYPE_CREATE_MUTATION, "variables": variables},
        headers=auth_headers
    )
    data = response.json()
    result = data["data"]["botType"]["create"]
    assert result["name"] == variables["input"]["name"]
    assert result["health"] == variables["input"]["health"]


@pytest.mark.asyncio
async def test_update_bottype(test_client, auth_headers):
    create_vars = {
        "input": {
            "name": f"BotTypeUpdate_{uuid.uuid4().hex[:8]}",
            "health": 80,
            "strength": 40,
            "speed": 25,
            "vision": 12
        }
    }
    create_response = await test_client.post(
        "/graphql",
        json={"query": BOTTYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers
    )
    create_data = create_response.json()["data"]["botType"]["create"]

    update_vars = {
        "id": create_data["id"],
        "input": {
            "name": f"UpdatedBotType_{uuid.uuid4().hex[:8]}",
            "health": 90,
            "strength": 55,
            "speed": 30,
            "vision": 15
        }
    }
    update_response = await test_client.post(
        "/graphql",
        json={"query": BOTTYPE_UPDATE_MUTATION, "variables": update_vars},
        headers=auth_headers
    )
    update_data = update_response.json()["data"]["botType"]["update"]

    assert update_data["name"] == update_vars["input"]["name"]
    assert update_data["health"] == update_vars["input"]["health"]


@pytest.mark.asyncio
async def test_get_bottype_by_id(test_client, auth_headers):
    create_vars = {
        "input": {
            "name": f"BotTypeGet_{uuid.uuid4().hex[:8]}",
            "health": 70,
            "strength": 35,
            "speed": 15,
            "vision": 8
        }
    }
    create_response = await test_client.post(
        "/graphql",
        json={"query": BOTTYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers
    )
    created = create_response.json()["data"]["botType"]["create"]

    query_vars = {"id": created["id"]}
    get_response = await test_client.post(
        "/graphql",
        json={"query": BOTTYPE_GET_BY_ID_QUERY, "variables": query_vars},
        headers=auth_headers
    )
    get_data = get_response.json()["data"]["botType"]["byId"]

    assert get_data["id"] == created["id"]
    assert get_data["name"] == created["name"]


@pytest.mark.asyncio
async def test_get_all_bottype(test_client, auth_headers):
    response = await test_client.post(
        "/graphql",
        json={"query": BOTTYPE_GET_ALL_QUERY},
        headers=auth_headers
    )
    data = response.json()["data"]["botType"]["all"]
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_delete_bottype(test_client, auth_headers):
    create_vars = {
        "input": {
            "name": f"BotTypeDelete_{uuid.uuid4().hex[:8]}",
            "health": 60,
            "strength": 30,
            "speed": 12,
            "vision": 6
        }
    }
    create_response = await test_client.post(
        "/graphql",
        json={"query": BOTTYPE_CREATE_MUTATION, "variables": create_vars},
        headers=auth_headers
    )
    created = create_response.json()["data"]["botType"]["create"]

    delete_vars = {"id": created["id"]}
    delete_response = await test_client.post(
        "/graphql",
        json={"query": BOTTYPE_DELETE_MUTATION, "variables": delete_vars},
        headers=auth_headers
    )
    delete_data = delete_response.json()["data"]["botType"]["delete"]

    assert delete_data is True
