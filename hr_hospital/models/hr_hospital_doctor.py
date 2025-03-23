from odoo import models, fields, api, exceptions


class HRHDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char()
    profession = fields.Char()

    specialization_id = fields.Many2one(
        comodel_name='hr.hospital.specialization',
        string="Спеціальність")
    is_intern = fields.Boolean(string="Інтерн")
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Лікар-ментор",
        domain="[('is_intern', '=', False)]")

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor_assignment(self):
        for doctor in self:
            if doctor.is_intern and not doctor.mentor_id:
                raise exceptions.ValidationError(
                    "Інтерн повинен мати лікаря-ментора.")
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise exceptions.ValidationError(
                    "Інтерн не може бути ментором.")
