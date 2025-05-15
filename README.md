# 🧑‍💻 Face Recognition Attendance System

A Python-based face recognition attendance system using OpenCV, face_recognition, SQLite, and Tkinter for GUI.

This project captures real-time webcam input, detects and identifies faces, and records attendance with timestamps into a local database.

---

## 📸 Features

- Real-time face recognition using webcam
- Attendance logged with name, date, and time
- Recent attendance displayed via GUI popup
- Attendance records saved in SQLite database
- Easy to update images for new faces
- Clean and simple GUI using Tkinter

---

## 🗂 Project Structure

face-recognition-attendance/

| File / Folder        | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `ImagesAttendance/`  | Folder to store images of known people (used for face recognition).                         |
| `Taylor Swift.jpg`   | Example image inside `ImagesAttendance/`. Represents a known person.                        |
| `Selena Gomez.jpg`   | Another example image. You can add/remove images as needed.                                 |
| `create_database.py` | Script to create the SQLite database (`Attendance.db`) and required table.                  |
| `main.py`            | Main GUI application with real-time webcam-based face recognition and attendance tracking.  |
| `Attendance.db`      | SQLite database storing attendance records (auto-created; ignored in Git).                  |
| `requirements.txt`   | Contains the list of Python libraries required to run the project.                          |
| `.gitignore`         | Specifies which files/folders should be ignored by Git (e.g., `.db`, `__pycache__/`, etc.). |
| `README.md`          | Project documentation and usage instructions.                                               |


## ⚙️ Requirements

Install all dependencies using:

```
bash
pip install -r requirements.txt
```

### Key libraries used:

- opencv-python
- face_recognition
- numpy
- tkinter 
- sqlite3 

Note: face_recognition library is dpendant on cmake and dlib. Make sure to install those before proceeding !

```
pip install cmake
pip install dlib
pip install face_recognition
```

## 🚀 How to Run ?

1. Clone the repository:

   ```
   git clone https://github.com/YOUR-USERNAME/face-recognition-attendance.git
   cd face-recognition-attendance
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the database:

   Run this once to create the Attendance.db file.
   ```
   python create_database.py
   ```
4. Add known face images:

   Place images of people you want to recognize inside the 'ImagesAttendance' folder. Use .jpg or .png files with clear front-facing faces. The filename (without extension) becomes the person's name.
5. Run the main program:
   ```
   python main.py
   ```
6. Usage:

- Click "Start Attendance" to activate the webcam and begin recognition.
- Click "View Recent Attendance" to see the last 10 records.
- A .xlsx file is automatically generated that stores the attendance record when "View Recent Attendance" is clicked.
- Attendance is automatically saved to the local SQLite database.

## 📦 Output
Attendance records are stored in:

Attendance.db (SQLite Database)

Each record includes:

- Name
- Time
- Date
