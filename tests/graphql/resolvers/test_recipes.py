# server/tests/graphql/resolvers/test_recipes.py
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

RECIPE_CREATE_MUTATION = r"""
mutation CreateRecipe($input: RecipeInput!) {
  recipe {
    create(input: $input) {
      id
      name
      outputAmount
    }
  }
}
"""

RECIPE_UPDATE_MUTATION = r"""
mutation UpdateRecipe($id: UUID!, $input: RecipeInput!) {
  recipe {
    update(id: $id, input: $input) {
      id
      name
      outputAmount
    }
  }
}
"""

RECIPE_DELETE_MUTATION = r"""
mutation DeleteRecipe($id: UUID!) {
  recipe {
    delete(id: $id)
  }
}
"""

RECIPE_GET_BY_ID_QUERY = r"""
query GetRecipeById($id: UUID!) {
  recipe {
    byId(id: $id) {
      id
      name
      outputAmount
    }
  }
}
"""

RECIPE_GET_ALL_QUERY = r"""
query GetAllRecipes {
  recipe {
    all {
      id
      name
      outputAmount
    }
  }
}
"""

async def create_item_type(test_client, auth_headers):
    variables = {
        "input": {
            "name": f"Item_{uuid.uuid4().hex[:8]}",
            "durability": 100
        }
    }
    response = await test_client.post(
        "/graphql", json={"query": ITEMTYPE_CREATE_MUTATION, "variables": variables}, headers=auth_headers
    )
    return response.json()["data"]["itemType"]["create"]["id"]

async def create_building_type(test_client, auth_headers):
    variables = {
        "input": {
            "name": f"Building_{uuid.uuid4().hex[:8]}",
            "health": 100,
            "buildingRecipes": []
        }
    }
    response = await test_client.post(
        "/graphql", json={"query": BUILDINGTYPE_CREATE_MUTATION, "variables": variables}, headers=auth_headers
    )
    return response.json()["data"]["buildingType"]["create"]["id"]

async def create_recipe(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    building_type_id = await create_building_type(test_client, auth_headers)
    variables = {
        "input": {
            "name": f"Recipe_{uuid.uuid4().hex[:8]}",
            "buildingTypeId": building_type_id,
            "outputItemTypeId": item_type_id,
            "outputAmount": 5,
            "ingredients": [
                {
                    "itemTypeId": item_type_id,
                    "amount": 2
                }
            ]
        }
    }
    response = await test_client.post(
        "/graphql", json={"query": RECIPE_CREATE_MUTATION, "variables": variables}, headers=auth_headers
    )
    return response.json()["data"]["recipe"]["create"]

@pytest.mark.asyncio
async def test_create_recipe(test_client, auth_headers):
    recipe = await create_recipe(test_client, auth_headers)
    assert recipe["name"].startswith("Recipe_")
    assert recipe["outputAmount"] == 5

@pytest.mark.asyncio
async def test_update_recipe(test_client, auth_headers):
    original_recipe = await create_recipe(test_client, auth_headers)

    new_item_type_id = await create_item_type(test_client, auth_headers)
    new_building_type_id = await create_building_type(test_client, auth_headers)

    new_name = f"UpdatedRecipe_{uuid.uuid4().hex[:8]}"
    update_vars = {
        "id": original_recipe["id"],
        "input": {
            "name": new_name,
            "buildingTypeId": new_building_type_id,
            "outputItemTypeId": new_item_type_id,
            "outputAmount": 10,
            "ingredients": [
                {
                    "itemTypeId": new_item_type_id,
                    "amount": 3
                }
            ]
        }
    }

    response = await test_client.post(
        "/graphql",
        json={"query": RECIPE_UPDATE_MUTATION, "variables": update_vars},
        headers=auth_headers
    )
    updated = response.json()["data"]["recipe"]["update"]

    assert updated["name"] == new_name
    assert updated["outputAmount"] == 10

@pytest.mark.asyncio
async def test_get_recipe_by_id(test_client, auth_headers):
    recipe = await create_recipe(test_client, auth_headers)
    response = await test_client.post(
        "/graphql",
        json={"query": RECIPE_GET_BY_ID_QUERY, "variables": {"id": recipe["id"]}},
        headers=auth_headers
    )
    fetched = response.json()["data"]["recipe"]["byId"]
    assert fetched["id"] == recipe["id"]

@pytest.mark.asyncio
async def test_get_all_recipes(test_client, auth_headers):
    response = await test_client.post(
        "/graphql", json={"query": RECIPE_GET_ALL_QUERY}, headers=auth_headers
    )
    data = response.json()["data"]["recipe"]["all"]
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_delete_recipe(test_client, auth_headers):
    recipe = await create_recipe(test_client, auth_headers)
    response = await test_client.post(
        "/graphql",
        json={"query": RECIPE_DELETE_MUTATION, "variables": {"id": recipe["id"]}},
        headers=auth_headers
    )
    assert response.json()["data"]["recipe"]["delete"] is True
