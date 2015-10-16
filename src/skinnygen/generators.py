import random

from choices import *

def weighted_choice(choices):
   total = sum(w for c,w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto+w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"

def general_generator():
   return random_generator(general_choices, 'start')

def updated_dict(d1, d2):
   d = d1.copy()
   d.update(d2)
   return d

def in_generator():
   d = updated_dict(connection_choices, in_choices)
   return random_generator(d)

def out_generator():
   d = updated_dict(connection_choices, out_choices)
   return random_generator(d)


def random_generator(states_choices, start_state='start'):
   curr_state = start_state
   while True:
      if curr_state is None:
         raise StopIteration
      choices = states_choices[curr_state]
      action, next_state = weighted_choice(choices)
      yield action
      curr_state = next_state


