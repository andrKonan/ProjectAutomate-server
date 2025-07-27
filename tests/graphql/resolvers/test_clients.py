# server/tests/graphql/resolvers/test_clients.py
import uuid
import pytest

CLIENT_REGISTER_MUTATION = r"""
mutation Register($name: String!) {
    client {
        create(input: {name: $name}) {
            id
            Token
            createdAt
            name
        }
    }
}
"""

CLIENT_RENAME_MUTATUION = r"""
mutation RenameClient($id: UUID!, $name: String!) {
    client {
        update(input: {id: $id, name: $name}) {
            id
            createdAt
            name
        }
    }
}
"""

CLIENT_GET_ME_QUERY = r"""
query GetMyClient {
  client {
    me {
        id
        Token
        createdAt
        name
    }
  }
}
"""


@pytest.mark.asyncio
async def test_create_client(test_client):
    variables = {"name": f"TestUserCreate_{uuid.uuid4().hex[:8]}"}
    response = await test_client.post(
        "/graphql",
        json={"query": CLIENT_REGISTER_MUTATION, "variables": variables}
    )
    data = response.json()
    
    assert "data" in data
    assert data["data"] is not None
    assert data["data"]["client"]["create"]["name"] == variables["name"]
    assert "Token" in data["data"]["client"]["create"]


@pytest.mark.asyncio
async def test_update_client(test_client):
    variables = {"name": f"TestUserUpdate_{uuid.uuid4().hex[:8]}"}
    response = await test_client.post(
        "/graphql",
        json={"query": CLIENT_REGISTER_MUTATION, "variables": variables}
    )
    data = response.json()
    data = data["data"]["client"]["create"]

    headers = {
        "Authorization": f"Bearer {data['Token']}"
    }

    rename_variables = {"name": f"TestUpdate_{uuid.uuid4().hex[:8]}", "id": data['id']}
    response = await test_client.post(
        "/graphql",
        json={"query": CLIENT_RENAME_MUTATUION, "variables": rename_variables}, 
        headers=headers
    )

    data = response.json()
    assert data["data"]["client"]["update"]["name"] == rename_variables["name"]


@pytest.mark.asyncio
async def test_get_client(test_client):
    variables = {"name": f"TestUserGetMe_{uuid.uuid4().hex[:8]}"}
    response = await test_client.post(
        "/graphql",
        json={"query": CLIENT_REGISTER_MUTATION, "variables": variables}
    )
    data_create = response.json()["data"]["client"]["create"]

    headers = {
        "Authorization": f"Bearer {data_create['Token']}"
    }

    response = await test_client.post(
        "/graphql",
        json={"query": CLIENT_GET_ME_QUERY},
        headers=headers
    )
    data_response = response.json()["data"]["client"]["me"]

    for key, value in data_create.items():
        assert value == data_response.get(key)
