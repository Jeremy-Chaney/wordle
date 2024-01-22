import os
import sys
import random
import time
import math
import signal
from datetime import datetime
import wordle_word_dict

num_guesses = 6
debug_mode = 0
word_len = 5
alphabetize_mode = 0
debug_word = 'debug'
box_str = '\u2588 '
guess_str = ['', '', '', '', '', '']

keyboard_str = [
    'q w e r t y u i o p',
    ' a s d f g h j k l ',
    '  z x c v b n m',
]

class color:
    GREY        = "\033[38;5;246m"
    GREEN       = "\033[38;5;10m"
    YELLOW      = "\033[38;5;220m"
    WHITE       = "\033[38;5;255m"
    RESET       = "\033[0;0m"
    GREEN_BG    = "\033[48;5;10m\033[38;5;232m"  # bold black text on green background
    YELLOW_BG   = "\033[48;5;220m\033[38;5;232m" # bold black text on yellow background
    GREY_BG     = "\033[48;5;246m\033[38;5;232m" # bold black text on grey background
    RED_BG      = "\033[48;5;196m\033[38;5;232m"   # bold white text on red background

# define our clear function
def clear():
    if sys.platform == 'win32':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

# get the letter index ie, a->0, b->1, y->24, z->25
def get_letter_idx(letter):
    for i in range(len(wordle_word_dict.valid_char_list)):
        if letter == wordle_word_dict.valid_char_list[i]:
            return i

# print the above keyboard with information on each letter
def print_keyboard():
    for kb_line in keyboard_str:
        keyboard_str_updated = ''
        for i in range(len(kb_line)):
            if wordle_word_dict.all_letters.find(kb_line[i]) != -1:
                letter_idx = get_letter_idx(kb_line[i])
                letter_status = wordle_word_dict.keyboard_status[letter_idx]

                if debug_mode:
                    print(str(letter_idx))
                    print(str(letter_status))

                if letter_status == '1':
                    keyboard_str_updated = keyboard_str_updated + color.YELLOW + kb_line[i] + color.RESET
                elif letter_status == '2':
                    keyboard_str_updated = keyboard_str_updated + color.GREEN + kb_line[i] + color.RESET
                elif letter_status == '3':
                    keyboard_str_updated = keyboard_str_updated + color.GREY + kb_line[i] + color.RESET
                else:
                    keyboard_str_updated = keyboard_str_updated + color.WHITE + kb_line[i] + color.RESET
            else:
                keyboard_str_updated = keyboard_str_updated + kb_line[i]
        print(keyboard_str_updated + color.RESET)

# update the keyboard information based on the last guess and previous information
def update_keyboard(guess_wd, soln):
    for i in range(len(guess_wd)):
        letter_idx = get_letter_idx(guess_wd[i])
        if soln.find(guess_wd[i]) != -1:

            # update to green status if correct letter and place is true
            if soln[i] == guess_wd[i]:
                wordle_word_dict.keyboard_status[letter_idx] = '2'

            # update to yellow status only if it's not already green
            else:
                if wordle_word_dict.keyboard_status[letter_idx] == '2':
                    wordle_word_dict.keyboard_status[letter_idx] = '2'
                else:
                    wordle_word_dict.keyboard_status[letter_idx] = '1'

        # if letter is nowhere in the word, change to grey status
        else:
            wordle_word_dict.keyboard_status[letter_idx] = '3'

# print the color-coded guesses with characters
def wordle_print(guess_wd, soln):
    wordle_str = ''
    if debug_mode:
        print(guess_wd)

    for i in range(len(guess_wd)):

        if guess_wd[i] != '\n':
            if soln.find(guess_wd[i]) != -1:
                if soln[i] == guess_wd[i]:
                    wordle_str = wordle_str + " " + color.GREEN_BG + " " + guess_wd[i] + " " + color.RESET
                else:
                    wordle_str = wordle_str + " " + color.YELLOW_BG + " " + guess_wd[i] + " " + color.RESET
            else:
                wordle_str = wordle_str + " " + color.GREY_BG + " " + guess_wd[i] + " " + color.RESET
    print(wordle_str + color.RESET + '\n')
    wordle_str = ''

# print the color-coded guesses with boxes
def final_print(guess_wd, soln):
    wordle_str = ''
    if debug_mode:
        print(guess_wd)
        print(str(wordle_word_dict.keyboard_status))

    for i in range(len(guess_wd)):

        if guess_wd[i] != '\n':
            if soln.find(guess_wd[i]) != -1:
                if soln[i] == guess_wd[i]:
                    wordle_str = wordle_str + " " + color.GREEN_BG + " " + guess_wd[i] + " " + color.RESET
                else:
                    wordle_str = wordle_str + " " + color.YELLOW_BG + " " + guess_wd[i] + " " + color.RESET
            else:
                wordle_str = wordle_str + " " + color.GREY_BG + " " + guess_wd[i] + " " + color.RESET
    print(wordle_str + '\n')
    wordle_str = ''

# checks if word is in valid word dictionary, and matches the word length defined
# also updates updates the keyboard status once a valid word is found
def get_valid_word(guess_num, soln):
    ascii_trig = 0

    def handle_ctrl_c(signal, frame):
        print(f"\n{color.GREEN}INFO{color.RESET} : user did CTRL+C exit after {guess_num} guesses, solution = {soln}")
        exit()
    signal.signal(signal.SIGINT, handle_ctrl_c)

    while(1):
        pre_guess_print(guess_num, soln)
        print_keyboard()
        in_str = input("\nEnter your guess: ")
        if len(in_str) == word_len:
            if in_str in wordle_word_dict.valid_word_list:
                break

            if in_str == 'ascii':
                ascii_trig = 1

    update_keyboard(in_str, soln)
    return in_str, ascii_trig

# handles all printing until end-of-game print
def pre_guess_print(guess_num, soln):
    clear()
    if guess_num != 0:
        print("Wrong, take another guess...\n")
        for i in range(guess_num):
            wordle_print(guess_str[i], soln)

# end-of-game print handled here
def post_game_rpt(soln):
    for i in range(num_guesses):
        final_print(guess_str[i], soln)

def ascii_fail_rpt(soln):
    i = 0
    for line in wordle_word_dict.ascii_fail:
        if line.find("xxx") == -1:
            print(line)
        else:
            print(line[0: line.find("xxx")] + color.RED_BG + " " + soln[i] + " " + color.RESET + line[line.find("xxx") + 3: len(line)])
            i = i + 1

def ascii_pass_rpt(soln):
    i = 0
    for line in wordle_word_dict.ascii_pass:
        if line.find("xxx") == -1:
            print(line)
        elif i == 0:
            print(line[0: line.find("xxx")] + color.GREEN_BG + " " + soln[2] + " " + color.RESET + line[line.find("xxx") + 3: len(line)])
            i = i + 1
        elif i == 1:
            print(line[0: line.find("xxx")] + color.GREEN_BG + " " + soln[3] + " " + color.RESET + line[line.find("xxx") + 3: len(line)])
            i = i + 1
        elif i == 2:
            print(line[0: line.find("xxx")] + color.GREEN_BG + " " + soln[1] + " " + color.RESET + line[line.find("xxx") + 3: len(line)])
            i = i + 1
        elif i == 3:
            print(line[0: line.find("xxx")] + color.GREEN_BG + " " + soln[0] + " " + color.RESET + line[line.find("xxx") + 3: len(line)])
            i = i + 1
        elif i == 4:
            print(line[0: line.find("xxx")] + color.GREEN_BG + " " + soln[4] + " " + color.RESET + line[line.find("xxx") + 3: len(line)])
            i = i + 1

# general function for the game to be running
def playing_fcn(soln):
    victory = 0
    ascii_mode = 0
    for i in range(num_guesses):

        guess_str[i], ascii_trig = get_valid_word(i, soln)
        if guess_str[i] == soln:
            victory = i + 1
            break
        if ascii_trig == 1:
            if ascii_mode == 0:
                ascii_mode = 1
            else:
                ascii_mode = 0

    clear()

    if ascii_mode:
        if victory == 0:
            ascii_fail_rpt(soln)
        else:
            ascii_pass_rpt(soln)
            print("\n\n" + str(i + 1) + '/6')

    else:
        if victory == 0:
            print('wow... you are bad at this')
            print('The word was ' + soln)
        else:
            print('YOU GOT IT!\n' + str(i + 1) + '/6')

        post_game_rpt(soln)

    return i


def main():

    # takes the specified list below and prints them in alphabetical order, ready to copy into wordle_word_dict.py
    if alphabetize_mode:
        with open("wordle_list_alpha.txt", 'w') as output_file:
            wordle_word_dict.valid_word_list.sort()
            for i in range(len(wordle_word_dict.valid_word_list)):
                output_file.write("\t\'" + wordle_word_dict.valid_word_list[i] + '\',\n')
        output_file.close()

    # the game will be played in either debug mode or normal mode
    else:
        start_time = time.time()

        if debug_mode:
            soln = debug_word
        else:
            random.seed(datetime.now())
            rnd_idx = random.randrange(0, len(wordle_word_dict.valid_answer_list))
            soln = wordle_word_dict.valid_answer_list[rnd_idx]

        num_guesses = playing_fcn(soln)

        end_time = time.time()
        print(f"SCORE : {math.floor(num_guesses * (end_time - start_time))}")

if __name__ == '__main__':
    main()
    end_time = time.time()
