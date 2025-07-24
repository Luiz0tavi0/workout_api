import uuid
from http import HTTPStatus

import httpx
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factory.categoria import (
    CategoriaModelFactory,
    CategoriaSchemaFactory,
)
from workout_api.categorias.models import CategoriaModel


@pytest.mark.asyncio
async def test_create_categoria_persists_in_db(
    client: httpx.AsyncClient, session: AsyncSession
):
    payload = CategoriaSchemaFactory().model_dump()

    response = await client.post('/categorias/', json=payload)
    assert response.status_code == HTTPStatus.CREATED

    stmt = select(CategoriaModel).where(CategoriaModel.nome == payload['nome'])
    result = await session.execute(stmt)
    categoria = result.scalar_one_or_none()

    assert categoria is not None
    assert categoria.nome == payload['nome']


@pytest.mark.asyncio
async def test_get_categorias_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    qtd = 5
    objs = [CategoriaModelFactory.build() for _ in range(5)]
    session.add_all(objs)
    await session.commit()

    response = await client.get('/categorias/')
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == qtd


@pytest.mark.asyncio
async def test_get_categoria_by_id_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    categoria = CategoriaModelFactory.build()
    session.add(categoria)
    await session.flush()
    # await session.commit()
    response = await client.get(f'/categorias/{categoria.id}')
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert uuid.UUID(content['id']) == categoria.id
    assert content['nome'] == categoria.nome


@pytest.mark.asyncio
async def test_get_categoria_by_id_not_found(client: httpx.AsyncClient):
    fake_id = uuid.uuid4()
    response = await client.get(f'/categorias/{fake_id}')
    detail: str = response.json()['detail']
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'categoria não encontrada' in detail.lower()
