# src/workers/seed.py
from __future__ import annotations

import pathlib
import hashlib
import yaml

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import get_db
from src.database.services import (
    ItemTypeService, 
    StructureTypeService, 
    BotTypeService, 
    BotRecipeService, 
    BuildingTypeService
)

from src.database.models import SeedMeta

async def _already_applied(db, sha):
    result = await db.execute(select(SeedMeta).where(SeedMeta.file_sha == sha))
    return result.scalar_one_or_none() is not None


async def _mark_applied(db: AsyncSession, sha: str, path: pathlib.Path) -> None:
    db.add(SeedMeta(file_sha=sha, file_path=str(path)))

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()


def _file_sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


async def seed_item_types(file: pathlib.Path) -> None:
    sha = _file_sha256(file)

    async for db in get_db():
        if await _already_applied(db, sha):
            print(f"✔ ItemType seed already applied: {sha[:7]}")
            return

        payload = yaml.safe_load(file.read_text())
        items = payload.get("items", [])

        # Upsert each item
        for raw in items:
            await ItemTypeService.upsert_from_dict(db, raw)

        await _mark_applied(db, sha, file)
        await db.commit()
        print(f"✔ Seeded {len(items)} item types (hash {sha[:7]})")


async def seed_structure_types(file: pathlib.Path) -> None:
    sha = _file_sha256(file)

    async for db in get_db():
        if await _already_applied(db, sha):
            print(f"✔ StructureType seed already applied: {sha[:7]}")
            return

        payload = yaml.safe_load(file.read_text())
        structs = payload.get("structures", [])

        for raw in structs:
            item_type_name = raw.pop("item_type")
            item_type_row = await ItemTypeService.get_by_name(db, item_type_name)
            if item_type_row is None:
                raise RuntimeError(f'ItemType "{item_type_name}" not found')
            raw["item_type_id"] = item_type_row.id

            engage_name = raw.pop("item_to_engage", None)
            if engage_name:
                engage_row = await ItemTypeService.get_by_name(db, engage_name)
                if engage_row is None:
                    raise RuntimeError(f'ItemType "{engage_name}" not found')
                raw["item_to_engage_id"] = engage_row.id
            else:
                raw["item_to_engage_id"] = None

            await StructureTypeService.upsert_from_dict(db, raw)

        await _mark_applied(db, sha, file)
        await db.commit()
        print(f"✔ Seeded {len(structs)} structure types (hash {sha[:7]})")


async def seed_bot_types(file: pathlib.Path) -> None:
    sha = _file_sha256(file)

    async for db in get_db():
        if await _already_applied(db, sha):
            print(f"✔ BotType seed already applied: {sha[:7]}")
            return

        payload = yaml.safe_load(file.read_text())
        bots = payload.get("bots", [])

        for raw in bots:
            # Extract and transform recipe info
            raw_recipes = raw.pop("recipes", [])
            recipe_models = []

            for r in raw_recipes:
                item_type_name = r.get("item_type")
                item_type = await ItemTypeService.get_by_name(db, item_type_name)
                if item_type is None:
                    raise RuntimeError(f'ItemType "{item_type_name}" not found')

                recipe_models.append({
                    "item_type_id": item_type.id,
                    "amount": r["amount"],
                })

            # Create BotType
            bottype = await BotTypeService.upsert_from_dict(db, {
                "name": raw["name"],
                "health": raw["health"],
                "strength": raw["strength"],
                "speed": raw["speed"],
                "vision": raw["vision"],
            })

            if bottype:
                for r in recipe_models:
                    await BotRecipeService.create(
                        db=db,
                        bot_type_id=bottype.id,
                        item_type_id=r["item_type_id"],
                        amount=r["amount"]
                    )

        await _mark_applied(db, sha, file)
        await db.commit()
        print(f"✔ Seeded {len(bots)} bot types (hash {sha[:7]})")

async def seed_building_types(file: pathlib.Path) -> None:
    sha = _file_sha256(file)

    async for db in get_db():
        if await _already_applied(db, sha):
            print(f"✔ BuildingType seed already applied: {sha[:7]}")
            return

        payload = yaml.safe_load(file.read_text())
        buildings = payload.get("buildings", [])

        for raw in buildings:
            await BuildingTypeService.upsert_from_dict(db, raw)

        await _mark_applied(db, sha, file)
        await db.commit()
        print(f"✔ Seeded {len(buildings)} building types (hash {sha[:7]})")

async def run_all_seeds(seed_dir: pathlib.Path) -> None:
    await seed_item_types(seed_dir / "items.yaml")
    await seed_structure_types(seed_dir / "structures.yaml")
    await seed_bot_types(seed_dir / "bots.yaml")
    await seed_building_types(seed_dir / "buildings.yaml")