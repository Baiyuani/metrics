from __init__ import __version__

app_config = {
    'host': '0.0.0.0',
    'port': 5000,
    'context_path': '/metrics',
    'threading_num': 10,
    'namespace': 'dev',
    'ex_labels': '{version="%s"}' % __version__
}
