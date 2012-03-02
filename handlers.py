from twisted.internet import reactor
from threading import Event
from generators import *
from util import *
from collections import defaultdict


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
                       ['answer', 'ringout', 'transfer'],
                       line, id)

def aggressive_call_factory(action_cb, params_generators, line, id):
    return CallHandler(action_cb, params_generators,
                       ['ringout', 'answer', 'transfer'],
                       line, id)


class GeneratorActor:

    def __init__(self, action_cb, action_generator, params_generators, id):
        self.action_generator = action_generator
        self.params_generators = params_generators
        self.action_cb = action_cb
        self.delete_event = Event()
        self.id = id
        self.did_call = False

    def stop(self):
        self.delete_event.set()

    def start(self):
        reactor.callInThread(self.run)

    def run(self):
        for action in self.action_generator:
            if action == 'newcall':
                if self.did_call:
                    continue
                self.did_call = True
            params = generate_params(action, self.params_generators)
            if self.delete_event.is_set():
                break
            if action == 'sleep':
                print '\n=[%s] sleeping=\n' % self.id
                self.delete_event.wait(0.5)
            else:
                reactor.callFromThread(self.action_cb,
                                       self.id,
                                       action,
                                       params)

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

    def on_actions(self, actions):
        #self.maybe_go_insane()
        if not self.sane:
            return

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
            self.action_cb(action, generate_params(action, self.params_generators), self.line, self.id)

    def on_dialtone(self, tone):
        #self.maybe_go_insane()
        if not self.sane:
            return
        if tone != 'inside':
            return
        print 'pushing number for tone', tone
        self.action_cb('number', generate_params('correct_number', self.params_generators), self.line, self.id)

