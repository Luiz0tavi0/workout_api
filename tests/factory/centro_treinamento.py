import textwrap

import factory
from faker import Faker

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn

fake_pt = Faker('pt_BR')


def corta(texto: str, limite: int = 20) -> str:
    return textwrap.shorten(texto, width=limite, placeholder='')


class CentroTreinamentoBaseFactory(factory.Factory):
    nome = factory.Sequence(lambda n: corta(f"{fake_pt.company()} {n}"))
    endereco = factory.LazyAttribute(lambda _: corta(fake_pt.address(), 60))
    proprietario = factory.LazyAttribute(lambda _: corta(fake_pt.name(), 30))


class CentroTreinamentoSchemaFactory(CentroTreinamentoBaseFactory):
    class Meta:
        model = CentroTreinamentoIn


class CentroTreinamentoModelFactory(CentroTreinamentoBaseFactory):
    class Meta:
        model = CentroTreinamentoModel
