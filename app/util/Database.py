import random
from flask_pymongo import PyMongo

CHARSET = "1234567890QWERTYUIOPASDFGHJKLZXCVBNM"

class DBTools:

    def __init__(self, app):
        self.mongo = PyMongo(app)

    def registerAdmin(self, username, password):
        if self.checkAdminExists(username):
            return 'User already exists!'
        self.mongo.db.admin.insert({
            'username' : username,
            'password' : password,
            'schools' : []
        })
        return 'Registration successful.'

    def registerSchool(self, username, schoolName):
        schoolID = ''.join(random.choice(CHARSET) for x in range(10))
        while self.mongo.db.school.find({'schoolID' : schoolID}).limit(1).count() != 0:
            schoolID += random.choice(CHARSET)
        self.mongo.db.school.insert({ #Registers new school to database
            'schoolID' : schoolID,
            'schoolName' : schoolName,
            'admins' : [username],
            'students' : [],
            'teachers' : [],
            'classes' : []
        })
        self.mongo.db.admin.update({ 'username' : username }, { #Add school to user's school list
            '$push' : {'schools' : schoolID}
        })
    
    def addStudent(self, username, schoolID, studentName, studentID, skipAdminCheck = False):
        if not(skipAdminCheck):
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

    def addStudentsFromCSV(self, username, schoolID, csv):
        if not(self.checkAdmin(schoolID, username)):
            return "User is not an admin of this school!"
        csv = [[value.strip() for value in line.split(',')] for line in csv.split('\n')[1:]]
        for studentInfo in csv:
            if len(studentInfo) < 2:
                continue
            self.addStudent(username, schoolID, studentInfo[0], studentInfo[1], skipAdminCheck = True)

    def addAdmin(self, username, schoolID, adminUsername):
        if not(self.checkAdminExists(adminUsername)):
            return "This user doesn't exist!"
        adminCheck = {
            'username' : username,
            'schools' : schoolID
        }
        if self.mongo.db.admin.find(adminCheck).limit(1).count() == 0:
            return "User is not an admin of this school!"
        if self.checkAdmin(schoolID, adminUsername):
            return "This user is already an admin!"
        self.mongo.db.school.update({'schoolID' : schoolID}, { #Add user to admins list
            '$push' : {
                'admins' : adminUsername
            }
        })
        self.mongo.db.admin.update({'username' : adminUsername}, { #Add school to admin's school list
            '$push' : {
                'schools' : schoolID
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
        if self.checkStudentInClass(schoolID, studentID, classID):
            return "This student is already in this class!"
        classSelector = { #Selects the class with a matching classID
            'schoolID' : schoolID,
            'classes.classID' : classID
        }
        self.mongo.db.school.update(classSelector, { #Add student to class's student list
            '$push' : {
                'classes.$.students' : studentID
            }
        })
        studentSelector = { #Selects the student with a matching studentID
            'schoolID' : schoolID,
            'students.studentID' : studentID
        }
        self.mongo.db.school.update(studentSelector, {
            '$push' : {
                'students.$.classes' : classID
            }
        })
        return 'Class added to student.'
    
    def checkAdmin(self, schoolID, username):
        adminCheck = {
            'schoolID' : schoolID,
            'admins' : username
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
    
    def checkAdminExists(self, username):
        return self.mongo.db.admin.find({'username' : username}).limit(1).count() != 0
    
    def checkStudentInClass(self, schoolID, studentID, classID):
        inClassCheck = {
            'schoolID' : schoolID,
            'classes' : {
                '$elemMatch' : {
                    'classID' : classID,
                    'students' : studentID
                }
            }
        }
        return self.mongo.db.school.find(inClassCheck).limit(1).count() != 0

    def getSchoolIDs(self, username):
        return [x['schools'] for x in self.mongo.db.admin.find({'username' : username}).limit(1)][0]
    
    def authAdmin(self, username, password):
        authCheck = {
            'username' : username,
            'password' : password
        }
        return self.mongo.db.admin.find(authCheck).limit(1).count() != 0
    
    def authStudent(self, schoolID, username, password):
        authCheck = {
            'schoolID' : schoolID,
            'students.username' : username,
            'students.password' : password
        }
        return self.mongo.db.school.find(authCheck).limit(1).count() != 0
    
    def getSchoolInfo(self, schoolID):
        for i in self.mongo.db.school.find({'schoolID' : schoolID}).limit(1):
            return i
    
    def getBasicSchoolInfo(self, username):
        schoolIDs = self.getSchoolIDs(username)
        #[School Name, School ID, Number of Students]
        output = []
        for currID in schoolIDs:
            currSchool = self.getSchoolInfo(currID)
            output.append([currSchool['schoolName'], currID, len(currSchool['students'])])