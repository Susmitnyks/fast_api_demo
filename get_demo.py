import json
import mysql
import pyodbc
from starlette.responses import JSONResponse, HTMLResponse
from typing import Dict, Any
import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# uvicorn get_demo:app --reload
# http://127.0.0.1:8000/docs
app = FastAPI()
my_dict = {}
# Azure SQL Database Details
SERVER = "apapsqlserverdev.database.windows.net"
DATABASE = "apapsqldbdev"
USERNAME = "susmit.surwade@blenheimchalcot.com"  # Your Azure AD account
PASSWORD = "SusRoop@123"  # Your Azure AD password (not recommended for MFA accounts)

# Connection String with Username and Password
conn_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"Authentication=ActiveDirectoryPassword;"
)


# Request model for POST API
class EmailRequest(BaseModel):
    email_id: str


@app.post("/user/postdata")
def post_demo(user_age: int, user_name: str):
    if user_age == 500 and user_name == "amit":
        raise HTTPException(status_code=500, detail="Invalid input: user_age=100 and user_name=amit")
    if user_age == 401 and user_name == "amit":
        raise HTTPException(status_code=401, detail="Invalid input: user_age=100 and user_name=amit")
    if user_age == 400 and user_name == "amit":
        raise HTTPException(status_code=400, detail="Invalid input: user_age=100 and user_name=amit")
    if user_age == 402 and user_name == "amit":
        raise HTTPException(status_code=402, detail="Invalid input: user_age=100 and user_name=amit")
    if user_age == 403 and user_name == "amit":
        raise HTTPException(status_code=403, detail="Invalid input: user_age=100 and user_name=amit")
    if user_age == 404 and user_name == "amit":
        raise HTTPException(status_code=404, detail="Invalid input: user_age=100 and user_name=amit")
    if user_age == 429 and user_name == "amit":
        raise HTTPException(status_code=429, detail="Invalid input: user_age=100 and user_name=amit")

    global my_dict
    my_dict[user_age] = user_name
    return {"message": "User added successfully"}


@app.get("/user/getdict")
def get_dict():
    return my_dict


@app.get("/user/return")
def name():
    return {'name': 3}


@app.get("/user/condition")
def condition(user_age: int):
    if user_age > 18:
        return "allowed"
    else:
        return "not allowed"


@app.get("/login")
def login():
    with open("json_response.json", "r") as file:
        response = json.load(file)
    return JSONResponse(content=response, status_code=200)


@app.post("/user/postdata/body")
def post_demo(user_input: Dict[str, Any]):
    user_age = user_input.get("user_age")
    user_name = user_input.get("user_name")

    if user_age == 500 and user_name == "amit":
        raise HTTPException(status_code=500, detail="Invalid input: user_age=500 and user_name=amit")
    if user_age == 401 and user_name == "amit":
        raise HTTPException(status_code=401, detail="Invalid input: user_age=401 and user_name=amit")
    if user_age == 400 and user_name == "amit":
        raise HTTPException(status_code=400, detail="Invalid input: user_age=400 and user_name=amit")
    if user_age == 402 and user_name == "amit":
        raise HTTPException(status_code=402, detail="Invalid input: user_age=402 and user_name=amit")
    if user_age == 403 and user_name == "amit":
        raise HTTPException(status_code=403, detail="Invalid input: user_age=403 and user_name=amit")
    if user_age == 404 and user_name == "amit":
        raise HTTPException(status_code=404, detail="Invalid input: user_age=404 and user_name=amit")
    if user_age == 429 and user_name == "amit":
        raise HTTPException(status_code=429, detail="Invalid input: user_age=429 and user_name=amit")

    # Store the data in the in-memory dictionary
    my_dict[user_age] = user_name
    return {"message": "User added successfully"}


# Database connection details
DB_HOST = "sql12.freesqldatabase.com"
DB_NAME = "sql12754075"
DB_USER = "sql12754075"
DB_PASS = "beyecNZkCz"


# Pydantic model to describe the input structure
class UserName(BaseModel):
    Name: str


# Function to get the salary from the database
def get_salary_from_db(name: str):
    global cursor
    connection = None  # Initialize connection to None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = connection.cursor()

        # SQL query to get the salary
        cursor.execute("SELECT Salary FROM Employee WHERE FirstName = %s", (name,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None
    finally:
        # Ensure that connection is closed only if it's initialized and open
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# API endpoint to get the salary
@app.post("/user/getsalary")
async def get_salary(user: UserName):
    name = user.Name
    salary = get_salary_from_db(name)

    if salary is not None:
        return {"salary": salary}
    else:
        raise HTTPException(status_code=404, detail="User not found")


# Pydantic model to describe the input structure
class UserSalaryUpdate(BaseModel):
    Name: str
    Salary: int  # Salary field to update


# Function to update the salary in the database
def update_salary_in_db(name: str, salary: int):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = connection.cursor()

        # SQL query to update the salary
        update_query = "UPDATE Employee SET Salary = %s WHERE FirstName = %s"
        cursor.execute(update_query, (salary, name))
        connection.commit()  # Commit the changes to the database

        return cursor.rowcount  # Returns the number of rows affected
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# API endpoint to update the salary
@app.post("/user/updatesalary")
async def update_salary(name: str, user_salary: int):  # update here for html page
    # async def update_salary(name: str = Form(...), user_salary: int = Form(...)):
    rows_affected = update_salary_in_db(name, user_salary)
    # async def update_salary(user: UserSalaryUpdate):
    #     name = user.Name
    #     new_salary = user.Salary
    #    rows_affected = update_salary_in_db(name, new_salary)

    if rows_affected > 0:
        return {"message": f"Salary updated successfully for {name}"}
    else:
        raise HTTPException(status_code=404, detail=f"User '{name}' not found or salary not updated")


# Serve HTML form
@app.get("/html", response_class=HTMLResponse)
async def read_form():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Update Salary</title>
    </head>
    <body>
        <h2>Update Salary</h2>
        <form action="/user/updatesalary" method="post">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name" required><br><br>
            <label for="salary">Salary:</label><br>
            <input type="number" id="salary" name="user_salary" required><br><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
@app.post("/user/postdata/otp")
def get_otp(data: EmailRequest):
    query = f"""
        SELECT TOP 1 [otp]
        FROM [dbo].[EmailTokenMapping]
        WHERE email_id='{data.email_id}'
        ORDER BY created_at DESC
        """

    try:
        # Connect to the database
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(query)

        # Fetch OTP
        row = cursor.fetchone()
        conn.close()

        if row:
            otp = row[0]  # Assuming OTP is in the first column
            return {"email_id": data.email_id, "otp": otp}
        else:
            raise HTTPException(status_code=404, detail="OTP not found for the given email ID")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
