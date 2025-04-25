from datetime import timedelta
from odoo import fields
from .test_common import TestHRHospitalCommon


class TestHRHospitalAction(TestHRHospitalCommon):
    """Test actions and business logic"""

    def test_doctor_action_create_visit(self):
        """Test doctor action to create a visit"""
        action = self.doctor.action_create_visit()
        self.assertEqual(action['res_model'], 'hr.hospital.patient.visit')
        self.assertEqual(action['context']['default_doctor_id'], self.doctor.id)

    def test_patient_action_create_visit(self):
        """Test patient action to create a visit"""
        visit_action = self.patient.action_create_visit()
        self.assertEqual(visit_action['res_model'], 'hr.hospital.patient.visit')
        visit_id = visit_action.get('res_id')
        visit = self.env['hr.hospital.patient.visit'].browse(visit_id)
        self.assertEqual(visit.patient_id, self.patient)

    def test_patient_action_open_patient_visits(self):
        """Test opening patient visits"""
        action = self.patient.action_open_patient_visits()
        self.assertEqual(action['res_model'], 'hr.hospital.patient.visit')
        self.assertEqual(action['domain'][0][2], self.patient.id)

    def test_patient_visit_check_single_visit_per_day(self):
        """Test constraint: one visit per doctor per day"""
        # Should raise ValidationError if same doctor/patient/visit on same day
        with self.assertRaises(Exception):
            self.env['hr.hospital.patient.visit'].create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'disease_id': self.disease.id,
                'scheduled_datetime': self.visit.scheduled_datetime,
                'visit_date': self.visit.visit_date,
                'status': 'planned',
            })

    def test_patient_visit_create_and_fields(self):
        """Test creating a visit with different date"""
        visit = self.env['hr.hospital.patient.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': self.disease.id,
            'scheduled_datetime': self.visit.scheduled_datetime + timedelta(days=1),
            'visit_date': self.visit.visit_date + timedelta(days=1),
            'status': 'planned',
        })
        self.assertEqual(visit.patient_id, self.patient)
        self.assertEqual(visit.doctor_id, self.doctor)
        self.assertEqual(visit.disease_id, self.disease)

    def test_patient_visit_ondelete_with_diagnosis(self):
        """Test that visit with diagnosis cannot be deleted"""
        # Attempt to delete a visit with a diagnosis should raise an exception
        with self.assertRaises(Exception):
            self.visit.unlink()

    def test_visit_status_change(self):
        """Test changing visit status"""
        # Create a new visit
        visit = self.env['hr.hospital.patient.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': self.disease.id,
            'scheduled_datetime': fields.Datetime.now() + timedelta(days=2),
            'visit_date': fields.Datetime.now() + timedelta(days=2),
            'status': 'planned',
        })

        # Change status to 'done'
        visit.status = 'done'
        self.assertEqual(visit.status, 'done')

        # Change status to 'cancelled'
        visit.status = 'cancelled'
        self.assertEqual(visit.status, 'cancelled')
