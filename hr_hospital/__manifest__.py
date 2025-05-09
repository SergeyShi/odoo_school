{
    'name': 'HR Hospital',
    'summary': '',
    'author': 'Serhii',
    'website': 'https://github.com/SergeyShi/odoo_school/',
    'category': 'Human Resources',
    'license': 'OPL-1',
    'version': '17.0.1.1.0',

    'depends': [
        'base',
        'web',
        'website',
    ],

    'external_dependencies': {
        'python': [],
    },
    'data': [
        'security/hr_hospital_groups.xml',
        'views/hr_hospital_menu.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_patient_visit_views.xml',
        'views/hr_hospital_diagnosis_views.xml',
        'security/hr_hospital_security.xml',
        'security/ir.model.access.csv',
        'wizard/hr_hospital_patient_doctor_wizard_views.xml',
        'wizard/hr_hospital_disease_report_wizard_views.xml',

        'data/hr_hospital_disease_data.xml',
        'data/hr_hospital_specialization_data.xml',

        'report/hr_hospital_reports.xml',
    ],
    'demo': [
        'demo/hr_hospital_demo.xml',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],

    # 'assets': {
    # 'web.assets_backend': [
    # 'hr_hospital/static/src/js/phone_mask.js',
    # ],
    # },
}
