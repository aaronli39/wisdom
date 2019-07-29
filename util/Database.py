import random
from flask_pymongo import PyMongo

CHARSET = set("1234567890QWERTYUIOPASDFGHJKLZXCVBNM")

databasePass = "Something"

mongo = PyMongo(app = None, uri = f"Something{databasePass}Something")

def registerSuperUser(username, password):
    if mongo.db.superAdmin.find({'username' : username}).limit(1).size() != 0:
        return 'User already exists!'
    mongo.db.superAdmin.insert({
        'username' : username,
        'password' : password,
        'schools' : []
    })
    return 'User added.'

def registerSchool(username, schoolName):
    schoolID = ''.join(random.choice(CHARSET) for x in range(10))
    while mongo.db.school.find({'schoolID' : schoolID}).limit(1).size() != 0:
        schoolID += random.choice(CHARSET)
    mongo.db.school.insert({ #Registers new school to database
        'schoolID' : schoolID,
        'schoolName' : schoolName,
        'admins' : [],
        'students' : [],
        'teachers' : [],
        'classes' : []
    })
    mongo.db.superAdmin.update({ 'username' : username }, { #Add school to user's school list
        {
            '$push' : {'schools' : schoolID}
        }
    })

if __name__ == '__main__':
    registerSuperUser('Kevin', '1234')
    registerSchool('Kevin', 'Stuyvesant High School')