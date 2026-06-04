import random

def run_quiz():
    # Dictionary storing questions as keys and answers as values
    questions = {
        "What is the capital of France?": "Paris",
        "What is 5 + 7?": "12",
        "What is the largest planet in our solar system?": "Jupiter",
        "Who wrote 'Romeo and Juliet'?": "Shakespeare",
        "What is the chemical symbol for water?": "H2O"
    }

    print("Welcome to the Python Quiz Game!")
    print("Answer the following questions. Type 'quit' at any time to exit.\n")

    # Get a list of the questions and shuffle them for randomized order
    question_list = list(questions.keys())
    random.shuffle(question_list)

    score = 0
    questions_asked = 0

    # Loop through the randomized questions
    for q in question_list:
        print(f"Question: {q}")
        user_answer = input("Your answer: ").strip()

        # Allow the user to quit early
        if user_answer.lower() == 'quit':
            print("Exiting the quiz early...\n")
            break
            
        questions_asked += 1
        correct_answer = questions[q]
        
        # Check answer (case-insensitive)
        if user_answer.lower() == correct_answer.lower():
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {correct_answer}\n")

    print("===================================")
    print(f"Quiz completed! Your final score is {score}/{questions_asked}.")
    print("===================================")

if __name__ == "__main__":
    run_quiz()
