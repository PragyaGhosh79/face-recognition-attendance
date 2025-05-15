import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import sqlite3
import pandas as pd
import subprocess
import platform

# Load known images
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if encode:
            encodeList.append(encode[0])
    return encodeList

encodeListKnown = findEncodings(images)

def markAttendance(name):
    time_now = datetime.now()
    tString = time_now.strftime('%H:%M:%S')
    dString = time_now.strftime('%d/%m/%Y')
    conn = sqlite3.connect('Attendance.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, time TEXT, date TEXT)")
    c.execute("SELECT * FROM attendance WHERE name=? AND date=?", (name, dString))
    data = c.fetchall()
    if len(data) == 0:
        c.execute("INSERT INTO attendance (name, time, date) VALUES (?, ?, ?)", (name, tString, dString))
        conn.commit()
    conn.close()

def startAttendance():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                markAttendance(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
        cv2.imshow('Webcam - Press ESC to exit', img)
        if cv2.waitKey(10) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def showAttendance():
    conn = sqlite3.connect('Attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()

    if not rows:
        messagebox.showinfo("Attendance Records", "No attendance records found.")
        return

    # Display in messagebox
    records = "\n".join([f"{r[1]} - {r[2]} - {r[3]}" for r in rows])
    messagebox.showinfo("Recent Attendance", records)

    # Export to Excel
    df = pd.DataFrame(rows, columns=["ID", "Name", "Time", "Date"])
    file_path = "Attendance.xlsx"
    df.to_excel(file_path, index=False)

    # Open Excel file
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", file_path])
        else:  # Linux
            subprocess.call(["xdg-open", file_path])
    except Exception as e:
        print("Could not open Excel file:", e)

# GUI setup
window = tk.Tk()
window.title("Face Recognition Attendance")
window.geometry("400x300")

tk.Label(window, text="Face Recognition Attendance System", font=("Helvetica", 16)).pack(pady=20)
tk.Button(window, text="Start Attendance", command=startAttendance, width=25).pack(pady=10)
tk.Button(window, text="View Recent Attendance", command=showAttendance, width=25).pack(pady=10)
tk.Button(window, text="Exit", command=window.quit, width=25).pack(pady=10)

window.mainloop()
