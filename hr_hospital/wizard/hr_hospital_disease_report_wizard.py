from odoo import models, fields


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Wizard for generating disease report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors')
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',)
    start_date = fields.Date()
    end_date = fields.Date()

    def generate_report(self):
        domain = []
        if self.start_date:
            domain.append(('visit_id.visit_date',
                           '>=', self.start_date))
        if self.end_date:
            domain.append(('visit_id.visit_date',
                           '<=', self.end_date))
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id',
                           'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id',
                           'in', self.disease_ids.ids))

        diagnoses = self.env['hr.hospital.diagnosis'].search(domain)
        #for diagnos in diagnoses:
         #   print(diagnos)
        return diagnoses
