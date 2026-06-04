import random

def main():
    print("Welcome to the Number Guessing Game!")
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    
    print("I have selected a number between 1 and 100.")
    print("Can you guess what it is?")
    
    while True:
        try:
            # Get user input
            guess_str = input("Enter your guess: ")
            guess = int(guess_str)
            attempts += 1
            
            # Check the guess
            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

if __name__ == "__main__":
    main()
