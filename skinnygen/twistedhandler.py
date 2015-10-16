from Queue import Queue
from collections import defaultdict, Iterable
from generators import *
from const import *
import util

import handlers

from sccp.sccpkeypadbutton import SCCPKeyPadButton
from sccp.sccpsoftkeyevent import SCCPSoftKeyEvent

from gui.softkeys import *

import logging
log = logging.getLogger(__name__)

actions_to_softkeys = {
                           'redial' : SKINNY_LBL_REDIAL,
                           'newcall' : SKINNY_LBL_NEWCALL,
                           'hold' : SKINNY_LBL_HOLD,
                           'transfer' :SKINNY_LBL_TRANSFER,
                           'endcall' : SKINNY_LBL_ENDCALL,
                           'answer' : SKINNY_LBL_ANSWER,
                           'dial' : SKINNY_LBL_DIAL,
                           'dial' : SKINNY_LBL_DIAL,
                           'dnd' : SKINNY_LBL_DND,
                           }


def action_to_messages(action, params, line=0, callid=0):
    messages = []
    if action == 'number':
        number = params[0]
        print 'CHOSEN NUMBER:', number, type(number)
        softkey = actions_to_softkeys['dial']
        sk_event = SCCPSoftKeyEvent(softkey, line, callid)
        messages = [SCCPKeyPadButton(int(digit)) for digit in number] #+ [sk_event] * 20
    elif action in actions_to_softkeys:
        softkey = actions_to_softkeys[action]
        sk_event = SCCPSoftKeyEvent(softkey, line, callid)
        messages = [sk_event]
    return messages


class Manager:

    def __init__(self, user_id, params_generators, user_factory, call_factory):
        self.call_handlers = {}
        self.user_id = user_id
        self.params_generators = defaultdict(list)
        self.params_generators.update(params_generators)

        self.user_factory = user_factory
        self.call_factory = call_factory
        self.user_handler = None
        self.messages_handler = None

        self.placed_dnd = False

    def execute_action(self, action, params, line=0, callid=0):
        messages = action_to_messages(action, params, line, callid)
        if self.messages_handler is not None:
            self.messages_handler.onMessages(messages)
            
    def on_call_action(self, action, params, line, callid):
        log.info('[%s] call action: %s(%s)' % (callid, action, params))
        self.execute_action(action, params, line, callid)

    def on_user_action(self, id, action, params):
        log.info('[%s] user action: %s(%s)' % (id, action, params))
        if action == 'dnd':
            self.placed_dnd = not self.placed_dnd
        self.execute_action(action, params)

    def delete_call(self, id):
        call_handler = self.call_handlers[id]
        call_handler.stop()

    def start(self):
        log.info('starting user %s' % self.user_id)
        generator = handlers.create_user_generator(self.user_factory)
        self.user_handler = handlers.UserActor(self.on_user_action,
                                                    generator,
                                                    self.params_generators,
                                                    self.user_id)
        self.user_handler.start()

    def on_dialtone(self, line, callid, tone):
        if not self.has_call(callid):
            self.create_call('ingoing', line, callid)
        self.call_handlers[callid].on_dialtone(tone)

    def on_actions(self, line, callid, actions):
        if not self.has_call(callid):
            self.create_call('ingoing', line, callid)
        self.call_handlers[callid].on_actions(actions)

    def has_call(self, callid):
        return callid in self.call_handlers

    def stop(self):
        if self.user_handler is not None:
            self.user_handler.stop()

    def got_call_handler(self, ctype, line, callid):
        return callid in self.call_handlers
    
    def maybe_create_call(self, ctype, line, callid):
        return \
            self.call_handlers[callid] \
            if self.got_call_handler(ctype, line, callid) \
            else self.create_call(ctype, line, callid)

    def create_call(self, ctype, line, callid):
        actions = handlers.get_call_actions(self.call_factory)
        call_handler = handlers.CallActor(self.on_call_action,
                                   self.params_generators,
                                   actions, line, callid)
        self.call_handlers[callid] = call_handler
        call_handler.start()
        return call_handler


def number_generator():
    sz = random.randint(1, 10)
    number = ''.join(random.choice(BUTTONS) for i in range(sz))
    return number


def choose_number(numbers):
    if not numbers:
        raise Exception('No numbers to choose from when asked to dial. Please supply numbers for correct operation.')
    number = random.choice(numbers)
    return number


def create_params_generators(numbers):
    sleep_factory = lambda: [util.randfloat(0, 4)]
    incorrect_numbers_factory = lambda: [number_generator]
    correct_numbers_factory = lambda: [choose_number(numbers)]
    params_generators = {'correct_number': correct_numbers_factory,
                         'incorrect_number': incorrect_numbers_factory,
                         'sleep': sleep_factory}
    return params_generators


if __name__ == '__main__':
    from twisted.internet import reactor
    reactor.callFromThread(test_calls)
    reactor.run()
