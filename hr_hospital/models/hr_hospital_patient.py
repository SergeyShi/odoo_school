from odoo import models, fields


class HRHPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char(required=True)
    birth_date = fields.Date()
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor")
