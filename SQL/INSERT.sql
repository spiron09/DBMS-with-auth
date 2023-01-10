USE DrivingSchool;

INSERT INTO Student  VALUES 
(1, 'John', 'Smith', '5551234567', 'john.smith@gmail.com'),
(2, 'Jane', 'Doe', '5554567890', 'jane.doe@gmail.com'),
(3, 'Robert', 'Johnson', '5557890123', 'robert.johnson@gmail.com');

INSERT INTO Instructors VALUES
(1, 'Mike', 'Williams', '5551234567', 'mike.williams@gmail.com', '123 Main St'),
(2, 'Sarah', 'Johnson', '5554567890', 'sarah.johnson@gmail.com', '456 Park Ave'),
(3, 'Chris', 'Thompson', '5557890123', 'chris.thompson@gmail.com', '789 Maple St');

INSERT INTO Vehicles VALUES
(1, 'Honda', 'Civic', 2018),
(2, 'Toyota', 'Corolla', 2016),
(3, 'Subaru', 'Outback', 2019);

INSERT INTO Lessons VALUES 
(1, 1, 1, 1, '2020-05-01', '10:00', 2),
(2, 1, 2, 2, '2020-05-02', '13:00', 1),
(3, 2, 3, 3, '2020-05-03', '15:00', 1.5),
(4, 3, 1, 1, '2020-05-04', '17:00', 2);

INSERT INTO Payment VALUES 
(1, 1, 100.00, '2020-05-01', 'Cash'),
(2, 1, 50.00, '2020-05-02', 'Credit'),
(3, 2, 75.00, '2020-05-03', 'Debit'),
(4, 3, 125.00, '2020-05-04', 'Check');