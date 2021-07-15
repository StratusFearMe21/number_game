"""
Copyright (c) 2021 Mitch Feigenbaum <mfeigenbaum23@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
A number guessing game
Main functions:
Record amount of local tries and amount of total tries at the end
Generate random number in a certain range (random module)
Tell whether too high, low, or correct after each try
Play again function
Different difficulty modes
"""

from secrets import randbelow

# Meta stats

total_guesses = 0
rounds_won = 0
rounds_lost = 0
total_rounds = 0
current_guesses = 0
high_score = 100


def correct_check(guess: int, correct: int) -> bool:
    """Checks if a number is too high, low, or correct"""
    if guess > correct:
        print("Your guess is too high.")
    elif guess < correct:
        print("Your guess is too low.")
    else:
        print("You guessed correct!")
        return True
    return False


def select_difficulty() -> int:
    """Returns number of possible guesses based on user input"""
    print("""
Which difficulty would you like?
          1: Very Easy (100 possibilities)
          2: Easy (1,000 possibilities)
          3: Default (10,000 possibilities)
          4: Hard (100,000 possibilites)
          5: Very Hard (1,000,000 possibilities)
          """)
    mode_switch = {
        "1": 100,
        "2": 1_000,
        "4": 100_000,
        "5": 1_000_000,
    }
    selection = input("=> ")
    return mode_switch.get(selection, 10_000)


def start_round() -> bool:
    """Generates a random number and then has the user try to guess the number"""
    global total_guesses
    global current_guesses
    possibilities = select_difficulty()
    correct_number = randbelow(possibilities)
    print("Try to guess what number I'm thinking of (in less than 100 guesses)!")
    while current_guesses < 100:
        guessed_number = input("=> ")
        try:
            guessed_number = int(guessed_number)
        except ValueError:
            print("You must input a valid integer")
            continue
        else:
            current_guesses += 1
            result = correct_check(guessed_number, correct_number)
            if result: return True
    return False


def play_again():
    """Prompts user to play again or quit the program"""
    while True:
        again = input("Would you like to play another round? (y/n): ").lower()
        if again == "y":
            break
        elif again == "n":
            raise SystemExit("Thank you for playing!")
        else:
            print("Please input a valid option (either 'y' or 'n')")


def play():
    """Main function"""
    global total_guesses
    global high_score
    global total_rounds
    global current_guesses
    global rounds_lost
    global rounds_won
    global percent_won
    while True:
        round_result = start_round()
        if round_result:
            rounds_won += 1
        else:
            rounds_lost += 1
        total_guesses += current_guesses
        percent_won = rounds_won / (rounds_won + rounds_lost)
        total_rounds = rounds_won + rounds_lost
        if current_guesses < high_score:
            high_score = current_guesses
        print(f"""
Current standings:
    Guesses during this round: {current_guesses}
    Total guesses: {total_guesses}
    Rounds lost: {rounds_lost}
    Rounds won: {rounds_won}
    Winning percentage: {percent_won:.2%}
    Best round: {high_score}
""")
        current_guesses = 0
        play_again()


if __name__ == "__main__":
    play()
