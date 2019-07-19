# Copyright 2019 - 2019 OdooGap <info@odoogap.com> https://www.odoogap.com
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import api, fields, models, _


class EtlRuleTest(models.AbstractModel):
    _name = 'etl.rule.test01'
    _inherit = ['etl.rule.mixin']
    _description = 'This is a Mixin for creating jobs -----'

    def _run(self, test=False):
        return "Test mode = %s" % test


class EtlRuleTest(models.AbstractModel):
    _name = 'etl.rule.test02'
    _inherit = ['etl.rule.mixin']
    _description = 'This is a Mixin for creating jobs 2-----'

    def _run(self, test=False):
        return "Test mode 2 = %s" % test


