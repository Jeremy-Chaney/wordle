import os
import sys
import random
import time
import math
import signal
import argparse
from datetime import datetime
import wordle_word_dict

class CustomHelpFormatter(
    argparse.RawDescriptionHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.MetavarTypeHelpFormatter):
    pass

help_text = """
Python Wordle by Jeremy Chaney

This is a python-based version of Wordle
This version uses a seeded pseudo-random number generator
to come up with a new word from over 2.3k possible words.
Unlike the web-based version, the answer dictionary is stored
in alphabetical order instead of a day-by-day list which is easy to cheat.

If you want to make a version of this for yourself, I recommend using the word
dictionaries from this wordle_word_dict.py

### Rules of Wordle ###
-   You must guess a 5 letter word in 6 or fewer guesses
-   Your guesses must be a word in the dictionary of valid words (there are almost 13k valid words)
-   You will get feedback after each valid guess:
    1. a correct letter in the correct spot will appear green
    2. a correct letter in the wrong spot will appear yellow
    3. a letter that does not appear in the final word will appear grey
"""

num_guesses = 6
word_len = 5
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

def clear():
    """
    define our clear function
    """
    if sys.platform == 'win32':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def get_letter_idx(letter):
    """
    get the letter index ie, a->0, b->1, y->24, z->25
    """
    for i in range(len(wordle_word_dict.valid_char_list)):
        if letter == wordle_word_dict.valid_char_list[i]:
            return i

def print_keyboard():
    """
    print the above keyboard with information on each letter
    """
    for kb_line in keyboard_str:
        keyboard_str_updated = ''
        for i in range(len(kb_line)):
            if wordle_word_dict.all_letters.find(kb_line[i]) != -1:
                letter_idx = get_letter_idx(kb_line[i])
                letter_status = wordle_word_dict.keyboard_status[letter_idx]

                if debug_mode:
                    print(str(letter_idx))
                    print(str(letter_status))

                if letter_status == 1:
                    keyboard_str_updated = keyboard_str_updated + color.YELLOW + kb_line[i] + color.RESET
                elif letter_status == 2:
                    keyboard_str_updated = keyboard_str_updated + color.GREEN + kb_line[i] + color.RESET
                elif letter_status == 3:
                    keyboard_str_updated = keyboard_str_updated + color.GREY + kb_line[i] + color.RESET
                else:
                    keyboard_str_updated = keyboard_str_updated + color.WHITE + kb_line[i] + color.RESET
            else:
                keyboard_str_updated = keyboard_str_updated + kb_line[i]
        print(keyboard_str_updated + color.RESET)

def update_keyboard(guess_wd, soln):
    """
    update the keyboard information based on the last guess and previous information
    """
    for i in range(len(guess_wd)):
        letter_idx = get_letter_idx(guess_wd[i])
        if soln.find(guess_wd[i]) != -1:

            # update to green status if correct letter and place is true
            if soln[i] == guess_wd[i]:
                wordle_word_dict.keyboard_status[letter_idx] = 2

            # update to yellow status only if it's not already green
            else:
                if wordle_word_dict.keyboard_status[letter_idx] == 2:
                    wordle_word_dict.keyboard_status[letter_idx] = 2
                else:
                    wordle_word_dict.keyboard_status[letter_idx] = 1

        # if letter is nowhere in the word, change to grey status
        else:
            wordle_word_dict.keyboard_status[letter_idx] = 3

def wordle_print(guess_wd, soln):
    """
    print the color-coded guesses with characters
    """
    wordle_str = ''
    if debug_mode:
        print(guess_wd)

    if len(guess_wd) != 0:
        for i in range(len(wordle_word_dict.guess_num_letter_per_word)):
            wordle_word_dict.guess_num_letter_per_word[i] = 0
            wordle_word_dict.guess_num_letter_per_word_printed[i] = 0

            for letter in guess_wd:
                if letter == wordle_word_dict.valid_char_list[i]:
                    wordle_word_dict.guess_num_letter_per_word[i] = wordle_word_dict.guess_num_letter_per_word[i] + 1

        for i in range(len(guess_wd)):
            if guess_wd[i] != '\n':
                if soln.find(guess_wd[i]) != -1:
                    if soln[i] == guess_wd[i]:
                        for letter in range(len(wordle_word_dict.valid_char_list)):
                            if wordle_word_dict.valid_char_list[letter] == guess_wd[i]:
                                wordle_word_dict.guess_num_letter_per_word_printed[letter] = wordle_word_dict.guess_num_letter_per_word_printed[letter] + 1
                        wordle_str = wordle_str + " " + color.GREEN_BG + " " + guess_wd[i] + " " + color.RESET
                    else:
                        for letter in range(len(wordle_word_dict.valid_char_list)):
                            if wordle_word_dict.valid_char_list[letter] == guess_wd[i]:
                                if wordle_word_dict.guess_num_letter_per_word[letter] <= wordle_word_dict.soln_num_letter_per_word[letter]:
                                    wordle_str = wordle_str + " " + color.YELLOW_BG + " " + guess_wd[i] + " " + color.RESET
                                elif wordle_word_dict.guess_num_letter_per_word_printed[letter] < wordle_word_dict.soln_num_letter_per_word[letter]:
                                    wordle_str = wordle_str + " " + color.YELLOW_BG + " " + guess_wd[i] + " " + color.RESET
                                    wordle_word_dict.guess_num_letter_per_word_printed[letter] = wordle_word_dict.guess_num_letter_per_word_printed[letter] + 1
                                else:
                                    wordle_str = wordle_str + " " + color.GREY_BG + " " + guess_wd[i] + " " + color.RESET
                else:
                    wordle_str = wordle_str + " " + color.GREY_BG + " " + guess_wd[i] + " " + color.RESET
        print(wordle_str + color.RESET + '\n')

def get_valid_word(guess_num, soln):
    """
    checks if word is in valid word dictionary, and matches the word length defined

    also updates updates the keyboard status once a valid word is found
    """
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

def pre_guess_print(guess_num, soln):
    """
    handles all printing until end-of-game print
    """
    clear()
    if guess_num != 0:
        print("Wrong, take another guess...\n")
        for i in range(guess_num):
            wordle_print(guess_str[i], soln)

def post_game_rpt(soln):
    """
    end-of-game print handled here
    """
    for i in range(num_guesses):
        wordle_print(guess_str[i], soln)

def ascii_fail_rpt(soln):
    """
    easter egg fail print
    """
    i = 0
    for line in wordle_word_dict.ascii_fail:
        if line.find("xxx") == -1:
            print(line)
        else:
            print(line[0: line.find("xxx")] + color.RED_BG + " " + soln[i] + " " + color.RESET + line[line.find("xxx") + 3: len(line)])
            i = i + 1

def ascii_pass_rpt(soln):
    """
    easter egg pass print
    """
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

def playing_fcn(soln):
    """
    general function for the game to be running
    """
    victory = 0
    ascii_mode = 0

    # reset the solution number per word to the new solution
    for i in range(len(wordle_word_dict.soln_num_letter_per_word)):
        wordle_word_dict.soln_num_letter_per_word[i] = 0

        for letter in soln:
            if letter == wordle_word_dict.valid_char_list[i]:
                wordle_word_dict.soln_num_letter_per_word[i] = wordle_word_dict.soln_num_letter_per_word[i] + 1

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

    global debug_mode

    parser = argparse.ArgumentParser(
        formatter_class = CustomHelpFormatter,
        description = help_text
    )

    parser.add_argument("-d", "--debug_mode",   dest = "debug_mode",        action = 'store_true', help="enable printing of non-essential debug messages, solution will be 'debug'")
    parser.add_argument("-a", "--alphabatize",  dest = "alphabetize_mode",  action = 'store_true', help="alphabatizes a word list to be copied into wordle_word_dict.py")
    parser.add_argument("-f", "--force_mode",   dest = "force_mode",  type = str, nargs = 1, help="force the game Wordle to be played with this word")

    args = parser.parse_args()

    debug_mode          = args.debug_mode
    alphabetize_mode    = args.alphabetize_mode
    force_mode          = args.force_mode

    # takes the specified list below and prints them in alphabetical order, ready to copy into wordle_word_dict.py
    if alphabetize_mode:
        with open("wordle_list_alpha.txt", 'w') as output_file:
            wordle_word_dict.valid_word_list.sort()
            for i in range(len(wordle_word_dict.valid_word_list)):
                output_file.write("\t\'" + wordle_word_dict.valid_word_list[i] + '\',\n')
        output_file.close()

    # the game will be played in either debug mode or normal mode
    else:
        for i in range(wordle_word_dict.num_letters):
            wordle_word_dict.soln_num_letter_per_word.append(0)
            wordle_word_dict.guess_num_letter_per_word.append(0)
            wordle_word_dict.guess_num_letter_per_word_printed.append(0)
            wordle_word_dict.keyboard_status.append(0)
        start_time = time.time()

        if force_mode:
            _ = input(f"About to play Wordle with solution: {color.GREEN}{force_mode[0]}{color.RESET}\nPress 'Enter' to continue...")
            soln = force_mode[0]
        elif debug_mode:
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
