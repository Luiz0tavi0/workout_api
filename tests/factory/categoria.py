# pyright: reportAttributeAccessIssue=false
# pyright: reportPrivateImportUsage=false
import factory
from utils import fake_pt

from tests.utils import corta
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn


class CategoriaBaseFactory(factory.Factory):
    nome = factory.Sequence(lambda n: corta(f'{fake_pt.name()}_{n}', 10))


class CategoriaSchemaFactory(CategoriaBaseFactory):
    class Meta:  # type: ignore[attr-defined]
        model = CategoriaIn


class CategoriaModelFactory(
    factory.alchemy.SQLAlchemyModelFactory, CategoriaBaseFactory
):
    class Meta:  # type: ignore[attr-defined]
        model = CategoriaModel
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'flush'
