from twisted.internet import defer
from threading import Event
from generators import *

from util import generate_params, sleep
from collections import defaultdict
from itertools import repeat, takewhile

from twisted.internet import reactor

INSIDE_DIAL_TONE = 0x21
INTER_CALL_TIME = 3
SLEEP_TIME = 1

import logging
log = logging.getLogger(__name__)

USER_GENERATORS = {
    'idle': (iter, [lambda: weighted_choice([('sleep', 0.8), ('dnd', 0.2)]), None]),
    'random': (general_generator, [])
    }

CALL_ACTIONS = {
    'autoanswer': ['answer'],
    'autotransfer': ['answer', 'dial', 'transfer'],
    'aggressive': ['dial', 'answer']
    }

def create_user_generator(generator_name):
    generator_func, args = USER_GENERATORS[generator_name]
    print generator_func, args
    generator = generator_func(*args)
    return generator

def get_call_actions(actions_name):
    return CALL_ACTIONS[actions_name]


def find_first_common_element(actions_to_fire, actions):
    for action in actions_to_fire:
        if action in actions:
            return action
    return None


class Actor:

    def __init__(self):
        self.running = False

    def start(self):
        reactor.callLater(0, self.run)

    def stop(self):
        self.running = False
        if self.delayed_call is not None:
            self.delayed_call.cancel()

    @defer.inlineCallbacks
    def sleep(self, tm):
        self.delayed_call = sleep(SLEEP_TIME)
        yield self.delayed_call
        self.delayed_call = None


class UserActor(Actor):

    def __init__(self, action_cb, action_generator, params_generators, id):
        Actor.__init__(self)
        self.action_generator = action_generator
        self.params_generators = params_generators
        self.action_cb = action_cb
        self.id = id
        self.did_call = False
        self.delayed_call = None
        self.last_action = None

    def log(self, msg):
        return 'user %s - %s' % (self.id, msg)

    @defer.inlineCallbacks
    def fire_action(self, action, params):
        log.info(self.log('last action %s action %s' % (self.last_action, action)))
        if action == 'sleep':
            yield self.sleep(SLEEP_TIME)
            log.info(self.log('woke up from sleep'))
        else:
            self.action_cb(self.id, action, params)

    def maybe_override_action(self, action):
        is_repeated_newcall = action == 'newcall' and self.last_action == 'newcall'
        if is_repeated_newcall:
            return 'sleep'
        else:
            return action

    @defer.inlineCallbacks
    def run(self):
        self.running = True
        for action in takewhile(lambda a: self.running, self.action_generator):
            log.info(self.log('action %s' % action))
            action = self.maybe_override_action(action)
            params = generate_params(action, self.params_generators)
            yield self.fire_action(action, params)
            self.last_action = action


class CallActor(Actor):

    lines_calls = defaultdict(list)

    def __init__(self, action_cb, params_generators, actions, line, id):
        Actor.__init__(self)
        self.params_generators = params_generators
        self.action_cb = action_cb
        self.call_actor = None
        self.sane = True
        self.line = line
        self.id = id
        self.actions_to_do = actions
        self.dial_counter = 0
        self.transfer_counter = 0
        self.lines_calls[line].append(id)
        self.got_tone = False

    def call_action(self, action, params):
        self.action_cb(action, params, self.line, self.id)

    def log(self, msg):
        return 'call %s - %s' % (self.id, msg)

    @defer.inlineCallbacks
    def on_actions(self, actions):
        #self.maybe_go_insane()
        if not self.sane:
            return

        log.info(self.log('actions: %s' % actions))
        action = find_first_common_element(self.actions_to_do, actions)

        if action == 'dial':
            if self.dial_counter >= 1:
                return
            self.dial_counter += 1

        if action == 'transfer':
            if self.transfer_counter >= 1 or len(CallHandler.lines_calls) < 2:
                return
            self.transfer_counter += 1

        if self.dial_counter > 50:
            print 'OVERFLOW========================================='
            import sys; sys.exit(1)

        if action is not None:
            log.info(self.log('generated call action: %s' % action))
            if action == 'number':
                self.call_action('onhook', [])
                self.call_action('offhook', [])
            self.call_action(action, generate_params(action, self.params_generators))
            if action == 'number':
                yield sleep()


    def on_dialtone(self, tone):
        #self.maybe_go_insane()
        if not self.sane:
            return
        if tone != 'inside':
            return
        if self.got_tone:
            return
        self.got_tone = True
        log.info(self.log('dialtone'))
        self.action_cb('number', generate_params('correct_number', self.params_generators), self.line, self.id)

    @defer.inlineCallbacks
    def run(self):
        self.running = True
        while self.running:
            yield sleep(5)

