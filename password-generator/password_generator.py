import random
import string

def generate_password(length, include_numbers=True, include_symbols=True):
    """
    Generates a secure password based on user preferences.
    """
    # Base characters: lowercase and uppercase letters
    characters = string.ascii_letters
    
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation
        
    if length <= 0:
        return "Error: Password length must be greater than 0."
        
    # Generate the password by randomly choosing characters
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("Welcome to the Secure Password Generator!")
    print("-" * 40)
    
    # Get password length
    while True:
        try:
            length = int(input("Enter desired password length (e.g., 12): "))
            if length <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
    # Get preferences for numbers and symbols
    inc_num_input = input("Include numbers? (y/n): ").strip().lower()
    include_numbers = inc_num_input in ['y', 'yes']
    
    inc_sym_input = input("Include symbols? (y/n): ").strip().lower()
    include_symbols = inc_sym_input in ['y', 'yes']
    
    # Generate and display the password
    password = generate_password(length, include_numbers, include_symbols)
    
    print("\n--- Your Generated Password ---")
    print(f"\n{password}\n")
    print("-" * 40)

if __name__ == "__main__":
    main()
