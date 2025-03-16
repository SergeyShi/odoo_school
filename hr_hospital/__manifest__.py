{
    'name': 'HR Hospital',
    'summary': '',
    'author': 'Serhii',
    'website': 'https://github.com/SergeyShi/odoo_school/',
    'category': 'Human Resources',
    'license': 'OPL-1',
    'version': '17.0.1.0.0',

    'depends': [
        'base',
                ],

    'external_dependencies': {
        'python': [],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/hr_hospital_menu.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_patient_visit_views.xml',
        'data/hr_hospital_disease_data.xml',
    ],
    'demo': [
        'demo/hr_hospital_demo.xml',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
      ],
}
