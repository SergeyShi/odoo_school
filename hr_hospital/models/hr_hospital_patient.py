from datetime import date
from odoo import models, fields, api


class HRHPatient(models.Model):
    """
    Patient model. Contains personal data, doctor relationship, diagnosis history, and visit history.
    """
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.person'
    _description = 'Patient'

    name = fields.Char(
        compute='_compute_name',
        store=True)

    last_name = fields.Char()

    first_name = fields.Char()

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Related User',
        help='User account linked to this patient')

    birth_date = fields.Date()

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor")

    age = fields.Integer(
        compute="_compute_age",
        store=True)

    diagnosis_history_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='patient_id',
        string="Diagnosis history"
    )

    visit_ids = fields.One2many(
        comodel_name='hr.hospital.patient.visit',
        inverse_name='patient_id',
        string="Visit history"
    )

    passport_data = fields.Char()
    contact_person = fields.Char()

    def action_open_patient_visits(self):
        """
        Opens the visit history for this patient.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit history',
            'res_model': 'hr.hospital.patient.visit',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',
        }

    def action_create_visit(self):
        """
        Creates a new visit for the patient with automatic doctor assignment.
        """
        visit_obj = self.env['hr.hospital.patient.visit']

        doctor = self.env['hr.hospital.doctor'].search([], limit=1)

        new_visit = visit_obj.create({
            'patient_id': self.id,
            'doctor_id': doctor.id,
            'visit_date': fields.Datetime.now(),
            'scheduled_datetime': fields.Datetime.now(),
            'status': 'planned',
        })

        action = {
            'type': 'ir.actions.act_window',
            #'name': 'New visit',
            'res_model': 'hr.hospital.patient.visit',
            'res_id': new_visit.id,
            'view_mode': 'form',
            'target': 'current',
        }

        return action

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        """
        Computes the patient's full name based on first and last name.
        """
        for record in self:
            record.name = f'{record.first_name} {record.last_name}'

    @api.depends('birth_date')
    def _compute_age(self):
        """
        Computes the patient's age based on the birth date.
        """
        for patient in self:
            if patient.birth_date:
                today = date.today()
                patient.age = (today.year - patient.birth_date.year
                               - ((today.month, today.day)
                                  < (patient.birth_date.month,
                                     patient.birth_date.day)))
            else:
                patient.age = 0
