import yaml

configs = {}
cfg={}
LOG_PATH='/log'
ENV='beta'

def init(config_file='./config.yaml'):
    global cfg
    global LOG_PATH
    global ENV
    global cfg
    configs = load(config_file)
    ENV = configs['env']
    cfg = configs[ENV]
    LOG_PATH = cfg['LOG_PATH']

def load(config_file='./config.yaml'):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

