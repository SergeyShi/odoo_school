# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields
from odoo.tests import TransactionCase

from odoo.exceptions import ValidationError, AccessError


class TestHRHospitalAll(TransactionCase):
    """Комплексний тестовий клас для модуля hr_hospital з повним покриттям"""

    def setUp(self):
        super().setUp()
        # Створюємо базові записи для тестів
        self.doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'John',
            'last_name': 'Doe',
        })
        self.mentor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Mentor',
            'last_name': 'Doctor',
        })
        self.intern = self.env['hr.hospital.doctor'].create({
            'first_name': 'Intern',
            'last_name': 'Doctor',
            'is_intern': True,
            'mentor_id': self.mentor.id,
        })
        self.patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '+380501234567',
            'birth_date': fields.Date.today() - timedelta(days=365 * 30),
        })
        self.disease = self.env['hr.hospital.disease'].create({
            'name': 'Flu',
        })
        self.visit = self.env['hr.hospital.patient.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': self.disease.id,
            'scheduled_datetime': fields.Datetime.now(),
            'visit_date': fields.Datetime.now(),
            'status': 'planned',
        })

    # Тести для моделі Doctor
    def test_doctor_create(self):
        self.assertEqual(self.doctor.first_name, 'John')
        self.assertEqual(self.doctor.last_name, 'Doe')
        self.assertFalse(self.doctor.is_intern)

    def test_action_create_visit(self):
        action = self.doctor.action_create_visit()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'hr.hospital.patient.visit')
        self.assertEqual(action['context']['default_doctor_id'], self.doctor.id)

    def test_get_report_base_filename(self):
        filename = self.doctor._get_report_base_filename()
        self.assertEqual(filename, 'Doctor_John_Doe')

    def test_check_mentor_assignment(self):
        # Тест для інтерна без ментора
        with self.assertRaises(ValidationError):
            self.env['hr.hospital.doctor'].create({
                'first_name': 'New',
                'last_name': 'Intern',
                'is_intern': True,
            })._check_mentor_assignment()

        # Тест для інтерна як ментора
        with self.assertRaises(ValidationError):
            bad_doctor = self.env['hr.hospital.doctor'].create({
                'first_name': 'Bad',
                'last_name': 'Doctor',
                'mentor_id': self.intern.id,
            })
            bad_doctor._check_mentor_assignment()

        # Тест для коректного призначення ментора
        try:
            self.intern._check_mentor_assignment()
        except ValidationError:
            self.fail("Valid mentor assignment raised ValidationError")

    # Тести для моделі Patient
    def test_patient_create(self):
        self.assertEqual(self.patient.first_name, 'Jane')
        self.assertEqual(self.patient.last_name, 'Smith')
        self.assertEqual(self.patient.age, 30)

    def test_patient_compute_name(self):
        # Тест для пустих значень
        empty_patient = self.env['hr.hospital.patient'].create({})
        self.assertEqual(empty_patient.name, 'None None')

        # Тест для частково заповнених даних
        partial_patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Partial'
        })
        self.assertEqual(partial_patient.name, 'Partial None')

    def test_patient_phone_validation(self):
        # Тест невалідного телефону
        with self.assertRaises(ValidationError):
            self.env['hr.hospital.patient'].create({
                'first_name': 'Invalid',
                'last_name': 'Phone',
                'phone': 'invalid'
            })

    def test_patient_action_open_visits(self):
        action = self.patient.action_open_patient_visits()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertIn(('patient_id', '=', self.patient.id), action['domain'])

    # Тести для моделі Visit
    def test_visit_compute_display_name(self):
        # Тест без дати
        no_date_visit = self.env['hr.hospital.patient.visit'].create({
            'patient_id': self.patient.id,
            'scheduled_datetime': fields.Datetime.now(),
        })
        self.assertIn('New visit', no_date_visit.display_name)

        # Тест без пацієнта
        no_patient_visit = self.env['hr.hospital.patient.visit'].create({
            'visit_date': fields.Datetime.now(),
            'scheduled_datetime': fields.Datetime.now(),
        })
        self.assertIn('None', no_patient_visit.display_name)

    def test_visit_check_modification(self):
        done_visit = self.visit.copy({'status': 'done'})
        done_visit.write({'visit_date': fields.Datetime.now()})  # ensure visit_date is set
        with self.assertRaises(ValidationError):
            done_visit.write({'scheduled_datetime': fields.Datetime.now() + timedelta(days=1)})

    def test_visit_single_per_day(self):
        # Тест дублювання візиту
        with self.assertRaises(ValidationError):
            self.env['hr.hospital.patient.visit'].create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'scheduled_datetime': self.visit.scheduled_datetime,
            })

    # Тести для моделі Disease
    def test_disease_complete_name(self):
        parent = self.env['hr.hospital.disease'].create({'name': 'Parent'})
        child = self.env['hr.hospital.disease'].create({
            'name': 'Child',
            'parent_id': parent.id
        })
        self.assertEqual(child.complete_name, 'Parent / Child')

        # Тест рекурсії
        with self.assertRaises(ValidationError):
            parent.parent_id = child.id
            parent._check_recursion()

    # Тести для моделі Diagnosis
    def test_diagnosis_compute_data(self):
        diagnosis = self.env['hr.hospital.diagnosis'].create({
            'visit_id': self.visit.id,
            'disease_id': self.disease.id,
            'patient_id': self.patient.id,
        })
        self.assertEqual(diagnosis.doctor_id, self.visit.doctor_id)
        self.assertEqual(diagnosis.diagnosis_date, self.visit.scheduled_datetime)

    def test_diagnosis_mentor_approval(self):
        # Тест схвалення без ментора
        diagnosis = self.env['hr.hospital.diagnosis'].create({
            'visit_id': self.visit.id,
            'disease_id': self.disease.id,
            'patient_id': self.patient.id,
            'approved': True
        })

        # Для звичайного лікаря має працювати
        try:
            diagnosis._check_mentor_approval()
        except ValidationError:
            self.fail("Regular doctor approval failed")

        # Для інтерна без ментора
        intern_visit = self.visit.copy({'doctor_id': self.intern.id})
        intern_diagnosis = diagnosis.copy({'visit_id': intern_visit.id})
        with self.assertRaises(ValidationError):
            intern_diagnosis._check_mentor_approval()

    # Тести для Wizard
    def test_patient_doctor_wizard(self):
        wizard = self.env['hr.hospital.patient.doctor.wizard'].create({
            'doctor_id': self.doctor.id,
            'patient_ids': [(6, 0, [self.patient.id])],
        })
        wizard.add_doctor()
        self.assertEqual(self.patient.doctor_id, self.doctor)

    def test_disease_report_wizard(self):
        wizard = self.env['hr.hospital.disease.report.wizard'].create({
            'date_from': '2024-01-01',
            'date_to': '2024-01-31',
        })
        action = wizard.action_generate_report()
        self.assertEqual(action['res_model'], 'hr.hospital.diagnosis')

    def test_disease_report_wizard_action_generate_report_with_doctor(self):
        Wizard = self.env['hr.hospital.disease.report.wizard']
        doctor = self.env['hr.hospital.doctor'].create({'first_name': 'Doc', 'last_name': 'Test'})
        today = fields.Date.today()
        wizard = Wizard.create({
            'date_from': today,
            'date_to': today,
            'doctor_ids': [(6, 0, [doctor.id])],
        })
        action = wizard.action_generate_report()
        domain = action['domain']
        self.assertIn(('doctor_id', 'in', [doctor.id]), domain)

    def test_disease_report_wizard_action_generate_report_with_disease(self):
        Wizard = self.env['hr.hospital.disease.report.wizard']
        disease = self.env['hr.hospital.disease'].create({'name': 'Test Disease'})
        today = fields.Date.today()
        wizard = Wizard.create({
            'date_from': today,
            'date_to': today,
            'disease_ids': [(6, 0, [disease.id])],
        })
        action = wizard.action_generate_report()
        domain = action['domain']
        self.assertIn(('disease_id', 'in', [disease.id]), domain)

    def test_disease_report_wizard_action_generate_report_domain(self):
        Wizard = self.env['hr.hospital.disease.report.wizard']
        today = fields.Date.today()
        wizard = Wizard.create({
            'date_from': today,
            'date_to': today,
        })
        action = wizard.action_generate_report()
        domain = action['domain']
        self.assertIn(('diagnosis_date', '>=', wizard.date_from), domain)
        self.assertIn(('diagnosis_date', '<=', wizard.date_to), domain)

    def test_wizard_check_dates(self):
        Wizard = self.env['hr.hospital.disease.report.wizard']
        with self.assertRaises(Exception):
            Wizard.create({'date_from': fields.Date.today(),
                           'date_to': fields.Date.today().replace(year=fields.Date.today().year - 1)})

    # Тести прав доступу
    def test_access_rights(self):
        demo_user = self.env.ref('base.user_demo')
        with self.assertRaises(AccessError):
            self.patient.with_user(demo_user).write({'last_name': 'Changed'})

    def test_disease_name_create(self):
        Disease = self.env['hr.hospital.disease']
        rec_id, display_name = Disease.name_create('Test Disease')
        rec = Disease.browse(rec_id)
        self.assertEqual(rec.name, 'Test Disease')
        self.assertEqual(display_name, rec.display_name)

    def test_disease_compute_display_name_context(self):
        Disease = self.env['hr.hospital.disease']
        disease = Disease.create({'name': 'Test Disease'})
        # hierarchical_naming = False
        disease.with_context(hierarchical_naming=False)._compute_display_name()
        self.assertEqual(disease.display_name, 'Test Disease')
        # hierarchical_naming = True (default)
        disease.with_context(hierarchical_naming=True)._compute_display_name()
        # display_name має бути як у суперкласі (можна перевірити, що не змінився)

    def test_patient_action_create_visit_no_doctor(self):
        # Видаляємо всіх лікарів
        self.env['hr.hospital.doctor'].search([]).unlink()
        patient = self.env['hr.hospital.patient'].create({'first_name': 'NoDoctor', 'last_name': 'Test'})
        action = patient.action_create_visit()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        # Можна також перевірити, що створено visit з doctor_id == False або None

    def test_patient_compute_name_batch(self):
        Patient = self.env['hr.hospital.patient']
        patients = Patient.new([
            {'first_name': 'Anna', 'last_name': 'Test'},
            {'first_name': 'Bohdan', 'last_name': 'Test2'},
        ])
        patients._compute_name()
        self.assertEqual(patients[0].name, 'Anna Test')
        self.assertEqual(patients[1].name, 'Bohdan Test2')

    def test_cannot_delete_visit_with_diagnosis(self):
        # Створюємо візит
        visit = self.env['hr.hospital.patient.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': self.disease.id,
            'scheduled_datetime': fields.Datetime.now(),
            'visit_date': fields.Datetime.now(),
            'status': 'planned',
        })
        # Додаємо діагноз до візиту
        diagnosis = self.env['hr.hospital.diagnosis'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': self.disease.id,
            'diagnosis_date': fields.Date.today(),
            'visit_id': visit.id,
        })
        # Перевіряємо, що не можна видалити візит із діагнозом
        with self.assertRaises(Exception):
            visit.unlink()
