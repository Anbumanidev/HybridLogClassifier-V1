from fastapi import FastAPI,File, UploadFile
from pydantic import BaseModel

from src.classifier import classifier, classifier_csv

app = FastAPI()

class LogEntry(BaseModel):
    source: str = None
    log_message: str

@app.post("/predict")
async def predict_log(source: str, log_message: str):
    label = classifier(source, log_message)
    return {"source": source, "log_message": log_message, "label": label}

@app.post("/predict_csv")
async def predict_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return {"error": "Only CSV files are supported."}
    
    contents = await file.read()
    with open("temp.csv", "wb") as f:
        f.write(contents)
    
    return classifier_csv("temp.csv")
