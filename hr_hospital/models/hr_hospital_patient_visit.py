from odoo import models, fields


class HRHPatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Patient visit'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string="Patient")
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor")
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string="Disease")
    visit_date = fields.Datetime(
        string="Visit Date",
        default=fields.Datetime.now)
