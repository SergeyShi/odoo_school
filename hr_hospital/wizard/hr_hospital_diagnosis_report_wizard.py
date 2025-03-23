from odoo import models, fields, api


class DiagnosisReportWizard(models.TransientModel):
    _name = 'hr.hospital.diagnosis.report.wizard'
    _description = 'Wizard for Monthly Disease Report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors')
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases')
    date_from = fields.Date(
        string='From Date',
        required=True)
    date_to = fields.Date(
        string='To Date',
        required=True)

    def action_generate_report(self):
        domain = [('visit_id.date', '>=', self.date_from),
                  ('visit_id.date', '<=', self.date_to)]
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        diagnoses = self.env['hr.hospital.diagnosis'].search(domain)
        return diagnoses
