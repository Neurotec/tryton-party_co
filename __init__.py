from trytond.pool import Pool
from .models import *


def register():
    Pool.register(
        PartyIdentifier,
        module='party_co', type_='model')
