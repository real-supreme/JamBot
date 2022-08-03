import json

with open('config.json') as config_file:
    config = json.load(config_file)
    
bot_description = config['description']
default_prefix = config['prefix']
status = config['mode']
bot_activity = config['activity']
    
def get_prefix():
    ...
    # check from database [?]
    return default_prefix

########################################################

def get_token():
    ...
    # use env variable [?]
    
    with open('dot.json') as dot_file:
        dot = json.load(dot_file)
    return dot['token'][::-1]