from typing import List, Optional, Sequence
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import (
    CentroTreinamentoIn,
    CentroTreinamentoOut,
)
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo Centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(
        id=uuid4(), **centro_treinamento_in.model_dump()
    )
    centro_treinamento_model = CentroTreinamentoModel(
        **centro_treinamento_out.model_dump()
    )

    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get(
    '/',
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=List[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> List[CentroTreinamentoOut]:
    stmt = select(CentroTreinamentoModel)
    centros_treinamento: Sequence[CentroTreinamentoModel] = (
        await db_session.scalars(stmt)
    ).all()

    # Converter modelos SQLAlchemy para schemas Pydantic
    centros_treinamento_out = [
        CentroTreinamentoOut.model_validate(model)
        for model in centros_treinamento
    ]

    return centros_treinamento_out


@router.get(
    '/{id}',
    summary='Consulta um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(
    id: UUID4, db_session: DatabaseDependency
) -> CentroTreinamentoOut:
    stmt = select(CentroTreinamentoModel).filter_by(id=id)
    result_query = await db_session.execute(stmt)

    centro_treinamento: Optional[CentroTreinamentoModel] = (
        result_query.scalar_one_or_none()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrado no id: {id}',
        )
    centro_treinamento_out = CentroTreinamentoOut.model_validate(
        centro_treinamento
    )
    return centro_treinamento_out
