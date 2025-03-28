from odoo import models, fields, api, exceptions


class HRHDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.person'
    _description = 'Doctor'

    name = fields.Char()
    last_name = fields.Char()
    first_name = fields.Char()

    specialization_id = fields.Many2one(
        comodel_name='hr.hospital.specialization',
        string="Specialization")

    is_intern = fields.Boolean(string="Intern")

    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor-mentor",
        domain=[('is_intern', '=', False)])

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor_assignment(self):
        for doctor in self:
            if doctor.is_intern and not doctor.mentor_id:
                raise exceptions.ValidationError_(
                    "The intern must have a mentor physician.")
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise exceptions.ValidationError_(
                    "An intern cannot be a mentor.")
