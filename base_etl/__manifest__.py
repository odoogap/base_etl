{
    'name': 'ETL Base',
    'version': '12.0.0.0.1',
    'category': 'ETL',
    'author': 'Diogo Duarte (ODOOGAP.COM)',
    'website': 'https://www.odoogap.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/etl_input_views.xml',
        'views/etl_rule_views.xml',
        'views/etl_process_views.xml',
        'wizard/multi_action.xml',
        'views/web_widget.xml',
        'views/_menus.xml'  # always last
    ],
    'installable': True,
    'qweb': [
        "static/src/xml/web_widget_jsonb.xml",
    ],
    'license': 'LGPL-3',
}
