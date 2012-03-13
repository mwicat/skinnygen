from twisted.internet import reactor
from threading import Event
from generators import *
from util import *
from collections import defaultdict

import threading

INSIDE_DIAL_TONE = 0x21


def idle_user_factory(action_cb, params_generators, id):
    generator = iter(lambda: 'sleep', None)
    actor = GeneratorActor(action_cb, generator, params_generators, id)
    return actor

def random_user_factory(action_cb, params_generators, id):
    generator = general_generator()
    actor = GeneratorActor(action_cb, generator, params_generators, id)
    return actor

def autoanswer_call_factory(action_cb, params_generators, line, id):
    return CallHandler(action_cb, params_generators,
                       ['answer'],
                       line, id)

def autotransfer_call_factory(action_cb, params_generators, line, id):
    return CallHandler(action_cb, params_generators,
                       ['answer', 'ringout', 'transfer'],
                       line, id)

def aggressive_call_factory(action_cb, params_generators, line, id):
    return CallHandler(action_cb, params_generators,
                       ['ringout', 'answer'],
                       line, id)


class GeneratorActor(threading.Thread):

    def __init__(self, action_cb, action_generator, params_generators, id):
        threading.Thread.__init__(self)
        self.action_generator = action_generator
        self.params_generators = params_generators
        self.action_cb = action_cb
        self.delete_event = Event()
        self.id = id
        self.did_call = False

    def stop(self):
        self.delete_event.set()

    def call_action(self, action, params):
        reactor.callFromThread(self.action_cb, self.id,
                               action, params)

    def sleep(self):
        self.delete_event.wait(0.5)
        
    def run(self):
        log('started user %s' % self.id)        
        for action in self.action_generator:
            # if action == 'newcall':
            #     if self.did_call:
            #         continue
            #     self.did_call = True

            log('user %s: generated user action: %s' % (self.id, action))

            params = generate_params(action, self.params_generators)
            if self.delete_event.is_set():
                break
            if action == 'sleep':
                self.sleep()
            else:
                self.call_action(action, params)

class CallHandler:

    lines_calls = defaultdict(list)

    def __init__(self, action_cb, params_generators, actions, line, id):
        self.params_generators = params_generators
        self.action_cb = action_cb
        self.call_actor = None
        self.sane = True
        self.line = line
        self.id = id
        self.actions_to_do = actions
        self.ringout_counter = 0
        self.transfer_counter = 0
        self.lines_calls[line].append(id)

    def find_action(self, actions_to_fire, actions):
        for action in actions_to_fire:
            if action in actions:
                return action
        return None

    def stop(self):
        pass

    def start(self):
        pass

    def delete(self):
        if self.call_actor is not None:
            self.call_actor.stop()

    def go_insane(self):
        generator = iter(lambda: random.choice(ACTIONS), None)
        self.call_actor = Actor(self.action_cb,
                                generator,
                                self.params_generators,
                                self.id)
        reactor.callInThread(self.call_actor.start)

    def maybe_go_insane(self):
        self.sane = random.choice([True, False])
        if not self.sane:
            self.go_insane()

    def call_action(self, action, params):
        #reactor.callFromThread(self.action_cb, params, self.line, self.id)
        self.action_cb(action, params, self.line, self.id)

    def on_actions(self, actions):
        #self.maybe_go_insane()
        if not self.sane:
            return

        print 'on_actions', actions

        action = self.find_action(self.actions_to_do, actions)

        if action == 'ringout':
            if self.ringout_counter >= 1:
                return
            self.ringout_counter += 1

        if action == 'transfer':
            if self.transfer_counter >= 1 or len(CallHandler.lines_calls) < 2:
                return
            self.transfer_counter += 1

        if self.ringout_counter > 50:
            print 'OVERFLOW========================================='
            import sys; sys.exit(1)

        if action is not None:
            log('call %s: generated call action: %s' % (self.id, action))
            # if action == 'number':
            #     self.call_action('onhook', [])
            #     self.call_action('offhook', [])
            self.call_action(action, generate_params(action, self.params_generators))
            # if action == 'number':
            #     self.sleep()


    def on_dialtone(self, tone):
        #self.maybe_go_insane()
        if not self.sane:
            return
        if tone != 'inside':
            return
        self.action_cb('number', generate_params('correct_number', self.params_generators), self.line, self.id)

