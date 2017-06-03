from trytond.model import fields, ModelSQL, ModelView
from trytond.pool import PoolMeta
import stdnum.co.nit

__all__ = ['PartyIdentifier']


CO_IDENTIFIERS = [
    ('co_vat_1', '1 - No identification'),
    ('co_vat_11', '11 - Birth Certificate'),
    ('co_vat_12', '12 - Identity Card'),
    ('co_vat_13', '13 - Citizenship Card'),
    ('co_vat_21', '21 - Alien Registration Card'),
    ('co_vat_22', '22 - Foreigner ID'),
    ('co_vat_31', '31 - TAX Number (NIT)'),
    ('co_vat_41', '41 - Passport'),
    ('co_vat_42', '42 - Foreign Identification Document'),
    ('co_vat_43', '43 - No Foreign Identification')
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
            if not stdnum.co.nit.is_valid(self.code):
                if self.party and self.party.id > 0:
                    party = self.party.rec_name
                else:
                    party = ''
                    self.raise_user_error('invalid_vat', {
                        'code': self.code,
                        'party': party,
                    })
