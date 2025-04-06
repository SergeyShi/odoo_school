from odoo import models, fields, api, exceptions, _


class HRHPatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Patient visit'
    _rec_name = 'display_name'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string="Patient")

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor")

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string="Disease")

    visit_date = fields.Datetime(
        string="Date and time visit")

    status = fields.Selection([
        ('planned', 'Planned'),
        ('done', 'End'),
        ('cancelled', 'Cancelled')
    ], string="Visit status",
        default='planned', required=True)

    scheduled_datetime = fields.Datetime(
        string="Scheduled date",
        required=True)

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='visit_id',
        string="Diagnosis")

    @api.depends("patient_id", "visit_date")
    def _compute_display_name(self):
        for rec in self:
            date_str = rec.visit_date.strftime(
                "%d-%m-%Y %H:%M") if rec.visit_date else "New visit"
            patient_name = rec.patient_id.name if rec.patient_id else ""
            rec.display_name = f"{date_str} - {patient_name}"

    @api.constrains('visit_date', 'doctor_id')
    def _check_visit_modification(self):
        if self.status == 'done':
            for visit in self:
                if visit.visit_date and (
                        visit.scheduled_datetime or visit.doctor_id):
                    raise exceptions.ValidationError(_(
                        "Can't change time or doctor"))

    @api.constrains('scheduled_datetime', 'doctor_id', 'patient_id')
    def _check_single_visit_per_day(self):
        for visit in self:
            same_day_visits = self.search([
                ('scheduled_datetime', '>=',
                 visit.scheduled_datetime.replace(
                     hour=0,
                     minute=0,
                     second=0)),
                ('scheduled_datetime', '<',
                 visit.scheduled_datetime.replace(
                     hour=23,
                     minute=59,
                     second=59)),
                ('doctor_id', '=', visit.doctor_id.id),
                ('patient_id', '=', visit.patient_id.id),
                ('id', '!=', visit.id)
            ])
            if same_day_visits:
                raise exceptions.ValidationError(_(
                    "A patient cannot make a visit with the same doctor more than once a day."))

    @api.ondelete(at_uninstall=False)
    def _check_delete_archival(self):
        for visit in self:
            if visit.diagnosis_ids:
                raise exceptions.ValidationError(_(
                    "Can't delete or archive visits with diagnosis."))
