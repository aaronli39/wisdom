def genStudentAccDct(csv): #CSV should be in the format studentName,OSIS/ID# with the first line being a header
    #[ [ [First, ..., Last], [OSIS/ID#] ] ]
    csv = [[value.strip().split(' ') for value in line.split(',')] for line in csv.split('\n')[1:]]
    collisionDct = {} #Generated Name : count
    output = [] # [ { username : gennedName, password : identifier } ]
    for student in csv:
        name = student[0]
        identifier = student[1][0]
        gennedName = (name[0][0] + name[1]).lower() #flast
        if gennedName in collisionDct: #Adds a number to the end of the generated name if it already exists
            gennedName += str(collisionDct[gennedName])
        else:
            collisionDct[gennedName] = 1
        output.append({
            'username' : gennedName,
            'password' : identifier,
            'classes' : [],
            'name' : name,
            'studentID' : identifier
        })
    return output

print(genStudentAccDct(open('exampleStudents.csv', 'r').read()))
