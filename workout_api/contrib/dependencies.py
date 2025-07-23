from typing import Annotated

from fastapi import Depends
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession

from workout_api.configs.database import get_session

ParamsDependency = Annotated[Params, Depends(Params)]
DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]
