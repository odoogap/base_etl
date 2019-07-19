# Copyright 2019 - 2019 OdooGap <info@odoogap.com> https://www.odoogap.com
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError

from pprint import pformat


PAGE_SIZE = 500


class EtlRule(models.Model):
    _name = "etl.function"
    _description = "ETL Functions"

    name = fields.Char('Name')
    import_id = fields.Char('Import ID')
    code = fields.Text(string='Python Function Code',
                       help="Write Python code that the action will execute. Some variables are "
                            "available for use; help about python expression is given in the help tab.")

    @api.multi
    def unset_import_id(self):
        self.write({'import_id': False})


class EtlRule(models.Model):
    _name = "etl.rule"
    _description = "ETL Rule"

    DEFAULT_PYTHON_CODE = """# Available variables:
    #  - data: Input data from JSONB
    # To return an action, assign: action = {...}\n\n\n\n"""

    @api.model
    def _select_child_classes(self):
        return [(p, self.env[p]._description) for p in self.env['etl.rule.mixin']._inherit_children]

    sequence = fields.Integer(string='Sequence')
    name = fields.Char('Name')
    process_ids = fields.Many2many('etl.process', 'etl_process_rules_rel', 'rule_id',
                                   'process_id', string='Process', readonly=True)
    type = fields.Selection([
        ('mapping', 'Mapping'),
        ('plugin', 'Plugin')
    ], required=True, default='create')
    code = fields.Text(string='Python Code',
                       default=DEFAULT_PYTHON_CODE,
                       help="Write Python code that the action will execute. Some variables are "
                            "available for use; help about python expression is given in the help tab.")
    etl_plugin = fields.Selection('_select_child_classes', string='Job Class')
    domain = fields.Text(default='[]', required=True, string='Domain', help="Domain for usage in update and delete types.")
    test_result = fields.Text('Last Result')

    @api.multi
    def _run_type_mapping(self, test=False, process_state='new'):
        # TODO: change from a run type to a mapping function usable in a plugin
        self.ensure_one()
        code = self.code
        try:
            EtlFunctions = self.env['etl.function'].search([])
            function_context = {fn.name: eval(fn.code) for fn in EtlFunctions}

            if test:
                InputRecords = self.env['etl.input'].search([
                ], limit=10)
            else:
                InputRecords = self.env['etl.input'].search([
                    ('state', '=', process_state)
                ], limit=PAGE_SIZE)
                InputRecords.write({'state': 'in_process'})
            result = []
            for rec in InputRecords:
                data = safe_eval(rec.json_data)
                function_context.update({'data': data})

                if test:
                    result.append(safe_eval(code, function_context))
                else:
                    self.test_result = safe_eval(code, function_context)

            if test:
                self.test_result = pformat(result, indent=4)
            else:
                InputRecords.write({'state': 'processed'})

        except Exception as e:
            message = (_(u'Unknown error during line total calculation:') + u' %s: %s' % (type(e), e))
            InputRecords.write({'state': 'failed'})
            raise UserError(message)

        return result

    @api.multi
    def _run_type_plugin(self, test=False):
        self.ensure_one()
        res = self.env[self.etl_plugin]._run(test=test)
        self.test_result = res

    @api.multi
    def _run(self, test=False):
        for record in self:
            # TODO: maybe we might need other run types in future
            if record.type == 'plugin':
                record._run_type_plugin(test=test)

    @api.multi
    def run_import(self):
        self._run(test=True)

    @api.multi
    def run_test(self):
        self._run()


class EtlRuleBase(models.AbstractModel):
    _name = "etl.rule.mixin"
    _description = 'This is a Mixin for creating jobs'

    def _run(self):
        pass


class EtlRuleTest(models.AbstractModel):
    _name = 'etl.rule.test01'
    _inherit = ['etl.rule.mixin']
    _description = 'This is a Mixin for creating jobs'

    def _run(self):
        print("test")


