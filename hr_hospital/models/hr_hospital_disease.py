import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class HRHDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char(string="Disease")
    description = fields.Text()
