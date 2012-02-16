import random

def randfloat(min_num, max_num):
    return min_num + random.random() * (max_num-min_num)

def generate_params(action, params_generators):
    params_factory = params_generators[action]
    params = params_factory() if callable(params_factory) else params_factory
    return params
