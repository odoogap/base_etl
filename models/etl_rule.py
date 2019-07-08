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
    # Python code
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

    name = fields.Char('Name')
    import_id = fields.Char('Import ID')
    type = fields.Selection([
        ('create', 'Create'),
        ('update', 'Update'),
        ('unlink', 'Delete')], required=True, default='create')
    code = fields.Text(string='Python Code',
                       default=DEFAULT_PYTHON_CODE,
                       help="Write Python code that the action will execute. Some variables are "
                            "available for use; help about python expression is given in the help tab.")
    domain = fields.Text(default='[]', required=True)
    test_result = fields.Text('Last Result')

    @api.multi
    def _run_import(self, process_state='new'):
        self.ensure_one()
        code = self.code
        try:

            EtlFunctions = self.env['etl.function'].search([
            ])

            function_context = {fn.name: eval(fn.code) for fn in EtlFunctions}

            InputRecords = self.env['etl.input'].search([
                ('state', '=', process_state)
            ], limit=PAGE_SIZE)

            InputRecords.write({'state': 'in_process'})

            for rec in InputRecords:
                data = safe_eval(rec.json_data)

                function_context.update({'data': data})
                print(safe_eval(code, function_context))
                self.text_result = safe_eval(code, function_context)
                InputRecords.write({'state': 'processed'})
        except Exception as e:
            message = (_(u'Unknown error during line total calculation:') + u' %s: %s' % (type(e), e))
            InputRecords.write({'state': 'failed'})
            raise UserError(message)

    @api.multi
    def run_import(self):
        for record in self:
            record._run_import()

    @api.multi
    def run_test(self):
        self.ensure_one()
        code = self.code
        try:
            EtlFunctions = self.env['etl.function'].search([
            ])
            function_context = {fn.name: eval(fn.code) for fn in EtlFunctions}
            InputRecords = self.env['etl.input'].search([
            ], limit=10)
            result = []
            for rec in InputRecords:
                data = safe_eval(rec.json_data)
                function_context.update({'data': data})
                result.append(safe_eval(code, function_context))

            self.test_result = pformat(result, indent=4)
        except Exception as e:
            message = (_(u'Unknown error during line total calculation:') + u' %s: %s' % (type(e), e))
            raise UserError(message)

    @api.multi
    def _cron_run_import(self):
        # TODO: to implement
        pass
