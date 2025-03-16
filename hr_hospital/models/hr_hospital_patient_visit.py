import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class HRHPatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Patient visit'

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string="Patient", required=True)
    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string="Doctor", required=True)
    disease_id = fields.Many2one(
        'hr.hospital.disease',
        string="Disease")
    visit_date = fields.Datetime(
        string="Visit Date",
        default=fields.Datetime.now)
