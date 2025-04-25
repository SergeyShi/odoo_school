from odoo.tests.common import HttpCase
from .test_common import TestHRHospitalCommon


class TestHRHospitalHttp(HttpCase, TestHRHospitalCommon):
    """Test HTTP endpoints and controllers"""

    def setUp(self):
        super().setUp()
        # Create a user with specific access rights for HTTP tests
        self.http_user = self.env['res.users'].create({
            'name': 'HTTP Test User',
            'login': 'http_test',
            'password': 'http_test',
            'email': 'http_test@example.com',
            'groups_id': [(4, self.env.ref('hr_hospital.group_hr_hospital_doctor').id)]
        })

    def test_doctor_report_http(self):
        """Test accessing doctor report via HTTP"""
        # Authenticate as the HTTP test user
        self.authenticate('http_test', 'http_test')

        # Access the doctor report URL
        url = f'/web/reports/doctor/{self.doctor.id}'
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.doctor.name, response.text)

    def test_patient_portal_access(self):
        """Test patient portal access"""
        # Create a portal user for the patient
        portal_user = self.env['res.users'].create({
            'name': 'Portal Patient',
            'login': 'portal_patient',
            'password': 'portal_patient',
            'email': 'portal_patient@example.com',
            'groups_id': [(4, self.env.ref('base.group_portal').id)]
        })

        # Link the portal user to the patient
        self.patient.write({'user_id': portal_user.id})

        # Authenticate as the portal user
        self.authenticate('portal_patient', 'portal_patient')

        # Access the patient's own page
        url = f'/my/patient/{self.patient.id}'
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.patient.name, response.text)

        # Try to access another patient's page (should be forbidden)
        url = f'/my/patient/{self.another_patient.id}'
        response = self.url_open(url)
        self.assertEqual(response.status_code, 403)

    def test_doctor_kanban_view_http(self):
        """Test accessing doctor kanban view via HTTP"""
        # Authenticate as the HTTP test user
        self.authenticate('http_test', 'http_test')

        # Access the doctor kanban view URL
        url = '/web#action=hr_hospital.action_hr_hospital_action_window&view_type=kanban'
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)

    def test_visit_calendar_view_http(self):
        """Test accessing visit calendar view via HTTP"""
        # Authenticate as the HTTP test user
        self.authenticate('http_test', 'http_test')

        # Access the visit calendar view URL
        url = '/web#action=hr_hospital.hr_hospital_visit_action&view_type=calendar'
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
