import random

def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'tie'
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        return 'user'
    else:
        return 'computer'

def play_game():
    print("Welcome to Rock-Paper-Scissors!")
    print("Choose your mode:")
    print("1. Best of 3")
    print("2. Best of 5")
    
    while True:
        mode_choice = input("Enter 1 or 2: ")
        if mode_choice == '1':
            target_score = 2
            break
        elif mode_choice == '2':
            target_score = 3
            break
        else:
            print("Invalid input. Please enter 1 or 2.")
            
    user_score = 0
    computer_score = 0
    
    while user_score < target_score and computer_score < target_score:
        print(f"\nScore - You: {user_score} | Computer: {computer_score}")
        user_choice = input("Enter rock, paper, or scissors (or 'quit' to exit): ").lower()
        
        if user_choice == 'quit':
            print("Thanks for playing!")
            return
            
        if user_choice not in ['rock', 'paper', 'scissors']:
            print("Invalid choice. Please try again.")
            continue
            
        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")
        
        winner = determine_winner(user_choice, computer_choice)
        
        if winner == 'tie':
            print("It's a tie!")
        elif winner == 'user':
            print("You win this round!")
            user_score += 1
        else:
            print("Computer wins this round!")
            computer_score += 1
            
    print(f"\nFinal Score - You: {user_score} | Computer: {computer_score}")
    if user_score > computer_score:
        print("Congratulations! You won the game!")
    else:
        print("Game over! The computer won.")

if __name__ == "__main__":
    play_game()
