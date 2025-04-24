from odoo import models, fields, api, exceptions, _


class HRHDoctor(models.Model):
    """
    Doctor model for a medical institution. Contains information about the doctor, their specialization, intern status, mentor, and subordinate interns.
    """
    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.person', 'avatar.mixin']
    _description = 'Doctor'

    last_name = fields.Char()

    first_name = fields.Char()
    
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Related User',
        help='User account linked to this doctor')

    specialization_id = fields.Many2one(
        comodel_name='hr.hospital.specialization',
        string="Specialization")

    is_intern = fields.Boolean(string="Intern")

    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor-mentor",
        domain=[('is_intern', '=', False)])

    intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id',
        string='Interns')

    color = fields.Integer("Color Index")

    def action_create_visit(self):
        """
        Creates an action to open the visit creation form with the doctor pre-filled.
        """
        return {
            "type": "ir.actions.act_window",
            "name": "Create Visit",
            "res_model": "hr.hospital.patient.visit",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_doctor_id": self.id,
            },
        }

    def _get_report_base_filename(self):
        """
        Returns the base filename for the doctor's report.
        """
        return f'Doctor_{self.first_name}_{self.last_name}'

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor_assignment(self):
        """
        Checks that an intern has a mentor doctor, and that an intern cannot be a mentor.
        """
        for doctor in self:
            if doctor.is_intern and not doctor.mentor_id:
                raise exceptions.ValidationError(_(
                    "The intern must have a mentor physician."))
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise exceptions.ValidationError(_(
                    "An intern cannot be a mentor."))
