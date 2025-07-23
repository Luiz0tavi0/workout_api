import factory
from faker import Faker

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn

fake_pt = Faker('pt_BR')


class CentroTreinamentoBaseFactory(factory.Factory):  # type: ignore
    nome = factory.LazyAttribute(lambda _: fake_pt.company()[:19])
    endereco = factory.LazyAttribute(lambda _: fake_pt.address()[:59])
    proprietario = factory.LazyAttribute(lambda _: fake_pt.name()[:29])


class CentroTreinamentoSchemaFactory(CentroTreinamentoBaseFactory):
    class Meta:
        model = CentroTreinamentoIn


class CentroTreinamentoModelFactory(CentroTreinamentoBaseFactory):
    class Meta:
        model = CentroTreinamentoModel
