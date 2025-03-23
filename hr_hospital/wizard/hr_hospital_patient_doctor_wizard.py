from odoo import models, fields, api


class PatientDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.patient.doctor.wizard'
    _description = 'Wizard for Mass Update of Personal Doctor'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Personal Doctor',
        required=True)

    def action_update_doctor(self):
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            patients = self.env['hr.hospital.patient'].browse(active_ids)
            patients.write({'doctor_id': self.doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}