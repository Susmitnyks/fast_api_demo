from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc

from get_demo import app

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
