# Welcome to Wisdom: your student management solution

---

This student management app aims to give you, an admin, an easier time generating and managing a school system

[Link](https://ftf-final-project-goldman.herokuapp.com/) to app
----
## Installation (on linux machine)
1) install virtual env (python3-venv) with `sudo apt install python3-venv`
2) run `python3 -m venv ~/venv` to create virtual env directory in the home directory
3) run `. ~/venv/bin/activate` to activate virtual env
4) run `pip3 install -r requirements.txt` to install requirements
5) run `python3 app.py` to run app on localhost 5000

-----
## Features
* When you create an account, it is an admin account that allows you to create and manage a school
* once you create an account, users can import a student CSV file (roster). There is an example csv file in the `utils` directory
* once a school is created and students are added, you can create classes, and add students to classes with their ID
* you can dynamically search for created classes, students, and their schedules
* click on a searched class to go to the class page
* teachers can be created by admins and they can both create class posts which students can see
* posts with due dates (Eg assignments) will be pushed to MongoDB and the class calendar
