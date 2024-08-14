import threading
from subprocess import call

files = ['log_bot.py',
         'poll_bot.py',
         'shitcoin_bot.py',
         'counter_bot.py',
         'basic_counter_bot.py']

def func(script):

    call(['python', script])

for script in files:

    x = threading.Thread(target = func, args = (script,))
    x.start()