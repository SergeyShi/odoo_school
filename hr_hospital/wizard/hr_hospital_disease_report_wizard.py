from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Wizard for generating disease report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors')
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases')
    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for record in self:
            if record.date_from > record.date_to:
                raise ValidationError(
                    _("'From Date' cannot be after 'To Date'"))

    def action_generate_report(self):
        self.ensure_one()
        if not self.date_from or not self.date_to:
            raise ValidationError(
                _("Please specify both 'From' and 'To' dates"))

        report_data = {
            'form_data': {
                'date_from': self.date_from.strftime('%Y-%m-%d'),
                'date_to': self.date_to.strftime('%Y-%m-%d'),
                'doctor_names': ', '.join(self.doctor_ids.mapped(
                    'name')) if self.doctor_ids else 'All doctors',
                'disease_names': ', '.join(self.disease_ids.mapped(
                    'complete_name')) if self.disease_ids else 'All diseases',
            },
            'diagnoses': []  # Ensure the key is 'diagnoses'
        }

        domain = [
            ('visit_id.visit_date', '>=', self.date_from),
            ('visit_id.visit_date', '<=', self.date_to)
        ]

        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        for diagnosis in self.env['hr.hospital.diagnosis'].search(domain):
            report_data['diagnoses'].append(
                {
                    'disease_name': diagnosis.disease_id.complete_name,
                    'patient_name': diagnosis.patient_id.name,
                    'doctor_name': diagnosis.visit_id.doctor_id.name,
                    'visit_date': diagnosis.visit_id.visit_date.strftime(
                        '%Y-%m-%d'),
                    'description': diagnosis.description or '-'
                })

        if not report_data['diagnoses']:
            raise ValidationError(
                _("No diagnoses found for the given criteria"))

        return self.env.ref(
            'hr_hospital.hr_hospital_disease_report_wizard').report_action(
            self,
            data=report_data)
