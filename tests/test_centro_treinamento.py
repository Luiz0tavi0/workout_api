from http import HTTPStatus

import httpx
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)


@pytest.mark.asyncio
async def test_root(client: httpx.AsyncClient):
    response = await client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Tomato'}


@pytest.mark.asyncio
async def test_create_centro_de_treinamento_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    payload = {
        'nome': 'CT Novo',
        'endereco': 'Rua Nova, 456',
        'proprietario': 'Maria',
    }
    response = await client.post('/centros_treinamento/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
