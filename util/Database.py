import random
from flask_pymongo import PyMongo

CHARSET = "1234567890QWERTYUIOPASDFGHJKLZXCVBNM"

class DBTools:

    def __init__(self, app):
        self.mongo = PyMongo(app)

    def registerSuperAdmin(self, username, password):
        if self.mongo.db.superAdmin.find({'username' : username}).limit(1).count() != 0:
            return 'User already exists!'
        self.mongo.db.superAdmin.insert({
            'username' : username,
            'password' : password,
            'schools' : []
        })
        return 'User added.'

    def registerSchool(self, username, schoolName):
        schoolID = ''.join(random.choice(CHARSET) for x in range(10))
        while self.mongo.db.school.find({'schoolID' : schoolID}).limit(1).count() != 0:
            schoolID += random.choice(CHARSET)
        self.mongo.db.school.insert({ #Registers new school to database
            'schoolID' : schoolID,
            'schoolName' : schoolName,
            'admins' : [],
            'students' : [],
            'teachers' : [],
            'classes' : []
        })
        self.mongo.db.superAdmin.update({ 'username' : username }, { #Add school to user's school list
            '$push' : {'schools' : schoolID}
        })
    
    def addStudent(self, username, schoolID, studentName, studentID):
        if not(self.checkAdmin(schoolID, username)):
            return "User is not an admin of this school!"
        if self.checkStudentExists(schoolID, studentID):
            return "Student already exists!"
        name = studentName.strip().split(' ')
        gennedName = (name[0][0] + name[-1]).lower() + random.choice(CHARSET[:10]) #flast
        checkStudentUsername = {
            'schoolID' : schoolID,
            'students.student' : gennedName
        }
        while self.mongo.db.school.find(checkStudentUsername).limit(1).count() != 0: #Ensures no identical usernames
            gennedName += random.choice(CHARSET[:10])
        self.mongo.db.school.update({'schoolID' : schoolID}, {
            '$push' : {
                'students' : {
                    'username' : gennedName,
                    'password' : studentID,
                    'classes' : [],
                    'name' : name,
                    'studentID' : studentID
                }
            }
        })

    def addAdmin(self, username, schoolID, adminUsername, adminPass, name):
        superAdminCheck = {
            'username' : username,
            'schools' : schoolID
        }
        if self.mongo.db.superAdmin.find(superAdminCheck).limit(1).count() == 0:
            return "User is not a super admin of this school!"
        if self.checkAdmin(schoolID, adminUsername):
            return "Admin already exists!"
        name = name.strip().split(' ')
        self.mongo.db.school.update({'schoolID' : schoolID}, {
            '$push' : {
                'admins' : {
                    'username' : adminUsername,
                    'password' : adminPass,
                    'name' : name
                }
            }
        })
        return "Admin added."

    def addClass(self, username, schoolID, className, teacherID = None):
        if not(self.checkAdmin(schoolID, username)):
            return "User is not an admin of this school!"
        classID = ''.join(random.choice(CHARSET) for x in range(5))
        while self.checkClassExists(schoolID, classID):
            classID += random.choice(CHARSET)
        self.mongo.db.school.update({'schoolID' : schoolID}, { #Add class to school's class list
            "$push" : {
                'classes' : {
                    'classID' : classID,
                    'students' : [],
                    'teacher' : teacherID,
                    'className' : className,
                    'posts' : []
                }
            }
        })
        return "Class added."
    
    def addStudentClass(self, username, schoolID, classID, studentID):
        if not(self.checkAdmin(schoolID, username)):
            return "User is not an admin of this school!"
        if not(self.checkClassExists(schoolID, classID)):
            return "This class does not exist!"
        if not(self.checkStudentExists(schoolID, studentID)):
            return "This student does not exist!"
        classSelector = { #Selects the class with a matching classID
            'schoolID' : schoolID,
            'classes.classID' : classID
        }
        for i in self.mongo.db.school.find(classSelector):
            print(i)
        self.mongo.db.school.update(classSelector, { #Add student to class's student list
            '$push' : {
                'classes.students' : studentID
            }
        })
        studentSelector = { #Selects the student with a matching studentID
            'schoolID' : schoolID,
            'students.studentID' : studentID
        }
        self.mongo.db.school.update(studentSelector, {
            '$push' : {
                'students.classes' : classID
            }
        })
        return 'Class added to student.'
    
    def checkAdmin(self, schoolID, username):
        adminCheck = {
            'schoolID' : schoolID,
            'admins.username' : username
        }
        return self.mongo.db.school.find(adminCheck).limit(1).count() != 0
    
    def checkClassExists(self, schoolID, classID):
        classCheck = {
            'schoolID' : schoolID,
            'classes.classID' : classID
        }
        return self.mongo.db.school.find(classCheck).limit(1).count() != 0

    def checkStudentExists(self, schoolID, studentID):
        studentCheck = {
            'schoolID' : schoolID,
            'students.studentID' : studentID
        }
        return self.mongo.db.school.find(studentCheck).limit(1).count() != 0
    
    def getSchoolIDs(self, username):
        return [x['schools'] for x in self.mongo.db.superAdmin.find({'username' : username}).limit(1)][0]