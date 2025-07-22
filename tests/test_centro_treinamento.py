from http import HTTPStatus

import httpx
import pytest
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from workout_api.centro_treinamento.models import CentroTreinamentoModel


@pytest.mark.asyncio
async def test_create_training_center_persists_in_db(
    client: httpx.AsyncClient,
    session: AsyncSession,
):
    payload = {
        'nome': 'CT Teste',
        'endereco': 'Rua Exemplo, 789',
        'proprietario': 'João',
    }

    response = await client.post('/centros_treinamento/', json=payload)
    assert response.status_code == HTTPStatus.CREATED
    stmt: Select = select(CentroTreinamentoModel).where(
        CentroTreinamentoModel.nome == 'CT Teste'
    )
    result = await session.execute(stmt)
    ct = result.scalar_one_or_none()
    assert ct is not None
    assert ct.endereco == 'Rua Exemplo, 789'


@pytest.mark.asyncio
async def test_get_training_center_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    response = await client.get('/centros_treinamento/')

    assert response.status_code == HTTPStatus.OK
