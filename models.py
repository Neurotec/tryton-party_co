from trytond.model import fields, ModelSQL, ModelView
from trytond.pool import PoolMeta
import stdnum.co.nit

__all__ = ['PartyIdentifier']


CO_IDENTIFIERS = [
    ('co_vat_1', 'No identification'),
    ('co_vat_11', 'Birth Certificate'),
    ('co_vat_12', 'Identity Card'),
    ('co_vat_13', 'Citizenship Card'),
    ('co_vat_22', 'Foreigner ID'),
    ('co_vat_31', 'TAX Number (NIT)'),
    ('co_vat_41', 'Passport'),
    ('co_vat_42', 'Foreign Identification Document'),
    ('co_vat_43', 'No Foreign Identification')
]

class PartyIdentifier(ModelSQL, ModelView):
    "Party Identifier Colombian"
    __name__ = "party.identifier"
    
    @classmethod
    def __setup__(cls):
        super(PartyIdentifier, cls).__setup__()
        cls.type.selection.extend(CO_IDENTIFIERS)

    @classmethod
    def get_types(cls):
        types = super(PartyIdentifier, cls).__setup__()
        types.extend(CO_IDENTIFIERS)
        return types

    @fields.depends('type', 'party', 'code')
    def check_code(self):
        super(PartyIdentifier, self).check_code()
        if self.type == 'co_vat_31':
            #generalizar multiples paises
            #puede ser por el country del party de la company actual
            if not stdnum.co.nit.is_valid(self.code):
                    self.raise_user_error('invalid_vat', {
                        'code': self.code,
                        'party': self.party.rec_name,
                    })
