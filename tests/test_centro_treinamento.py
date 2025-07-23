from http import HTTPStatus

import httpx
import pytest
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from tests.factory.centro_treinamento import CentroTreinamentoSchemaFactory
from workout_api.centro_treinamento.models import CentroTreinamentoModel


@pytest.mark.asyncio
async def test_create_training_center_persists_in_db(
    client: httpx.AsyncClient,
    session: AsyncSession,
):
    fake_ct = CentroTreinamentoSchemaFactory().dict()

    response = await client.post('/centros_treinamento/', json=fake_ct)
    assert response.status_code == HTTPStatus.CREATED

    stmt: Select = select(CentroTreinamentoModel).where(
        CentroTreinamentoModel.nome == fake_ct['nome']
    )
    result = await session.execute(stmt)
    ct = result.scalar_one_or_none()

    assert ct is not None
    assert ct.endereco == fake_ct['endereco']
    assert ct.proprietario == fake_ct['proprietario']


@pytest.mark.asyncio
async def test_get_training_center_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    response = await client.get('/centros_treinamento/')

    assert response.status_code == HTTPStatus.OK
