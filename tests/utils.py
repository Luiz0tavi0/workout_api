from faker import Faker

fake_pt = Faker('pt_BR')


def corta(texto: str, limite=20) -> str:
    return texto[:limite]
