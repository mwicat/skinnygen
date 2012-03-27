import random

import time
from twisted.internet import defer, reactor

def randfloat(min_num, max_num):
    return min_num + random.random() * (max_num-min_num)

def generate_params(action, params_generators):
    params_factory = params_generators[action]
    params = params_factory() if callable(params_factory) else params_factory
    return params

def sleep(tm):
    """Some function that returns a Deferred."""
    d = defer.Deferred()
    reactor.callLater(tm, d.callback, None)
    return d
