from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Person(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Abstract Person Model'

    name = fields.Char(
        compute='_compute_name',
    )
    last_name = fields.Char()

    first_name = fields.Char()

    phone = fields.Char()

    photo = fields.Image()

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], )

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.first_name} {record.last_name}'

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not re.match(r'^\+?[0-9\s\-]+$', record.phone):
                raise ValidationError('Invalid phone number format')
    # record.name = '%s %s' % (record.first_name, record.last_name
