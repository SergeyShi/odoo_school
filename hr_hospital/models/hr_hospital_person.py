from odoo import models, fields


class Person(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Abstract Person Model'

    last_name = fields.Char(
        string="Surname",
        required=True)
    first_name = fields.Char(
        string="Name",
        required=True)
    phone = fields.Char(string="Phone")
    photo = fields.Image(string="Photo")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender", required=True)
