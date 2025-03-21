from odoo import models, fields


class HRHDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char()
    description = fields.Text()
