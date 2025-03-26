from odoo import models, fields


class HRHSpecialization(models.Model):
    _name = 'hr.hospital.specialization'
    _description = 'Doctor Specialization'

    name = fields.Char(
        string="Specialization",
        required=True)
