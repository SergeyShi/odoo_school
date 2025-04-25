from odoo.exceptions import AccessError
from .test_common import TestHRHospitalCommon


class TestHRHospitalAccessRights(TestHRHospitalCommon):
    """Test access rights for different user groups"""

    def setUp(self):
        super().setUp()
        # Create users for different groups
        self.patient_group = self.env.ref('hr_hospital.group_hr_hospital_patient')
        self.intern_group = self.env.ref('hr_hospital.group_hr_hospital_intern')
        self.doctor_group = self.env.ref('hr_hospital.group_hr_hospital_doctor')
        self.manager_group = self.env.ref('hr_hospital.group_hr_hospital_manager')

        # Create another patient user for testing
        self.another_patient_user = self.env['res.users'].create({
            'name': 'Another Patient',
            'login': 'anotherpatient',
            'email': 'another@example.com',
            'groups_id': [(4, self.patient_group.id)]
        })

        # Create another patient
        self.another_patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Another',
            'last_name': 'Patient',
            'birth_date': '2001-02-03',
            'user_id': self.another_patient_user.id,
            'doctor_id': self.doctor.id,
        })

        # Create an intern user
        self.intern_user = self.env['res.users'].create({
            'name': 'Intern User',
            'login': 'intern',
            'email': 'intern@example.com',
            'groups_id': [(4, self.intern_group.id)]
        })

        # Create an intern doctor
        self.intern_doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Intern',
            'last_name': 'Doctor',
            'user_id': self.intern_user.id,
            'specialization_id': self.specialization.id,
            'is_intern': True,
            'mentor_id': self.doctor.id,
        })

        # Add patient group to patient_user
        self.patient_user.write({'groups_id': [(4, self.patient_group.id)]})

        # Add doctor group to doctor_user
        self.doctor_user.write({'groups_id': [(4, self.doctor_group.id)]})

        # Create a diagnosis for another patient
        self.another_visit = self.env['hr.hospital.patient.visit'].create({
            'patient_id': self.another_patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': self.disease.id,
            'scheduled_datetime': '2025-01-01 10:00:00',
            'visit_date': '2025-01-01 10:30:00',
            'status': 'planned',
        })

        self.another_diagnosis = self.env['hr.hospital.diagnosis'].create({
            'patient_id': self.another_patient.id,
            'visit_id': self.another_visit.id,
            'disease_id': self.disease.id,
            'description': 'Another diagnosis',
        })

    def test_patient_access_own_diagnosis(self):
        """Test that patient can access own diagnosis"""
        # Switch to patient user
        diagnosis_model = self.env['hr.hospital.diagnosis'].with_user(self.patient_user)

        # Should be able to read own diagnosis
        diagnosis = diagnosis_model.browse(self.diagnosis.id)
        self.assertEqual(diagnosis.description, 'Test diagnosis')

    def test_patient_cannot_access_other_diagnosis(self):
        """Test that patient cannot access another patient's diagnosis"""
        # Switch to patient user
        diagnosis_model = self.env['hr.hospital.diagnosis'].with_user(self.patient_user)

        # Should not be able to read another patient's diagnosis
        with self.assertRaises(AccessError):
            diagnosis_model.browse(self.another_diagnosis.id).read(['description'])

    def test_patient_cannot_create_diagnosis(self):
        """Test that patient cannot create diagnosis"""
        # Switch to patient user
        diagnosis_model = self.env['hr.hospital.diagnosis'].with_user(self.patient_user)

        # Should not be able to create diagnosis
        with self.assertRaises(AccessError):
            diagnosis_model.create({
                'patient_id': self.patient.id,
                'visit_id': self.visit.id,
                'disease_id': self.disease.id,
                'description': 'New diagnosis',
            })

    def test_doctor_access_patient_diagnosis(self):
        """Test that doctor can access patient diagnosis"""
        # Switch to doctor user
        diagnosis_model = self.env['hr.hospital.diagnosis'].with_user(self.doctor_user)

        # Should be able to read diagnosis
        diagnosis = diagnosis_model.browse(self.diagnosis.id)
        self.assertEqual(diagnosis.description, 'Test diagnosis')

        # Should be able to read another patient's diagnosis
        another_diagnosis = diagnosis_model.browse(self.another_diagnosis.id)
        self.assertEqual(another_diagnosis.description, 'Another diagnosis')

    def test_doctor_can_create_diagnosis(self):
        """Test that doctor can create diagnosis"""
        # Switch to doctor user
        diagnosis_model = self.env['hr.hospital.diagnosis'].with_user(self.doctor_user)

        # Should be able to create diagnosis
        new_diagnosis = diagnosis_model.create({
            'patient_id': self.patient.id,
            'visit_id': self.visit.id,
            'disease_id': self.disease.id,
            'description': 'New doctor diagnosis',
        })
        self.assertEqual(new_diagnosis.description, 'New doctor diagnosis')

    def test_intern_access_rights(self):
        """Test intern access rights"""
        # Create a visit for the intern
        intern_visit = self.env['hr.hospital.patient.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.intern_doctor.id,
            'disease_id': self.disease.id,
            'scheduled_datetime': '2025-02-01 10:00:00',
            'visit_date': '2025-02-01 10:30:00',
            'status': 'planned',
        })

        # Switch to intern user
        visit_model = self.env['hr.hospital.patient.visit'].with_user(self.intern_user)

        # Intern should be able to read own visit
        visit = visit_model.browse(intern_visit.id)
        self.assertEqual(visit.patient_id, self.patient)

        # Intern should not be able to read visits of other doctors
        with self.assertRaises(AccessError):
            visit_model.browse(self.visit.id).read(['status'])
