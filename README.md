# Wordle in Python
(By Jeremy Chaney)

This is a python-based version of [Wordle](https://www.nytimes.com/games/wordle/index.html) intended to be run on a command line.

This version uses a seeded pseudo-random number generator to come up with a new word from over 2.3k possible words.
Unlike the web-based version, the answer dictionary is stored in alphabetical order instead of a day-by-day list which is easy to cheat.
If you want to make a version of this for yourself, I recommend using the word dictionaries from this `wordle_word_dict.py`.

# Rules of Wordle
-   You must guess a 5 letter word in 6 or fewer guesses
-   Your guesses must be a word in the dictionary of valid words (there are almost 13k valid words)
-   You will get feedback after each valid guess:
    1. a correct letter in the correct spot will appear green
    2. a correct letter in the wrong spot will appear yellow
    3. a letter that does not appear in the final word will appear grey
    4. if a guess contains multiple of a given letter, only the amount that actually exists in the final word will be shaded yellow/green
    5. (hard mode only) if a guess eliminates a letter, no future guess can contain that letter
    6. (hard mode only) if a guess indicates a letter exists in the solution, every future guess must contain that letter

# Modifications to the Rules
In the interest of creating a game that can be played competatively, a score is assigned based on the # of guesses needed to solve as well as the amount of time spent guessing:
- Lower Score is better!
- This formula is `score = (# of guesses) * (time in seconds) * (100)`.
- Running in 'hard mode' (using `python wordle.py -r`) will result in dividing the score in half.

# Multiplayer over WiFi supported
Host a Wordle LAN party!
- Devices must be connected to the same WiFi network to work.
- One user must act as a 'host' using `python wordle.py -o`
- All other users must run in client mode using `python wordle.py -j`
- Host must relay IP Address displayed in terminal to clients to enter the first time
- Last entered IP Address is cached in `last_host_addr.txt` (auto-generated, not in this repo) so you do not need to re-enter the IP Address every time.

# Head to Head Mode
For users who don't wish to set up a WiFi, two-player head to head is supported.
- Run `python wordle.py -h2h` then follow the prompts to play.
- Both players will receive the same word so player 2 shouldn't watch while player 1 is guessing.
- After playing multiple times, a summary of the results will be printed upon exit from the script.
  - Only via answering 'No' to playing again, not by CTRL+C exit.
- Can be launched in conjuction with hard-mode using `python wordle.py -h2h -r`

# Terminal Text Effects supported for visual flare
Not required to run but installing the [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects) module (to get this, run `pip install terminaltexteffects`) will enable visual effects in parts of the script that do not get factored into scoring.

For more information, run `python wordle.py -h`.