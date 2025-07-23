from http import HTTPStatus
from uuid import UUID, uuid4

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factory.atleta import AtletaModelFactory, AtletaSchemaFactory
from tests.factory.categoria import CategoriaModelFactory
from tests.factory.centro_treinamento import CentroTreinamentoModelFactory


@pytest.mark.asyncio
async def test_post_atleta_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    categoria = CategoriaModelFactory.build()
    centro = CentroTreinamentoModelFactory.build()
    session.add_all([categoria, centro])
    await session.flush()

    atleta_payload = AtletaSchemaFactory(
        categoria={'nome': categoria.nome},
        centro_treinamento={'nome': centro.nome},
    ).model_dump()

    response = await client.post('/atletas/', json=atleta_payload)
    data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert data['nome'] == atleta_payload['nome']
    assert UUID(data['id'])


@pytest.mark.asyncio
async def test_post_atleta_categoria_not_found(
    client: httpx.AsyncClient, session: AsyncSession
):
    categoria = CategoriaModelFactory.build()
    centro = CentroTreinamentoModelFactory.build()
    session.add_all([categoria, centro])
    await session.flush()
    atleta_payload = AtletaSchemaFactory(
        categoria={'nome': 'inexiste'},
        centro_treinamento={'nome': centro.nome},
    ).model_dump()

    response = await client.post('/atletas/', json=atleta_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'categoria' in response.json()['detail']


@pytest.mark.asyncio
async def test_get_atletas_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    qtd = 15
    size = 10
    n_page = 1

    atletas = []
    for _ in range(qtd):
        atleta = AtletaModelFactory.build()
        session.add(atleta.categoria)
        session.add(atleta.centro_treinamento)
        session.add(atleta)
        atletas.append(atleta)

    await session.commit()

    response = await client.get(
        '/atletas/', params={'page': n_page, 'size': size}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data['items']
    assert len(data['items']) == size
    assert data['total'] == qtd
    assert data['page'] == n_page
    assert data['size'] == size


@pytest.mark.asyncio
async def test_get_atleta_by_id_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    atleta = AtletaModelFactory.create()
    await session.flush()

    response = await client.get(f'/atletas/{atleta.id}')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == str(atleta.id)


@pytest.mark.asyncio
async def test_get_atleta_by_id_not_found(client: httpx.AsyncClient):
    id_errado = str(uuid4())
    response = await client.get(f'/atletas/{id_errado}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'não encontrado' in response.json()['detail']


@pytest.mark.asyncio
async def test_patch_atleta_success(
    client: httpx.AsyncClient, session: AsyncSession
):
    atleta = AtletaModelFactory.create()
    await session.commit()
    patch_data = {'nome': 'Nome Atualizado'}
    response = await client.patch(
        f'/atletas/{str(atleta.id)}', json=patch_data
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['nome'] == patch_data['nome']


@pytest.mark.asyncio
async def test_patch_atleta_not_found(client: httpx.AsyncClient):
    patch_data = {'nome': 'Nome Atualizado'}
    id_errado = str(uuid4())
    response = await client.patch(
        f'/atletas/{str(id_errado)}', json=patch_data
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_atleta_success(client, session):
    atleta = AtletaModelFactory.create()
    await session.commit()

    response = await client.delete(f'/atletas/{atleta.id}')
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_atleta_not_found(client: httpx.AsyncClient):
    id_errado = uuid4()
    response = await client.delete(f'/atletas/{id_errado}')
    assert response.status_code == HTTPStatus.NOT_FOUND
