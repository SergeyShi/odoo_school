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
        domain = []

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        domain.append(('diagnosis_date', '>=', self.date_from))

        domain.append(('diagnosis_date', '<=', self.date_to))

        return {
            'type': 'ir.actions.act_window',
            'name': f'Disease Report ({self.date_from} to {self.date_to})',
            'res_model': 'hr.hospital.diagnosis',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
            'context': {
                'group_by': 'disease_id',
                'search_default_group_by_disease': True
            }
        }
