from datetime import date
from odoo.tests.common import Form
from .test_common import TestHRHospitalCommon


class TestHRHospitalForm(TestHRHospitalCommon):
    """Test form views and model fields"""

    def test_patient_compute_name(self):
        """Test that patient name is computed correctly"""
        self.assertEqual(self.patient.name, 'John Doe')

    def test_patient_compute_age(self):
        """Test that patient age is computed correctly"""
        expected_age = date.today().year - 2000 - ((date.today().month, date.today().day) < (1, 1))
        self.assertEqual(self.patient.age, expected_age)

    def test_disease_complete_name(self):
        """Test that disease complete name is computed correctly"""
        # Create a parent disease
        parent = self.env['hr.hospital.disease'].create({'name': 'Вірусні'})
        child = self.env['hr.hospital.disease'].create({'name': 'Грип', 'parent_id': parent.id})
        child._compute_complete_name()
        self.assertEqual(child.complete_name, 'Вірусні / Грип')

    def test_diagnosis_compute_data(self):
        """Test that diagnosis data is computed correctly"""
        self.diagnosis._compute_data()
        self.assertEqual(self.diagnosis.doctor_id, self.visit.doctor_id)
        self.assertEqual(self.diagnosis.diagnosis_date, self.visit.scheduled_datetime)

    def test_patient_create_and_fields(self):
        """Test creating a patient and checking fields"""
        patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Anna',
            'last_name': 'Ivanova',
            'phone': '+380501234567',
            'contact_person': 'Mother',
        })
        self.assertEqual(patient.name, 'Anna Ivanova')
        self.assertEqual(patient.phone, '+380501234567')
        self.assertEqual(patient.contact_person, 'Mother')

    def test_patient_diagnosis_history(self):
        """Test that diagnosis is added to patient history"""
        self.assertIn(self.diagnosis, self.patient.diagnosis_history_ids)

    def test_patient_visit_compute_display_name(self):
        """Test that visit display name is computed correctly"""
        self.visit._compute_display_name()
        self.assertIn(self.patient.name, self.visit.display_name)

    def test_form_patient(self):
        """Test patient form view"""
        # Use Form to simulate user input in the form
        with Form(self.env['hr.hospital.patient']) as form:
            form.first_name = 'Test'
            form.last_name = 'Patient'
            form.birth_date = date(1990, 5, 15)
            form.doctor_id = self.doctor
            form.phone = '+380991234567'

        patient = form.save()
        self.assertEqual(patient.name, 'Test Patient')
        self.assertEqual(patient.doctor_id, self.doctor)

    def test_form_doctor(self):
        """Test doctor form view"""
        with Form(self.env['hr.hospital.doctor']) as form:
            form.first_name = 'New'
            form.last_name = 'Doctor'
            form.specialization_id = self.specialization
            form.is_intern = True

        doctor = form.save()
        self.assertEqual(doctor.name, 'New Doctor')
        self.assertEqual(doctor.specialization_id, self.specialization)
        self.assertTrue(doctor.is_intern)
