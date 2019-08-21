from flask import Flask, request, json, jsonify
import os

from src.utils.fungsi import readFile, writeFile
from src.utils.crypt import encryp, decryp
from src.utils.authorization import encode

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ------------------ functions --------------------------------------
userFileLocation = 'src/data/users-file.json'
classFileLocation = 'src/data/classes-file.json'
classworkFileLocation = 'src/data/classwork-file.json'
# ------------------ routes -----------------------------------------

@app.route('/')
def testConnection():
    return "connected"

@app.route('/register', methods=["POST"])
def register():
    userData = []
    body = request.json
    body["classes_as_student"]=[]
    body["classes_as_teacher"]=[]

    response = {}
    response["message"] = "Creat class SUKSES"
    response["data"] = {}

    # kalau file users-file.json udah ada, di read dulu. kalau file ga ada, ga usah di read, langsung write
    userData = readFile(userFileLocation)

    AlreadyExist = False
    for user in userData:
        if user["userId"] == body["userId"]:
            response["message"] = "User ID {} is already exist".format(body["userId"])
            AlreadyExist = True
        elif user["username"] == body["username"]:
            response["message"] = "username {} is already exist".format(body["username"])
            AlreadyExist = True
        elif user["email"] == body["email"]:
            response["message"] = "email {} is already exist".format(body["email"])
            AlreadyExist = True
            break
        

    if not AlreadyExist:
        response["data"] = body
        body["password"] = encryp(body["password"])
        userData.append(body)

        # siapin file buat di write
        writeFile(userFileLocation, userData)

    return jsonify(response)

@app.route('/login', methods=["POST"])
def login():
    response = {}
    response["message"] = "login failed. username or password SALAH"
    response["data"] = {}
    body = request.json

    # siapin file buat di read
    userData = readFile(userFileLocation)

    for user in userData:
        if body["username"] == user["username"]:
            if body["password"] == decryp(user["password"]):
                response["message"]="login succses, welcome {}".format(user["fullName"])
                response["data"] = user
                # response["token"] = encode(response["data"])
            break             
    return jsonify(response)

@app.route('/users/<int:id>', methods=["GET"])
def getUser(id):
    response = {}
    response["message"] = "User ID {} is not found".format(id)
    response["data"] = {}

    # siapin file buat di read
    userData = readFile(userFileLocation)
    for user in userData:
        if id == user["userId"]:
            response["message"] = "User Found"
            response["data"] = user
            break

    return jsonify(response)

@app.route('/users', methods=["GET"])
def getAllUsers():
    # siapin file buat di read
    userData = readFile(userFileLocation)

    return jsonify(userData)

@app.route('/class', methods=["POST"])
def createClass():
    classesData = []

    body = request.json
    body["students"] = []
    body["classwork"] = []

    response = {}
    response["message"] = "Creat class SUKSES"
    response["data"] = {}

    classesData = readFile(classFileLocation)
        
        # check class id apakah sudah ada
    classidAlreadyExist = False
    for class_ in classesData:
        if class_["classid"] == body["classid"]:
            response["message"] = "Class ID {} is already exist".format(body["classid"])
            classidAlreadyExist = True
        elif class_["classname"] == body["classname"]:
            response["message"] = "Class Name {} is already exist".format(body["classname"])
            classidAlreadyExist = True
        elif class_["teachers"] == body["teachers"]:
            response["message"] = "Teacher {} is already exist".format(body["teachers"])
            classidAlreadyExist = True
            break

    if not classidAlreadyExist:
        response["data"] = body
        classesData.append(body)

            # siapin file buat di write
        writeFile(classFileLocation, classesData)

        # MENAMBAHKAN CLASSES AS TEACHER DI USER FILE
        usersTeac = readFile(userFileLocation)

        for user in usersTeac:
            if body["teachers"] == user["userId"]:
                if body["teachers"] not in user["classes_as_teacher"]:
                    user["classes_as_teacher"].append(body["classid"])
        
        writeFile(userFileLocation, usersTeac)

    return jsonify(response)
@app.route('/class/<int:id>', methods=["GET"])
def getClass(id):
    response = {}
    response["message"] = "Class with classid {} is not found.".format(id)
    response["data"] = {}

    # read data di user
    userData = getAllUsers().json
    # siapin file buat di read
    classesData = readFile(classFileLocation)
    # mencari kelas dengan yang sama di classID dan mengosongkan students agar bisa di isi fullname
    classData = {}
    classFound = False
    for class_ in classesData:
        if id == class_["classid"]:
            response["data"] = class_
            response["message"] = "Get Class Success"
            classFound = True
            break
    if classFound:
        classData["students"] = []
    # mengambil fullname untuk menggantikan userId yang di tampilkan students
    for user in userData:
        if id in user["classes_as_student"]:
            class_["students"].append(user["fullName"])
    return jsonify(response)

@app.route('/classes', methods=["GET"])
def getAllClasses():
    
    # siapin file buat di read
    classesData = readFile(classFileLocation)

    return jsonify(classesData)

@app.route('/joinClass', methods=["POST"])
def joinClass():
    body = request.json
 
    response = {}
    response["message"] = "JOIN CLASS SUKSES"
    response["data"] = {} 

    # nambahin userid ke classes-file
    classesData = readFile(classFileLocation)
    usersData = readFile(userFileLocation)

    AlreadyExist = False
    for class_ in classesData:
        if body["classid"] == class_["classid"]:
            if body["userId"] in class_["students"]:
                response["message"] = "Class ID {} is already exist".format(body["classid"])
                AlreadyExist = True
                break
    for user in usersData:
        if body["userId"] == user["userId"]:
            if body["classid"] in user["classes_as_student"]:
                response["message"] = "user ID {} is already exist".format(body["userId"])
                AlreadyExist = True
    if not AlreadyExist:
        response["data"] = body
        class_["students"].append(body["userId"])
        user["classes_as_student"].append(body["classid"])
        writeFile(classFileLocation, classesData)
        writeFile(userFileLocation, usersData)

    return jsonify(response)

@app.route('/updateUser/<int:id>', methods=["PUT"])
def updateUser(id):
    userData = getAllUsers().json
    body = request.json
    response = {}
    response["message"] = "GAGAL UPDATE"
    response["data"] = {}

    for user in userData:
        if id == user["userId"]:
            user["username"] = body["username"]
            user["fullName"] = body["fullName"]
            user["password"] = encryp(body["password"])
            user["email"] = body["email"]
            response["message"]="update dengan ID {} berhasil".format(id)
            response["data"] = user
    writeFile(userFileLocation, userData)
    return jsonify(response)

@app.route('/updateClass/<int:id>', methods=["PUT"])
def updateClass(id):
    class_Data = getAllClasses().json
    body = request.json

    response = {}
    response["message"] = "GAGAL UPDATE"
    response["data"] = {}

    for class_ in class_Data:
        if id == class_["classid"]:
            class_["classname"] = body["classname"]
            response["message"]="update dengan Class ID {} berhasil".format(id)
            response["data"] = class_
    writeFile(classFileLocation, class_Data)
    return jsonify(response)

@app.route('/classwork', methods=["POST"])
def creatClassWork():
    workData = []

    # kalau file users-file.json udah ada, di read dulu. kalau file ga ada, ga usah di read, langsung write
    workData = readFile(classworkFileLocation)
  

    body = request.json
    for work in workData:
        if body["classworkid"] == work["classworkid"]:
            return "ID ANDA MASUKAN SUDAH ADA GAN"
   
    body["answers"]=[]
    workData.append(body)
    
    # siapin file buat di write
    writeFile(classworkFileLocation, workData)

            
  # menambahkan classworkid di classwork yang ada di database classes-file
    classesData = readFile(classFileLocation)
    for class_ in classesData:
        if body["class"] == class_["classid"]:
            if body["classworkid"] not in class_["classwork"]:
                class_["classwork"].append(body["classworkid"])           
    writeFile(classFileLocation, classesData)

    return jsonify(workData)

@app.route('/classwork/<int:id>', methods=["GET"])
def getclasswork(id):
    # siapin file buat di read
    userData = readFile(userFileLocation)

    for work in userData:
        if id == work["classworkid"]:
            return jsonify(work)

    return "User ID {} is not found".format(id)

@app.route('/classworks', methods=["GET"])
def getAllClasswork():
    # siapin file buat di read
    workData = readFile(classworkFileLocation)

    return jsonify(workData)

@app.route('/assignclasswork/<int:id>', methods=["POST"])
def assignClassWork(id):
    body = request.json
 
    # nambahin userid ke classes-file
    workData = readFile(classworkFileLocation)

    for work in workData:
        if id == work["classworkid"]:
            work["answers"].append(body)
    
    writeFile(classworkFileLocation, workData)

    return "TUGAS ANDA TELAH BERHASIL DIKIRIM"

@app.route('/updateclasswork/<int:id>', methods=["PUT"])
def updateclasswork(id):
    workData = getAllClasswork().json
    body = request.json

    for work in workData:
        if id == work["classworkid"]:
            work["question"] = body["question"]
            
    writeFile(classworkFileLocation, workData)
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

    writeFile(userFileLocation, userData)

    writeFile(classFileLocation, class_Data)

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

                
    writeFile(classworkFileLocation, workData)

    writeFile(classFileLocation, class_Data)

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
            break
    for user in userData:
        if id in user["classes_as_student"]:
            user["classes_as_student"].remove(id)
    for user in userData:
        if id in user["classes_as_teacher"]:
            user["classes_as_teacher"].remove(id)

    writeFile(classFileLocation, class_Data)
    writeFile(classworkFileLocation, workData)
    writeFile(userFileLocation, userData)
            

    return "CLASS ANDA BERHASIL DI HAPUS"

    # return "User ID {} is not found".format(id)