import tkinter as tk
import RPi.GPIO as GPIO
import time


UNIT_TIME = .25

#set up pin
GPIO21 = 21
VERBOSE = True

symbols = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',

}


master = tk.Tk()
master.title("Enter a word:")
master.geometry("300x100")


def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO21, GPIO.OUT)

         
def transmit_word(word):
    for (index, letter) in enumerate(word):
        if index > 0:
            wait_between_letters()
        transmit_letter(letter)


def transmit_letter(letter):
    code = symbols.get(letter.upper(), '')

    if code != '':

        if VERBOSE:
            print('\nProcessing letter "{}" and code "{}"'.format(letter.upper(), code))

        for (index, signal) in enumerate(code):
            if index > 0:
                wait_between_signals()

            if signal == '.':
                transmit_dot()
            else:
                transmit_dash()

    else:
        if VERBOSE:
            print('\nInvalid input: {}'.format(letter))


def transmit_dot():
    GPIO.output(GPIO21, GPIO.HIGH)
    time.sleep(UNIT_TIME)


def transmit_dash():
    GPIO.output(GPIO21, GPIO.HIGH)
    time.sleep(UNIT_TIME * 3)


def wait_between_signals():
    GPIO.output(GPIO21, GPIO.LOW)
    time.sleep(UNIT_TIME)


def wait_between_letters():
    GPIO.output(GPIO21, GPIO.LOW)
    time.sleep(UNIT_TIME * 3)


initialize_gpio()

message = '~'
new = tk.StringVar()
def read_message():
    message = new.get()
    nLabel2 = tk.Label(master, text = message).pack()
    if message != '':
        if VERBOSE:
            print('\nBegin Transmission')

        transmit_word(message)
        GPIO.output(GPIO21, GPIO.LOW)

        if VERBOSE:
            print('\nEnd Transmission')

nLabel = tk.Label(master, text = 'Insert Text').pack()
nEntry = tk.Entry(master, textvariable = new).pack()
mbutton = tk.Button(master,  text = 'OK', command = read_message).pack()
