# **WELCOM TO MY GOOGLE CLASSROOM PROGRAM by PRAM**

### Aplikasi my Google Classroom ini menggunakan bahasa pemrograman python, agar pengguna mudah untuk membacanya dan di dalam python juga menggunakan Flask sebagai framework, JSON sebagai format penulisan datanya dan Insomnia sebagai REST API dari sisi kliennya.

# HOW TO INSTALL IN WINDOWS 10
## Python
### install PIP di pyhton
`pip install`
### jika PIP meminta untuk di update maka masukan
`python -m pip install --upgrade pip`
## FLASK
### install flask di pyhton dengan PIP
`pip install flask`
## INSOMNIA
### install insomnia mudah tinggal download filenya [disini]( https://insomnia.rest/). jika sudah di download tinggal install sesuai langkah.
# PENGGUNAAN APLIKASI
## register User (daftar murid)
### buka Insomnia, buat request POST dengan dengan body JSON dan masukan url `/register` . dan masukan contoh input:
```
{
        "userId": 2,
        "username": "guru2",
        "fullName": "lambe2",
        "password": "abc",
        "email": "lambet2@gmail.com"
}
```
### Maka hasil outputnya akan seperti ini:
```
{
  "message": "Creat class SUKSES",
  "data": {
    "userId": 2,
    "username": "guru2",
    "fullName": "lambe2",
    "password": "def",
    "email": "lambet2@gmail.com",
    "classes_as_student": [],
    "classes_as_teacher": []
  }
}
```
## Creat class (membuat kelas)
### buka Insomnia, buat request POST dengan dengan body JSON dan masukan url `/class` . dan masukan contoh input:
```
{
	"classname":"algo",
	"classid":1,
	"teachers":1
}
```
### Maka hasil outputnya akan seperti ini:
```
{
  "message": "Creat class SUKSES",
  "data": {
    "classname": "algo",
    "classid": 1,
    "teachers": 1,
    "students": [],
    "classwork": []
  }
}
```
## Creat classwork (membuat tugas/PR)
### buka Insomnia, buat request POST dengan dengan body JSON dan masukan url `/classwork` . dan masukan contoh input:
```
{
	"classworkid":1,
	"class":2,
	"question":"backand"
}
```
### Maka hasil outputnya akan seperti ini:
```
[
  {
    "classworkid": 1,
    "class": 2,
    "question": "backand",
    "answers": []
  }
]
```

# FITUR DALAM MY GOOGLE CLASSROOM by PRAM
- [x] Register
- [x] Login
- [x] Create class
- [x] Get class
- [x] Get All class
- [x] Join class
- [x] Update class
- [x] Delete class
- [x] Create classwork
- [x] Get classwork
- [x] Asign classwork
- [x] Update classwork
- [x] Delete classwork