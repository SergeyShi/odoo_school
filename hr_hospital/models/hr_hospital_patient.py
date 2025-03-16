import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class HRHPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char(string="Patient name")
    birth_date = fields.Date()
    doctor_id = fields.Many2one('hr.hospital.doctor', string="Doctor")
