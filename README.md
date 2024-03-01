Food Ordering Python Project
This project is a Flask application that allows users to create, update, delete, and search for tasks related to food ordering. The tasks are stored in a MySQL database and have a title, a description, a time, and a completion status. The application also sends a message to the user when the current time matches the time of any task.
Installation
To run this project, you need to have Python 3, Flask, and MySQL installed on your system. You also need to create a database named mydb and a table named ToDo with the following schema:

Column	Type	Constraint
id	Integer	Primary Key
title	String(80)	Not Null
task	String(120)	Not Null
time	String(6)	Not Null
timestamp	DateTime	Default: Current Time
task_completed	Integer	Default: 0
You can use the following SQL commands to create the database and the table:

SQL

CREATE DATABASE mydb;
USE mydb;
CREATE TABLE ToDo (
    id INT PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    task VARCHAR(120) NOT NULL,
    time VARCHAR(6) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    task_completed INT DEFAULT 0
);

Usage
To run the application, you need to execute the app.py file using the following command:

python app.py

The application will run on http://localhost:5000/ by default. You can use the following routes to interact with the application:

/: This route will return a message with the current time and the tasks that match the time, if any.
/create_todo: This route will create a new task in the database. You need to send a JSON object with the following keys: title, task, and time. The time should be in the format of HH:MM. For example:
JSON

{
    "title": "Order pizza",
    "task": "Call the pizza place and order a large cheese pizza",
    "time": "18:30"
}

/delete_task: This route will delete an existing task from the database. You need to send a JSON object with the key id, which is the primary key of the task. For example:
JSON

{
    "id": 1
}

/update_task: This route will update an existing task in the database. You need to send a JSON object with the key id, which is the primary key of the task, and the keys title and task, which are the new values for the task. For example:
JSON

{
    "id": 2,
    "title": "Order salad",
    "task": "Go to the salad bar and order a Caesar salad"
}

/search: This route will search for tasks that contain a given query in their description. You need to send a JSON object with the key query, which is the search term. For example:
JSON

{
    "query": "pizza"
}

/task_completed: This route will mark a task as completed in the database. You need to send a JSON object with the key id, which is the primary key of the task. For example:
JSON

{
    "id": 3
}

License
This project is licensed under the MIT License. See the LICENSE file for details
