import cv2
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="AttendanceSystem"
)
cursor = db.cursor()

# Function to add student to database
def add_student_to_database(first_name, last_name, major, email):
    sql = "INSERT INTO Student (FirstName, LastName, Major, Email, ClassID) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (first_name, last_name, major, email, None))  # Assign ClassID as None initially
    db.commit()
    print(f"Student {first_name} {last_name} added to database.")

# Collect facial data
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

user_id = input("Enter your ID: ")
first_name = input("Enter your First Name: ")
last_name = input("Enter your Last Name: ")
major = input("Enter your Major: ")
email = input("Enter your Email: ")

add_student_to_database(first_name, last_name, major, email)

count = 0
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        count += 1
        cv2.imwrite(f"dataset/User.{user_id}.{count}.jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q") or count >= 30:
        break

cap.release()
cv2.destroyAllWindows()
