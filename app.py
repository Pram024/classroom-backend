from flask import Flask, request, json, jsonify
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def testConnection():
    return "connected"

@app.route('/register', methods=["POST"])
def register():
    userData = []

    # kalau file users-file.json udah ada, di read dulu. kalau file ga ada, ga usah di read, langsung write
    if os.path.exists('./users-file.json'):
        userFile = open('./users-file.json', 'r')
        userData = json.load(userFile)

    body = request.json
    for user in userData:
        if body["userId"] == user["userId"]:
            return "ID YANG ANDA MASUKAN SUDAH ADA GAN"
        elif body["username"] == user["username"]:
            return "USERNAME YANG ANDA MASUKAN SUDAH ADA GAN"
        elif body["email"] == user["email"]:
            return "EMAIL YANG ANDA MASUKAN SUDAH ADA GAN"
        
    body["classes_as_student"]=[]
    body["classes_as_teacher"]=[]
    userData.append(body)

    # siapin file buat di write
    userFile = open('./users-file.json', 'w')
    userFile.write(json.dumps(userData))

    return jsonify(userData)

@app.route('/login', methods=["POST"])
def login():
    response = {}
    response["message"] = "login failed. username or password SALAH"
    response["data"] = {}
    body = request.json

    # siapin file buat di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)

    for user in userData:
        if body["username"] == user["username"]:
            if body["password"] == user["password"]:
                response["message"]="login succses, welcome {}".format(user["fullName"])
                response["data"] = user
            break             
            #     # return "Login succes, welcome {}".format(user["fullName"])
            # else:
            #     response["message"] = "login failed. username or password"
                # return "Login failed. Wrong password"
    return jsonify(response)

@app.route('/users/<int:id>', methods=["GET"])
def getUser(id):
    # siapin file buat di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)

    for user in userData:
        if id == user["userId"]:
            return jsonify(user)

    return "User ID {} is not found".format(id)

@app.route('/users', methods=["GET"])
def getAllUsers():
    # siapin file buat di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)

    return jsonify(userData)

@app.route('/class', methods=["POST"])
def createClass():
    classesData = []

    body = request.json
    body["students"] = []
    body["classwork"] = []

    if os.path.exists('./classes-file.json'):
        classesFile = open('./classes-file.json', 'r')
        classesData = json.load(classesFile)
    
    for class_ in classesData:
        if body["classname"] == class_["classname"]:
            return "CLASS YANG ANDA MASUKAN SUDAH ADA GAN"

    for class_ in classesData:
        if body["classid"] == class_["classid"]:
            return "GANTI NO CLASSIDNYA KARENA KELAS SUDAH ADA TEACHERNYA"

    for class_ in classesData:
        if body["teachers"] == class_["teachers"]:
            return "GANTI TEACHER KARENA KELAS SUDAH ADA TEACHERNYA"

    classesData.append(body)

    # siapin file buat di write
    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(classesData))

    # MENAMBAHKAN CLASSES AS TEACHER DI USER FILE
    usersFile = open('./users-file.json', 'r')
    usersTeac = json.load(usersFile)

    for user in usersTeac:
        if body["teachers"] == user["userId"]:
            if body["teachers"] not in user["classes_as_teacher"]:
                user["classes_as_teacher"].append(body["classid"])
    
    usersFile = open('./users-file.json', 'w')
    usersFile.write(json.dumps(usersTeac))

    return jsonify(classesData)

@app.route('/class/<int:id>', methods=["GET"])
def getClass(id):
    # read data di user
    userData = getAllUsers().json
    # siapin file buat di read
    classesFile = open('./classes-file.json', 'r')
    classesData = json.load(classesFile)
    # mencari kelas dengan yang sama di classID dan mengosongkan students agar bisa di isi fullname
    for class_ in classesData:
        if id == class_["classid"]:
            class_["students"]=[]
            break
    # mengambil fullname untuk menggantikan userId yang di tampilkan students
    for user in userData:
        if id in user["classes_as_student"]:
            class_["students"].append(user["fullName"])
    return jsonify(class_)

    # return "User ID {} is not found".format(id)

@app.route('/classes', methods=["GET"])
def getAllClasses():
    
    # siapin file buat di read
    classesFile = open('./classes-file.json', 'r')
    classesData = json.load(classesFile)

    return jsonify(classesData)

@app.route('/joinClass', methods=["POST"])
def joinClass():
    body = request.json
 
    # nambahin userid ke classes-file
    classesFile = open('./classes-file.json', 'r')
    classesData = json.load(classesFile)

    for class_ in classesData:
        if body["classid"] == class_["classid"]:
            if body["userId"] not in class_["students"]:
                class_["students"].append(body["userId"])
    
    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(classesData))

    # nambahin class_as_student ke users-file
    usersFile = open('./users-file.json', 'r')
    usersData = json.load(usersFile)

    for user in usersData:
        if body["userId"] == user["userId"]:
            if body["classid"] not in user["classes_as_student"]:
                user["classes_as_student"].append(body["classid"])
    
    usersFile = open('./users-file.json', 'w')
    usersFile.write(json.dumps(usersData))
    # userFile.close()
    return "success"

@app.route('/updateUser/<int:id>', methods=["PUT"])
def updateUser(id):
    userData = getAllUsers().json
    body = request.json

    for user in userData:
        if id == user["userId"]:
            user["username"] = body["username"]
            user["fullName"] = body["fullName"]
            user["password"] = body["password"]
            user["email"] = body["email"]
            
    userFile = open('./users-file.json', 'w')
    userFile.write(json.dumps(userData))
    return jsonify(body)

@app.route('/updateClass/<int:id>', methods=["PUT"])
def updateClass(id):
    class_Data = getAllClasses().json
    body = request.json

    for class_ in class_Data:
        if id == class_["classid"]:
            class_["classname"] = body["classname"]
            
    class_File = open('./classes-file.json', 'w')
    class_File.write(json.dumps(class_Data))
    return jsonify(body)

@app.route('/classwork', methods=["POST"])
def creatClassWork():
    workData = []

    # kalau file users-file.json udah ada, di read dulu. kalau file ga ada, ga usah di read, langsung write
    if os.path.exists('./classwork-file.json'):
        workFile = open('./classwork-file.json', 'r')
        workData = json.load(workFile)
  

    body = request.json
    for work in workData:
        if body["classworkid"] == work["classworkid"]:
            return "ID ANDA MASUKAN SUDAH ADA GAN"
   
    body["answers"]=[]
    workData.append(body)
    
    # siapin file buat di write
    workFile = open('./classwork-file.json', 'w')
    workFile.write(json.dumps(workData))

            
  # menambahkan classworkid di classwork yang ada di database classes-file
    classesFile = open('./classes-file.json', 'r')
    classesData = json.load(classesFile)
    for class_ in classesData:
        if body["class"] == class_["classid"]:
            if body["classworkid"] not in class_["classwork"]:
                class_["classwork"].append(body["classworkid"])           
    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(classesData))

    return jsonify(workData)

@app.route('/classwork/<int:id>', methods=["GET"])
def getclasswork(id):
    # siapin file buat di read
    userFile = open('./classwork-file.json', 'r')
    userData = json.load(userFile)

    for work in userData:
        if id == work["classworkid"]:
            return jsonify(work)

    return "User ID {} is not found".format(id)

@app.route('/classworks', methods=["GET"])
def getAllClasswork():
    # siapin file buat di read
    workFile = open('./classwork-file.json', 'r')
    workData = json.load(workFile)

    return jsonify(workData)

@app.route('/assignclasswork/<int:id>', methods=["POST"])
def assignClassWork(id):
    body = request.json
 
    # nambahin userid ke classes-file
    workFile = open('./classwork-file.json', 'r')
    workData = json.load(workFile)

    for work in workData:
        if id == work["classworkid"]:
            work["answers"].append(body)
    
    workFile = open('./classwork-file.json', 'w')
    workFile.write(json.dumps(workData))

    return "TUGAS ANDA TELAH BERHASIL DIKIRIM"

@app.route('/updateclasswork/<int:id>', methods=["PUT"])
def updateclasswork(id):
    workData = getAllClasswork().json
    body = request.json

    for work in workData:
        if id == work["classworkid"]:
            work["question"] = body["question"]
            
    workFile = open('./classWORK-file.json', 'w')
    workFile.write(json.dumps(workData))
    return "UPDATE QUESTION ANDA BERHASIL"

@app.route('/outclass/<int:id>', methods=["POST"])
def outClass(id):
    body = request.json
    # siapin file buat di read
    userData = getAllUsers().json
    class_Data = getAllClasses().json

    for kelas in class_Data:
        if id == kelas["classid"]:
            for user in userData:
                 if user["userId"] == body["userId"]:
                    user["classes_as_student"].remove(id)
                    kelas["students"].remove(user["userId"])

    usersFile = open('./users-file.json', 'w')
    usersFile.write(json.dumps(userData))

    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(class_Data))

    return "ANDA TELAH KELUAR KELAS"

    # return "User ID {} is not found".format(id)

@app.route('/deleteclasswork/<int:id>', methods=["POST"])
def deleteClassWork(id):
    # siapin file buat di read
    workData = getAllClasswork().json
    class_Data = getAllClasses().json

    for work in workData:
        if id == work["classworkid"]:
            workData.remove(work)
    for kelas in class_Data:
        if id in kelas["classwork"]:
            kelas["classwork"].remove(id)

                
    usersFile = open('./classwork-file.json', 'w')
    usersFile.write(json.dumps(workData))

    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(class_Data))

    return "CLASSWORK BERHASIL DI HAPUS"

    # return "User ID {} is not found".format(id)

@app.route('/deleteclass/<int:id>', methods=["POST"])
def deleteClass(id):
    # siapin file buat di read
    userData = getAllUsers().json
    workData = getAllClasswork().json
    class_Data = getAllClasses().json

    for kelas in class_Data:
        if id == kelas["classid"]:
            class_Data.remove(kelas)
    for work in workData:
        if id == work["class"]:
            workData.remove(work)
    for user in userData:
        if id in user["classes_as_student"]:
            user["classes_as_student"].remove(id)
    for user in userData:
        if id in user["classes_as_teacher"]:
            user["classes_as_teacher"].remove(id)

                
    usersFile = open('./classwork-file.json', 'w')
    usersFile.write(json.dumps(workData))

    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(class_Data))

    userFile = open('./users-file.json', 'w')
    userFile.write(json.dumps(userData))

    return "CLASS ANDA BERHASIL DI HAPUS"

    # return "User ID {} is not found".format(id)