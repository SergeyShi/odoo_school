from odoo import models, fields


class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.patient.visit',
        string="Visit",
        required=True, ondelete='cascade')
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string="Disease",
        required=True)
    description = fields.Text()
    approved = fields.Boolean()
