# Copyright 2019 - 2019 OdooGap <info@odoogap.com> https://www.odoogap.com
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import api, fields, models, _
import json


class EtlRuleTest(models.AbstractModel):
    _name = 'etl.rule.test01'
    _inherit = ['etl.rule.mixin']
    _description = 'This is a Mixin for creating jobs -----'

    def _run(self, test=False):
        # input_data = self.env['etl.input'].search([('state', '=', 'new')], limit=50)
        input_data = [
            {
                'customer': 'Mark David',
                'type': 'new'
            }, {
                'customer': 'Jane Doe',
                'type': 'new'
            },
        ]

        get_rule = lambda x: self.env['etl.rule'].search([('name', '=', x)])

        rule = get_rule('diamonds_make')

        transform = "{'name': etl_upper(data['customer']), 'state': data['type']}"
        print ("...", rule)
        return "Test mode = %s" % rule._etl_mapping_result(transform, input_data)
