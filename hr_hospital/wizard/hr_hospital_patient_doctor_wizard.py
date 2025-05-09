from odoo import models, fields


class PatientWizard(models.TransientModel):
    _name = 'hr.hospital.patient.doctor.wizard'
    _description = 'Patient wizard'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        required=True,
        string='New doctor',
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
    )

    def add_doctor(self):
        self.ensure_one()
        self.patient_ids.write({
            'doctor_id': self.doctor_id.id, })

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['patient_ids'] = [(6, 0, self.env.context.get('active_ids'))]
        return res
