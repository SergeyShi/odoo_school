from odoo import models, fields, api


class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.patient.visit',
        string="Візит",
        required=True, ondelete='cascade')
    disease = fields.Char(required=True)
    description = fields.Text()
    approved = fields.Boolean()
