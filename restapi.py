from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc
import httpx

app = FastAPI()

# Database connection details
server = '192.168.1.249'
database = 'PXMAIN'
username = 'sa'
password = 'PAXDB@dm1n'
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

class PatientData(BaseModel):
    patient_id: str
    name: str
    diagnosis: str

@app.get("/patient/{patient_id}")
async def get_patient_data(patient_id: int):
    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT pat_id, pat_name, pat_sex FROM Patients WHERE pat_id = ?", patient_id)
            row = cursor.fetchone()
            if row:
                patient_data = PatientData(patient_id=row[0], name=row[1] , diagnosis=row[2])
                return patient_data
            else:
                raise HTTPException(status_code=404, detail="Patient not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send_patient_data/")
async def send_patient_data(patient_data: PatientData):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1/api/receive_patient_data", json=patient_data.dict())
            response.raise_for_status()
            return {"status": "success", "response": response.json()}
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the FastAPI application, use the following command:
# uvicorn restapi:app --host 0.0.0.0 --port 8000