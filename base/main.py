from fastapi import FastAPI, HTTPException, Path
import json

app = FastAPI()

''' 
HTTP Methods:
GET --> to just display the message on any website.
'''
@app.get('/')
def greet():
    return {"message": "welcome the developer life"}

@app.get('/about')
def about():
    return {"message": "about page"}

def load_data():
    with open("/home/rishabh/Documents/FastApi/base/students_50.json", "r") as file:
        return json.load(file)

@app.get('/students')
def get_students():
    return load_data()


# this is the path parameter
@app.get('/students/{student_id}')
def get_id(student_id: int = Path(..., description="The ID of the student to get", example=1)):
    data = load_data()
    for student in data:
        if student['id'] == student_id:
            return student
    raise HTTPException(status_code=404, detail=f"Student with Id '{student_id}' not found")