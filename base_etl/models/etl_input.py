# Copyright 2019 - 2019 OdooGap <info@odoogap.com> https://www.odoogap.com
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import api, fields, models
from odoo.tools import ustr


class Jsonb(fields._String):
    type = 'jsonb'
    column_type = ('jsonb', 'jsonb')

    def convert_to_cache(self, value, record, validate=True):
        if value is None or value is False:
            return False
        return ustr(value)

    def convert_to_read(self, value, record, use_name_get=True):
        return value

    def convert_to_write(self, value, record):
        return value


fields.Jsonb = Jsonb


class EtlExternal(models.Model):
    _name = "etl.input"
    _description = "Input records"

    name = fields.Char('Import ID')
    state = fields.Selection([
        ('new', 'New'),
        ('failed', 'Failed'),
        ('in_process', 'In Process'),
        ('processed', 'Processed')], required=True, default='new')
    json_data = fields.Jsonb('Json Data')
    json_data_tx = fields.Text('Json Tx Data', compute='_compute_json_data')
    log = fields.Text('Import Log')

    @api.depends('json_data')
    def _compute_json_data(self):
        for record in self:
            record.json_data_tx = record.json_data

    @api.multi
    def validate(self):
        for record in self:
            record.state = "in_process"

    @api.multi
    def done(self):
        for record in self:
            record.state = "processed"

    @api.multi
    def cancel(self):
        for record in self:
            record.state = "new"
