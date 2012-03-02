from twisted.internet import reactor
from threading import Event

from Queue import Queue

from collections import defaultdict, Iterable

from generators import *

from const import *

import util

from sccp.sccpkeypadbutton import SCCPKeyPadButton

from sccp.sccpsoftkeyevent import SCCPSoftKeyEvent
from gui.softkeys import *

actions_to_softkeys = {
                           'redial' : SKINNY_LBL_REDIAL,
                           'newcall' : SKINNY_LBL_NEWCALL,
                           'hold' : SKINNY_LBL_HOLD,
                           'transfer' :SKINNY_LBL_TRANSFER,
                           'endcall' : SKINNY_LBL_ENDCALL,
                           'answer' : SKINNY_LBL_ANSWER,
                           'ringout' : SKINNY_LBL_RINGOUT,
                           'dial' : SKINNY_LBL_DIAL,
                           }


def action_to_messages(action, params, line=0, callid=0):
    messages = []
    if action == 'number':
        number = params[0]
        print 'CHOSEN NUMBER:', number, type(number)
        softkey = actions_to_softkeys['ringout']
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

    def execute_action(self, action, params, line=0, callid=0):
        messages = action_to_messages(action, params, line, callid)
        if self.messages_handler is not None:
            self.messages_handler.onMessages(messages)

    def on_call_action(self, action, params, line, callid):
        print '\n=[%s] call action: %s(%s)=\n' % (callid, action, params)
        self.execute_action(action, params, line, callid)

    def on_user_action(self, id, action, params):
        print '\n=[%s] user action: %s(%s)=\n' % (id, action, params)
        self.execute_action(action, params)

    def delete_call(self, id):
        call_handler = self.call_handlers[id]
        call_handler.stop()

    def start(self):
        self.user_handler = self.user_factory(
            self.on_user_action, self.params_generators, self.user_id)
        self.user_handler.start()

    def on_dialtone(self, callid, tone):
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

    def maybe_create_call(self, ctype, line, callid):
        if callid not in self.call_handlers:
            self.create_call(ctype, line, callid)

    def create_call(self, ctype, line, callid):
        generator = (in_generator if ctype == 'ingoing' else out_generator)()
        call_handler = self.call_factory(
            self.on_call_action, self.params_generators,
            line, callid)
        call_handler.start()
        self.call_handlers[callid] = call_handler


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
#    correct_numbers_factory = lambda: [choose_number(numbers)]
    correct_numbers_factory = lambda: [numbers[0]]

    params_generators = {'correct_number': correct_numbers_factory,
                         'incorrect_number': incorrect_numbers_factory,
                         'sleep': sleep_factory}
    return params_generators


def test_calls():
    numbers = ['133', '244', '343']
    params_generators = create_params_generators(numbers)
    manager = Manager('user_asia', params_generators)
    manager.start()
    line = 1
    c1 = 'call_marek'
    manager.create_call('outgoing', line, c1)
    manager.on_dialtone(c1, 'inside')
    manager.on_actions(c1, ['dial', 'endcall'])
    manager.on_actions(c1, ['transfer', 'endcall'])
    # manager.create_call('ingoing', 'call_adam')
    # manager.create_call('ingoing', 'call_kamil')


if __name__ == '__main__':
    reactor.callFromThread(test_calls)
    reactor.run()
