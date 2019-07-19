# Copyright 2019 - 2019 OdooGap <info@odoogap.com> https://www.odoogap.com
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EtlProcess(models.Model):
    _name = "etl.process"
    _description = "ETL Process"

    name = fields.Char('Name')
    rule_ids = fields.Many2many('etl.rule', 'etl_process_rules_rel', 'process_id', 'rule_id', string='Rules')
    cron_id = fields.Many2one('ir.cron', string='Cron Job', help="Scheduler which runs on etl")
    interval_number = fields.Integer(string='Cron Interval', default=1)
    interval_type = fields.Selection([('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months')], string='Interval Unit', default='months')
    exec_init = fields.Integer(string='Cron Runs')
    date_init = fields.Datetime(string='First Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    state = fields.Selection([('draft', 'Draft'), ('running', 'Running'), ('done', 'Done')], string='Status', copy=False, default='draft')

    @api.multi
    def set_process(self):
        for process in self:
            cron_data = {
                'name': process.name,
                'interval_number': process.interval_number,
                'interval_type': process.interval_type,
                'numbercall': process.exec_init,
                'nextcall': process.date_init,
                'model': self._name,
                'args': repr([[process.id]]),
                'function': '_cron_run_process',
                'priority': 6,
                'user_id': process.user_id.id
            }
            cron = self.env['ir.cron'].sudo().create(cron_data)
            process.write({'cron_id': cron.id, 'state': 'running'})

    @api.multi
    def unlink(self):
        if any(self.filtered(lambda s: s.state == "running")):
            raise UserError(_('You cannot delete an active ETL process!'))
        return super(EtlProcess, self).unlink()

    @api.multi
    def set_done(self):
        self.mapped('cron_id').write({'active': False})
        self.write({'state': 'done'})

    @api.multi
    def set_draft(self):
        self.write({'state': 'draft'})
