from datetime import date
from odoo import models, fields, api


class HRHPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.person'
    _description = 'Patient'

    name = fields.Char(required=True)
    birth_date = fields.Date()
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor")
    age = fields.Integer(
        string="Вік",
        compute="_compute_age", store=True)
    passport_data = fields.Char()
    contact_person = fields.Char()

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                today = date.today()
                patient.age = today.year - patient.birth_date.year - ((today.month, today.day) < (patient.birth_date.month, patient.birth_date.day))
            else:
                patient.age = 0
