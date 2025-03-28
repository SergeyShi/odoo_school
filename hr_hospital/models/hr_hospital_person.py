from odoo import models, fields


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
    ],)

    def _compute_name(self):
        for record in self:
            record.name = f'{record.first_name} {record.last_name}'
