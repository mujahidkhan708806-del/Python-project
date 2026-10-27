"""
Student Management System
MCA First Semester Python Project
Concepts used: functions, loops, conditions, exception handling,
               SQLite database (CRUD), string formatting, menu-driven program
"""

import sqlite3

DB_NAME = "students.db"


def connect_db():
    """Database se connection banata hai."""
    return sqlite3.connect(DB_NAME)


def create_table():
    """Agar table nahi hai to bana deta hai."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no INTEGER PRIMARY KEY,
            name    TEXT NOT NULL,
            course  TEXT NOT NULL,
            marks   REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_grade(marks):
    """Marks ke basis par grade return karta hai."""
    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 40:
        return "C"
    return "Fail"


def read_int(message):
    """Sirf valid integer leta hai, warna dobara poochta hai."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input! Number daaliye.")


def read_marks(message):
    """0 se 100 ke beech marks leta hai."""
    while True:
        try:
            m = float(input(message))
            if 0 <= m <= 100:
                return m
            print("Marks 0 se 100 ke beech hone chahiye.")
        except ValueError:
            print("Invalid input! Number daaliye.")


def add_student():
    roll_no = read_int("Roll No: ")
    name = input("Name: ").strip()
    course = input("Course: ").strip()
    marks = read_marks("Marks (0-100): ")

    try:
        conn = connect_db()
        conn.execute("INSERT INTO students VALUES (?, ?, ?, ?)",
                     (roll_no, name, course, marks))
        conn.commit()
        conn.close()
        print("Student successfully add ho gaya!")
    except sqlite3.IntegrityError:
        print("Error: Ye Roll No pehle se maujood hai.")


def view_students():
    conn = connect_db()
    rows = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
    conn.close()

    if not rows:
        print("Koi record nahi mila.")
        return

    print("\n{:<8}{:<20}{:<12}{:<8}{:<6}".format(
        "Roll", "Name", "Course", "Marks", "Grade"))
    print("-" * 54)
    for roll, name, course, marks in rows:
        print("{:<8}{:<20}{:<12}{:<8}{:<6}".format(
            roll, name, course, marks, get_grade(marks)))


def search_student():
    roll_no = read_int("Search karne ke liye Roll No: ")
    conn = connect_db()
    row = conn.execute("SELECT * FROM students WHERE roll_no = ?",
                       (roll_no,)).fetchone()
    conn.close()

    if row:
        print(f"\nRoll No : {row[0]}")
        print(f"Name    : {row[1]}")
        print(f"Course  : {row[2]}")
        print(f"Marks   : {row[3]}")
        print(f"Grade   : {get_grade(row[3])}")
    else:
        print("Student nahi mila.")


def update_student():
    roll_no = read_int("Update karne ke liye Roll No: ")
    conn = connect_db()
    exists = conn.execute("SELECT 1 FROM students WHERE roll_no = ?",
                          (roll_no,)).fetchone()
    if not exists:
        print("Student nahi mila.")
        conn.close()
        return

    name = input("Naya Name: ").strip()
    course = input("Naya Course: ").strip()
    marks = read_marks("Naye Marks (0-100): ")

    conn.execute("UPDATE students SET name=?, course=?, marks=? WHERE roll_no=?",
                 (name, course, marks, roll_no))
    conn.commit()
    conn.close()
    print("Record update ho gaya!")


def delete_student():
    roll_no = read_int("Delete karne ke liye Roll No: ")
    conn = connect_db()
    cur = conn.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
    conn.commit()
    conn.close()

    if cur.rowcount:
        print("Record delete ho gaya!")
    else:
        print("Student nahi mila.")


def show_statistics():
    """Total students, average, highest aur lowest marks dikhata hai."""
    conn = connect_db()
    count, avg, high, low = conn.execute(
        "SELECT COUNT(*), AVG(marks), MAX(marks), MIN(marks) FROM students"
    ).fetchone()
    conn.close()

    if count == 0:
        print("Abhi koi data nahi hai.")
        return

    print(f"\nTotal Students : {count}")
    print(f"Average Marks  : {avg:.2f}")
    print(f"Highest Marks  : {high}")
    print(f"Lowest Marks   : {low}")


def main():
    create_table()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Show Statistics")
        print("7. Exit")

        choice = input("Apna choice daaliye (1-7): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            show_statistics()
        elif choice == "7":
            print("Dhanyavaad! Program band ho raha hai.")
            break
        else:
            print("Galat choice! 1 se 7 ke beech daaliye.")


if __name__ == "__main__":
    main()
