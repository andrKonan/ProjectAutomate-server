import uuid

async def graphql_post(client, query, variables=None, headers=None):
    response = await client.post(
        "/graphql",
        json={"query": query, "variables": variables or {}},
        headers=headers
    )
    return response.json()


def assert_error_contains(data, keyword: str):
    assert "errors" in data
    assert keyword.lower() in data["errors"][0]["message"].lower()


def generate_unique_name(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def get_auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}