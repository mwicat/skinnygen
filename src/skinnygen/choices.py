out_choices = {
    'start':
        [(('end', None), 0.2),
         (('correct_number', 'entered_number'), 0.6),
         (('incorrect_number', 'entered_number'), 0.2)],
    'entered_number':
        [(('end', None), 0.1),
         (('dial', 'connected'), 0.6),
         (('wait_for_dial', 'connected'), 0.3)]
    }

in_choices = {
    'start':
        [(('end', None), 0.2),
         (('answer', 'connected'), 0.8)]
    }

connection_choices = {
    'connected':
        [(('end', None), 0.2),
         (('sleep', 'connected'), 0.4),
         (('transfer', 'connected'), 0.3),
         (('hold', 'hold'), 0.1)],
    'hold':
        [(('end', None), 0.2),
         (('resume', 'connected'), 0.4),
         (('transfer', 'connected'), 0.4)]
    }

general_choices = {
    'start':
        [(('sleep', 'start'), 0.69),
         (('newcall', 'start'), 0.3),
         (('terminate', None), 0.00)]
    }
