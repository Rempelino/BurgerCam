from datetime import  datetime

disable_print = False
print_string = ""
last_milli_call = 0

def millis():
    global last_milli_call
    now = datetime.now()
    last_milli_call = now.microsecond // 1000
    return last_milli_call


def get_time():
    global last_milli_call
    now = datetime.now()
    difference = now.microsecond // 1000 - last_milli_call
    if difference < 0:
        difference += 1000
    return difference


def print_time(msg):
    global disable_print
    if disable_print:
        return
    global print_string
    print_string = f'{print_string}{get_time()}ms- {msg}\n'


def commit_print():
    global disable_print
    if disable_print:
        return
    global print_string
    print("-------------------------")
    print(print_string)
    print_string = ""
    millis()
