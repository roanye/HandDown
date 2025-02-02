from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import random
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# Gmail SMTP settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "handdown.downhand@gmail.com"
SMTP_PASSWORD = "iuvx dxjl jyax ywca"

class EmailRequest(BaseModel):
    email: EmailStr

def generate_code() -> str:
    return str(random.randint(100000, 999999))

def send_email(email: str, code: str):
    subject = "Your Verification Code"
    body = f"Your verification code is: {code}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = email
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

@app.post("/send-code/")
def send_verification_code(request: EmailRequest):
    email = request.email.lower()
    if not email.endswith("@tufts.edu"):
        raise HTTPException(status_code=400, detail="Invalid email domain. Only 'tufts.edu' is allowed.")
    
    code = generate_code()
    send_email(email, code)
    return {"message": "Verification code sent successfully."}
