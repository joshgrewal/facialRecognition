#python gui_attendance.py

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import json

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="AttendanceSystem"
)
cursor = db.cursor()

# Function to log attendance in the database
def log_attendance(student_id):
    sql = "INSERT INTO Attendance (StudentID, Timestamp) VALUES (%s, NOW())"
    cursor.execute(sql, (student_id,))
    db.commit()
    print(f"Attendance logged for StudentID: {student_id}")

# Function to take attendance using facial recognition
def take_attendance():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("trainer.yml")
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))
            
            for (x, y, w, h) in faces:
                id_, conf = recognizer.predict(gray[y:y+h, x:x+w])
                if conf >= 50:
                    with open("names.json", "r") as f:
                        names = json.load(f)
                    name = names.get(str(id_), "Unknown")
                    print(f"Detected: {name}")
                    log_attendance(id_)
                else:
                    print("Face not recognized.")
            
            cv2.imshow("Frame", frame)
            if cv2.waitKey(20) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Attendance", "Attendance logged successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to add a student to the database
def add_student():
    def submit():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        major = entry_major.get()
        email = entry_email.get()

        sql = "INSERT INTO Student (FirstName, LastName, Major, Email, ClassID) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (first_name, last_name, major, email, None))
        db.commit()

        messagebox.showinfo("Success", f"Student {first_name} {last_name} added!")
        add_student_window.destroy()

    add_student_window = tk.Toplevel()
    add_student_window.title("Add Student")

    tk.Label(add_student_window, text="First Name").grid(row=0, column=0)
    tk.Label(add_student_window, text="Last Name").grid(row=1, column=0)
    tk.Label(add_student_window, text="Major").grid(row=2, column=0)
    tk.Label(add_student_window, text="Email").grid(row=3, column=0)

    entry_first_name = tk.Entry(add_student_window)
    entry_last_name = tk.Entry(add_student_window)
    entry_major = tk.Entry(add_student_window)
    entry_email = tk.Entry(add_student_window)

    entry_first_name.grid(row=0, column=1)
    entry_last_name.grid(row=1, column=1)
    entry_major.grid(row=2, column=1)
    entry_email.grid(row=3, column=1)

    tk.Button(add_student_window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2)

# Function to generate and display attendance reports
def generate_attendance_report():
    query = """
    SELECT 
        a.AttendanceID, 
        s.FirstName, 
        s.LastName, 
        a.Timestamp 
    FROM 
        Attendance a 
    JOIN 
        Student s 
    ON 
        a.StudentID = s.StudentID
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["AttendanceID", "FirstName", "LastName", "Timestamp"]
    df = pd.DataFrame(rows, columns=columns)

    # Convert Timestamp to datetime and group by date
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Date"] = df["Timestamp"].dt.date
    trend = df.groupby("Date").size()

    # Plot the attendance trend
    plt.figure(figsize=(10, 6))
    trend.plot(kind="line", marker="o")
    plt.title("Attendance Trends Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Attendances")
    plt.grid()
    plt.show()

# Main GUI window
root = tk.Tk()
root.title("Facial Recognition Attendance System")

tk.Label(root, text="Facial Recognition Attendance System", font=("Arial", 16)).pack(pady=20)

tk.Button(root, text="Take Attendance", command=take_attendance, width=20).pack(pady=10)
tk.Button(root, text="Add Student", command=add_student, width=20).pack(pady=10)
tk.Button(root, text="View Attendance Report", command=generate_attendance_report, width=20).pack(pady=10)

root.mainloop()
