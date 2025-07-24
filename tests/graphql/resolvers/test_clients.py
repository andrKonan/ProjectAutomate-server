# server/tests/graphql/resolvers/test_clients.py
import pytest

CREATE_CLIENT_MUTATION = """
mutation Register {
  client {
    create(input: {name: "TestUser"}) {
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
    response = await test_client.post("/graphql", json={"query": CREATE_CLIENT_MUTATION})
    data = response.json()
    print(data)
    
    assert "data" in data
    assert data["data"] is not None
    assert data["data"]["client"]["create"]["name"] == "TestUser"
    assert "Token" in data["data"]["client"]["create"]