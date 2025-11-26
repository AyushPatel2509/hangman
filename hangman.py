import random
import pickle
import os
from time import sleep

# Hangman ASCII Art (7 stages)
HANGMAN_ART = [
    """
    +---+
    |   |
        |
        |
        |
        |
  =========
    """,
    """
    +---+
    |   |
    O   |
        |
        |
        |
  =========
    """,
    """
    +---+
    |   |
    O   |
    |   |
        |
        |
  =========
    """,
    """
    +---+
    |   |
    O   |
   /|   |
        |
        |
  =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
        |
        |
  =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   /    |
        |
  =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   / \\  |
        |
  =========
    """
]

# Word Categories
WORD_CATEGORIES = {
    "superstars": ["Salmankhan", "JohnAbraham", "adityaroykapoor", "ShahRukhKhan", "aamirkhan", "vickykausal", "hritikroshan"],
    "cities": ["Mumbai", "Hyderabad", "Surat", "Bengaluru", "Pune"],
    "animals": ["elephant", "giraffe", "Leopard  ", "Lion", "Tiger"]
}

# Difficulty Settings
DIFFICULTY = {
    "easy": 9,
    "medium": 6,
    "hard": 4
}

SAVE_FILE = "hangman_save.dat"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'rb') as f:
            return pickle.load(f)
    return None

def save_game(game_state):
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump(game_state, f)

def select_category():
    print("\nChoose a category:")
    for i, category in enumerate(WORD_CATEGORIES.keys(), 1):
        print(f"{i}. {category.capitalize()}")
    while True:
        try:
            choice = int(input("Enter choice (1-3): ")) - 1
            if 0 <= choice < len(WORD_CATEGORIES):
                return list(WORD_CATEGORIES.keys())[choice]
        except ValueError:
            print("Invalid input. Try again.")

def select_difficulty():
    print("\nSelect difficulty:")
    for i, (diff, tries) in enumerate(DIFFICULTY.items(), 1):
        print(f"{i}. {diff.capitalize()} ({tries} tries)")
    while True:
        try:
            choice = int(input("Enter choice (1-3): ")) - 1
            if 0 <= choice < len(DIFFICULTY):
                return list(DIFFICULTY.values())[choice]
        except ValueError:
            print("Invalid input. Try again.")

def play_hangman():
    clear_screen()
    print("=== Lets play Hangman ===")
    
    # Try to load saved game
    saved_game = load_game()
    if saved_game:
        print("\nSaved game found!")
        if input("Load saved game? (y/n): ").lower() == 'y':
            word, guessed, tries_left, score = saved_game
            category = next((cat for cat, words in WORD_CATEGORIES.items() if word in words), "unknown")
            return main_game_loop(word, guessed, tries_left, score, category)
    
    # New game setup
    category = select_category()
    difficulty = select_difficulty()
    word = random.choice(WORD_CATEGORIES[category]).upper()
    guessed_letters = set()
    tries_left = difficulty
    score = 0
    
    return main_game_loop(word, guessed_letters, tries_left, score, category)

def main_game_loop(word, guessed_letters, tries_left, score, category):
    while tries_left > 0:
        clear_screen()
        print(f"\nCategory: {category.capitalize()} | Score: {score} | Tries left: {tries_left}")
        print(HANGMAN_ART[len(HANGMAN_ART) - tries_left - 1])
        
        # Display word with blanks
        display_word = ""
        for letter in word:
            display_word += letter if letter in guessed_letters else "_ "
        print("\n" + display_word + "\n")
        
        # Check win condition
        if "_" not in display_word:
            score += tries_left * 10  # Bonus for remaining tries
            print(f"\nCongratulations! You won! Final score: {score}")
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
            return
        
        # Get player input
        while True:
            guess = input("Guess a letter (or 'save' to quit): ").upper()
            if guess == "SAVE":
                save_game((word, guessed_letters, tries_left, score))
                print("Game saved. Come back later!")
                return
            elif len(guess) == 1 and guess.isalpha():
                break
            print("Invalid input. Enter a single letter or 'save'.")
        
        # Process guess
        if guess in guessed_letters:
            print("You already guessed that!")
            sleep(1)
        elif guess in word:
            print("Correct!")
            guessed_letters.add(guess)
            score += 5
            sleep(1)
        else:
            print("Wrong!")
            tries_left -= 1
            sleep(1)
    
    # Game over
    clear_screen()
    print(HANGMAN_ART[-1])
    print(f"\nGame over! The word was: {word}")
    print(f"Your final score: {score}")
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

if __name__ == "__main__":
    while True:
        play_hangman()
        if input("\nPlay again? (y/n): ").lower() != 'y':
            break
    print("Thanks for playing!")
