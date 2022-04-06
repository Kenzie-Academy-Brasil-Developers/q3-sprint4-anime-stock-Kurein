from app.models.anime_model import Anime

def KeyError_controller(keys):
    keys_dict = {'keys': Anime().fieldnames[1:], 'wrong_keys': []}
    for key in keys:
        if key not in keys_dict['keys']:
            keys_dict['wrong_keys'].append(key)
    
    return keys_dict
    