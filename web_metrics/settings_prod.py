import os

env = os.environ
app_config = {
    'host': '0.0.0.0',
    'port': env.get('WM_PORT', 5000),
    'context_path': env.get('WM_PATH', '/metrics'),
    'threading_num': env.get('WM_THREADING_NUM', 10),
    'namespace': env.get('NAMESPACE', 'default'),
    'ex_labels': env.get('EX_LABELS')
}


