import json
import os

class StudentGradeManager:
    def __init__(self, data_file='grades.json'):
        self.data_file = data_file
        self.students = self.load_data()

    def load_data(self):
        """Loads student data from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    # Migrate old format (Name -> ID) if needed
                    if data and not any(isinstance(v, dict) and 'name' in v for v in data.values()):
                        new_data = {}
                        current_id = 1
                        for name, grades in data.items():
                            student_id = str(current_id)
                            new_data[student_id] = {"name": name, "grades": grades}
                            current_id += 1
                        return new_data
                    
                    # Migrate UUID format to Int format if needed
                    if data and any(not k.isdigit() for k in data.keys()):
                        new_data = {}
                        current_id = 1
                        for old_id, info in data.items():
                            student_id = str(current_id)
                            new_data[student_id] = info
                            current_id += 1
                        return new_data
                        
                    return data
            except json.JSONDecodeError:
                return {}
        return {}

    def save_data(self):
        """Saves current student data to the JSON file."""
        with open(self.data_file, 'w') as file:
            json.dump(self.students, file, indent=4)

    def add_student(self, name):
        """Adds a new student and assigns an auto-incrementing ID."""
        if not self.students:
            next_id = 1
        else:
            next_id = max([int(k) for k in self.students.keys() if k.isdigit()] + [0]) + 1
            
        student_id = str(next_id)
        self.students[student_id] = {"name": name, "grades": {}}
        self.save_data()
        print(f"Student '{name}' added successfully with ID: {student_id}")
        return student_id

    def edit_student_name(self, student_id, new_name):
        """Edits a student's name using their ID."""
        if student_id not in self.students:
            print(f"Student ID '{student_id}' not found.")
            return
        
        old_name = self.students[student_id]['name']
        self.students[student_id]['name'] = new_name
        self.save_data()
        print(f"Student '{old_name}' (ID: {student_id}) has been renamed to '{new_name}'.")

    def delete_student(self, student_id):
        """Deletes a student and all their grades using their ID."""
        if student_id in self.students:
            name = self.students[student_id]['name']
            del self.students[student_id]
            self.save_data()
            print(f"Student '{name}' (ID: {student_id}) has been deleted.")
        else:
            print(f"Student ID '{student_id}' not found.")

    def delete_grade(self, student_id, subject):
        """Deletes a specific subject grade for a student using their ID."""
        if student_id not in self.students:
            print(f"Student ID '{student_id}' not found.")
            return
        
        name = self.students[student_id]['name']
        if subject in self.students[student_id]['grades']:
            del self.students[student_id]['grades'][subject]
            self.save_data()
            print(f"Grade for '{subject}' has been deleted from {name}.")
        else:
            print(f"Subject '{subject}' not found for {name}.")

    def update_grade(self, student_id, subject, grade):
        """Updates or adds a grade for a specific subject for a student using ID."""
        if student_id not in self.students:
            print(f"Student ID '{student_id}' not found.")
            return
        
        try:
            grade = float(grade)
            self.students[student_id]['grades'][subject] = grade
            self.save_data()
            name = self.students[student_id]['name']
            print(f"Grade updated for {name} (ID: {student_id}) in {subject}: {grade}")
        except ValueError:
            print("Invalid grade. Please enter a numerical value.")

    def report_grades(self, student_id=None):
        """Reports grades and average for a specific student or all students."""
        if student_id:
            if student_id in self.students:
                student = self.students[student_id]
                name = student['name']
                grades = student['grades']
                print(f"\n--- Grades for {name} (ID: {student_id}) ---")
                if not grades:
                    print("No grades recorded.")
                for subject, grade in grades.items():
                    print(f"{subject}: {grade}")
                
                if grades:
                    avg = sum(grades.values()) / len(grades)
                    print(f"Average: {avg:.2f}")
                print("---------------------------\n")
            else:
                print(f"Student ID '{student_id}' not found.")
        else:
            if not self.students:
                print("\nNo students found.\n")
                return

            print("\n--- All Students Grades ---")
            for sid, student in self.students.items():
                name = student['name']
                grades = student['grades']
                print(f"\n{name} (ID: {sid}):")
                if not grades:
                    print("  No grades recorded.")
                else:
                    for subject, grade in grades.items():
                        print(f"  {subject}: {grade}")
                    avg = sum(grades.values()) / len(grades)
                    print(f"  Average: {avg:.2f}")
            print("---------------------------\n")

def main():
    manager = StudentGradeManager()
    
    while True:
        print("\n=== Student Grade Manager ===")
        print("1. Add Student")
        print("2. Edit Student Name")
        print("3. Delete Student")
        print("4. Add/Update Grade")
        print("5. Delete Grade")
        print("6. View Student Grades")
        print("7. View All Grades")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            name = input("Enter student name: ").strip()
            if name:
                manager.add_student(name)
            else:
                print("Name cannot be empty.")
                
        elif choice == '2':
            sid = input("Enter student ID: ").strip()
            new_name = input("Enter new student name: ").strip()
            if sid and new_name:
                manager.edit_student_name(sid, new_name)
            else:
                print("Both ID and new name are required.")
                
        elif choice == '3':
            sid = input("Enter student ID to delete: ").strip()
            if sid:
                manager.delete_student(sid)
            else:
                print("ID cannot be empty.")
                
        elif choice == '4':
            sid = input("Enter student ID: ").strip()
            subject = input("Enter subject: ").strip()
            grade = input("Enter grade (e.g., 85.5): ").strip()
            if sid and subject and grade:
                manager.update_grade(sid, subject, grade)
            else:
                print("All fields are required.")
                
        elif choice == '5':
            sid = input("Enter student ID: ").strip()
            subject = input("Enter subject to delete: ").strip()
            if sid and subject:
                manager.delete_grade(sid, subject)
            else:
                print("All fields are required.")
                
        elif choice == '6':
            sid = input("Enter student ID: ").strip()
            if sid:
                manager.report_grades(sid)
            else:
                print("ID cannot be empty.")
                
        elif choice == '7':
            manager.report_grades()
            
        elif choice == '8':
            print("Exiting Student Grade Manager. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == '__main__':
    main()
