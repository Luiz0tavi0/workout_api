import uuid
from http import HTTPStatus

import httpx
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factory.centro_treinamento import (
    CentroTreinamentoModelFactory,
    CentroTreinamentoSchemaFactory,
)
from workout_api.centro_treinamento.models import CentroTreinamentoModel


@pytest.mark.asyncio
async def test_create_centro_treinamento_persists_in_db(
    client: httpx.AsyncClient, session: AsyncSession
):
    payload = CentroTreinamentoSchemaFactory().model_dump()

    response = await client.post('/centros_treinamento/', json=payload)
    assert response.status_code == HTTPStatus.CREATED

    stmt = select(CentroTreinamentoModel).where(
        CentroTreinamentoModel.nome == payload['nome']
    )
    result = await session.execute(stmt)
    ct = result.scalar_one_or_none()

    assert ct is not None
    assert ct.endereco == payload['endereco']
    assert ct.proprietario == payload['proprietario']


@pytest.mark.asyncio
async def test_get_centro_treinamento_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    qtd = 5
    cts = CentroTreinamentoModelFactory.create_batch(qtd)
    session.add_all(cts)
    await session.commit()

    response = await client.get('/centros_treinamento/')
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == qtd


@pytest.mark.asyncio
async def test_get_centro_treinamento_by_id_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    ct = CentroTreinamentoModelFactory()
    session.add(ct)
    await session.commit()

    response = await client.get(f'/centros_treinamento/{ct.id}')
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert content['id'] == str(ct.id)
    assert content['nome'] == ct.nome


@pytest.mark.asyncio
async def test_get_centro_treinamento_by_id_not_found(
    client: httpx.AsyncClient,
):
    fake_id = uuid.uuid4()
    response = await client.get(f'/centros_treinamento/{fake_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'não encontrado' in response.json()['detail']


@pytest.mark.asyncio
@pytest.mark.parametrize('field', ['nome', 'endereco', 'proprietario'])
async def test_create_centro_treinamento_missing_field(
    client: httpx.AsyncClient, field
):
    payload = CentroTreinamentoSchemaFactory().model_dump()
    del payload[field]

    response = await client.post('/centros_treinamento/', json=payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert any(field in str(err['loc']) for err in response.json()['detail'])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('field', 'value'),
    [
        ('nome', 'X' * 51),
        ('endereco', 'Y' * 61),
        ('proprietario', 'Z' * 31),
    ],
)
async def test_create_centro_treinamento_field_length_validation(
    client: httpx.AsyncClient, field, value
):
    payload = CentroTreinamentoSchemaFactory().model_dump()
    payload[field] = f'{payload[field]} {value}'

    response = await client.post('/centros_treinamento/', json=payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    # ipdb.set_trace()
    assert any(field in str(err['loc']) for err in response.json()['detail'])
