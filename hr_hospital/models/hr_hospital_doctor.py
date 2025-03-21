from odoo import models, fields


class HRHDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char()
    profession = fields.Char()
