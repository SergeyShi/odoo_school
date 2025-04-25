from datetime import date
from odoo.tests.common import TransactionCase
from odoo import fields


class TestHRHospitalCommon(TransactionCase):
    """Base class for all hr_hospital tests"""

    def setUp(self):
        super().setUp()
        # Create a specialization
        self.specialization = self.env['hr.hospital.specialization'].create({
            'name': 'Cardiology'
        })

        # Create a doctor user
        self.doctor_user = self.env['res.users'].create({
            'name': 'Dr. House',
            'login': 'house',
            'email': 'house@example.com',
        })

        # Create a doctor
        self.doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Gregory',
            'last_name': 'House',
            'user_id': self.doctor_user.id,
            'specialization_id': self.specialization.id,
        })

        # Create a patient user
        self.patient_user = self.env['res.users'].create({
            'name': 'John Doe',
            'login': 'johndoe',
            'email': 'john@example.com',
        })

        # Create a patient
        self.patient = self.env['hr.hospital.patient'].create({
            'first_name': 'John',
            'last_name': 'Doe',
            'birth_date': date(2000, 1, 1),
            'user_id': self.patient_user.id,
            'doctor_id': self.doctor.id,
        })

        # Create a disease
        self.disease = self.env['hr.hospital.disease'].create({
            'name': 'Грип',
        })

        # Create a visit
        self.visit = self.env['hr.hospital.patient.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': self.disease.id,
            'scheduled_datetime': fields.Datetime.now(),
            'visit_date': fields.Datetime.now(),
            'status': 'planned',
        })

        # Create a diagnosis
        self.diagnosis = self.env['hr.hospital.diagnosis'].create({
            'patient_id': self.patient.id,
            'visit_id': self.visit.id,
            'disease_id': self.disease.id,
            'description': 'Test diagnosis',
        })
