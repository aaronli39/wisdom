import random
from flask_pymongo import PyMongo

CHARSET = set("1234567890QWERTYUIOPASDFGHJKLZXCVBNM")

class DBTools:

    def __init__(self, app):
        self.mongo = PyMongo(app)

    def registerSuperUser(self, username, password):
        if self.mongo.db.superAdmin.find({'username' : username}).limit(1).size() != 0:
            return 'User already exists!'
        self.mongo.db.superAdmin.insert({
            'username' : username,
            'password' : password,
            'schools' : []
        })
        return 'User added.'

    def registerSchool(self, username, schoolName):
        schoolID = ''.join(random.choice(CHARSET) for x in range(10))
        while self.mongo.db.school.find({'schoolID' : schoolID}).limit(1).size() != 0:
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
            {
                '$push' : {'schools' : schoolID}
            }
        })