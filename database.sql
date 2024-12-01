-- Create database
CREATE DATABASE AttendanceSystem;

-- Use the database
USE AttendanceSystem;

-- Professor table
CREATE TABLE Professor (
    ProfessorID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Department VARCHAR(50),
    RoomID INT,
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

-- Room table
CREATE TABLE Room (
    RoomID INT AUTO_INCREMENT PRIMARY KEY,
    RoomName VARCHAR(50),
    Building VARCHAR(50),
    Capacity INT
);

-- Class table
CREATE TABLE Class (
    ClassID INT AUTO_INCREMENT PRIMARY KEY,
    ClassName VARCHAR(100),
    ClassCode VARCHAR(50),
    ProfessorID INT,
    RoomID INT,
    FOREIGN KEY (ProfessorID) REFERENCES Professor(ProfessorID),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

-- Student table
CREATE TABLE Student (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Major VARCHAR(50),
    Email VARCHAR(100),
    ClassID INT,
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
);