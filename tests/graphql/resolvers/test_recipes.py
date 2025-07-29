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
            "name": generate_unique_name("Item"),
            "durability": 100
        }
    }

    data = await graphql_post(test_client, ITEMTYPE_CREATE_MUTATION, variables, auth_headers)

    return data["data"]["itemType"]["create"]["id"]

async def create_building_type(test_client, auth_headers):
    variables = {
        "input": {
            "name": generate_unique_name("Building"),
            "health": 100,
            "buildingRecipes": []
        }
    }

    data = await graphql_post(test_client, BUILDINGTYPE_CREATE_MUTATION, variables, auth_headers)

    return data["data"]["buildingType"]["create"]["id"]

async def create_recipe(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    building_type_id = await create_building_type(test_client, auth_headers)
    variables = {
        "input": {
            "name": generate_unique_name("Recipe"),
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

    data = await graphql_post(test_client, RECIPE_CREATE_MUTATION, variables, auth_headers)

    return data["data"]["recipe"]["create"]

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

    new_name = generate_unique_name("UpdatedRecipe")
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

    data = await graphql_post(test_client, RECIPE_UPDATE_MUTATION, update_vars, auth_headers)
    updated = data["data"]["recipe"]["update"]

    assert updated["name"] == new_name
    assert updated["outputAmount"] == 10

@pytest.mark.asyncio
async def test_get_recipe_by_id(test_client, auth_headers):
    recipe = await create_recipe(test_client, auth_headers)

    data = await graphql_post(test_client, RECIPE_GET_BY_ID_QUERY, {"id": recipe["id"]}, auth_headers)
    fetched = data["data"]["recipe"]["byId"]

    assert fetched["id"] == recipe["id"]

@pytest.mark.asyncio
async def test_get_all_recipes(test_client, auth_headers):
    data = await graphql_post(test_client, RECIPE_GET_ALL_QUERY, headers=auth_headers)
    data = data["data"]["recipe"]["all"]

    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_delete_recipe(test_client, auth_headers):
    recipe = await create_recipe(test_client, auth_headers)

    data = await graphql_post(test_client, RECIPE_DELETE_MUTATION, {"id": recipe["id"]}, auth_headers)

    assert data["data"]["recipe"]["delete"] is True

@pytest.mark.asyncio
async def test_create_recipe_invalid_input(test_client, auth_headers):
    data = await graphql_post(test_client, RECIPE_CREATE_MUTATION, {"input": {}}, auth_headers)

    assert_error_contains(data, "field")

@pytest.mark.asyncio
async def test_update_recipe_invalid_id(test_client, auth_headers):
    item_type_id = await create_item_type(test_client, auth_headers)
    building_type_id = await create_building_type(test_client, auth_headers)
    fake_id = str(uuid.uuid4())

    update_vars = {
        "id": fake_id,
        "input": {
            "name": "InvalidUpdate",
            "buildingTypeId": building_type_id,
            "outputItemTypeId": item_type_id,
            "outputAmount": 10,
            "ingredients": [{"itemTypeId": item_type_id, "amount": 1}]
        }
    }

    data = await graphql_post(test_client, RECIPE_UPDATE_MUTATION, update_vars, auth_headers)
    
    assert_error_contains(data, "not found")

@pytest.mark.asyncio
async def test_delete_recipe_invalid_id(test_client, auth_headers):
    fake_id = str(uuid.uuid4())

    data = await graphql_post(test_client, RECIPE_DELETE_MUTATION, {"id": fake_id}, auth_headers)
    
    assert_error_contains(data, "not found")

@pytest.mark.asyncio
async def test_get_recipe_by_id_malformed_uuid(test_client, auth_headers):
    data = await graphql_post(test_client, RECIPE_GET_BY_ID_QUERY, {"id": "invalid-uuid"}, auth_headers)
    
    assert_error_contains(data, "uuid")

@pytest.mark.asyncio
async def test_get_all_recipes_unauthenticated(test_client):
    data = await graphql_post(test_client, RECIPE_GET_ALL_QUERY)
    
    assert_error_contains(data, "authorization required")