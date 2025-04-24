from odoo import models, fields, api, _, ValidationError


class Diagnosis(models.Model):
    """
    Diagnosis model. Contains information about the diagnosis, patient, doctor, date, disease, and approval status.
    """
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    name = fields.Char()

    active = fields.Boolean(
        default=True,
    )

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.patient.visit',
        string="Visit",
        required=True, ondelete='cascade'
    )

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string="Disease",
        required=True
    )

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string="Patient",
        required=True
    )

    diagnosis_date = fields.Datetime(
        compute='_compute_data',
        store=True)

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        compute='_compute_data',
        store=True)

    description = fields.Text()
    approved = fields.Boolean()

    @api.depends('visit_id')
    def _compute_data(self):
        """
        Sets the doctor and diagnosis date based on the related visit.
        """
        for record in self:
            if record.visit_id:
                record.doctor_id = record.visit_id.doctor_id.id
                record.diagnosis_date = record.visit_id.scheduled_datetime

    @api.constrains('approved')
    def _check_mentor_approval(self):
        """
        Ensures that an intern's diagnosis is approved by a mentor.
        """
        for record in self:
            doctor = record.visit_id.doctor_id
            if (doctor.is_intern and record.approved
                    and not doctor.mentor_id):
                raise ValidationError(_("Intern's diagnosis must be approved by a mentor."))
