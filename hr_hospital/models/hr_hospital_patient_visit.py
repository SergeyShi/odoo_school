from odoo import models, fields, api, exceptions


class HRHPatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Patient visit'

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
        string="Visit Date",
        default=fields.Datetime.now)

    status = fields.Selection([
        ('planned', 'Заплановано'),
        ('done', 'Завершено'),
        ('cancelled', 'Скасовано')
    ], string="Статус",
        default='planned', required=True)

    scheduled_datetime = fields.Datetime(
        string="Запланована дата та час",
        required=True)
    actual_datetime = fields.Datetime(string="Дата та час візиту")
    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='visit_id',
        string="Діагнози")

    @api.constrains('actual_datetime', 'doctor_id')
    def _check_visit_modification(self):
        for visit in self:
            if visit.actual_datetime and (
                    visit.scheduled_datetime or visit.doctor_id):
                raise exceptions.ValidationError(
                    "Неможливо змінити дату, час або лікаря після завершення візиту.")

    @api.constrains('diagnosis_ids')
    def _check_delete_archival(self):
        for visit in self:
            if visit.diagnosis_ids:
                raise exceptions.ValidationError(
                    "Неможливо видалити або архівувати візит з діагнозами.")

    @api.constrains('scheduled_datetime', 'doctor_id', 'patient_id')
    def _check_single_visit_per_day(self):
        for visit in self:
            same_day_visits = self.search([
                ('scheduled_datetime', '>=',
                 visit.scheduled_datetime.replace(hour=0, minute=0, second=0)),
                ('scheduled_datetime', '<',
                 visit.scheduled_datetime.replace(hour=23, minute=59,
                                                  second=59)),
                ('doctor_id', '=', visit.doctor_id.id),
                ('patient_id', '=', visit.patient_id.id),
                ('id', '!=', visit.id)
            ])
            if same_day_visits:
                raise exceptions.ValidationError(
                    "Пацієнт не може записатися до одного лікаря більше ніж один раз на день.")