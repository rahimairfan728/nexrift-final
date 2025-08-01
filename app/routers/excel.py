from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from typing import List, Dict

router = APIRouter()

EXCEL_FILE = os.path.join(os.path.dirname(__file__), '../../data.xlsx')

@router.get('/excel-data')
def read_excel_data():
    if not os.path.exists(EXCEL_FILE):
        raise HTTPException(status_code=404, detail='Excel file not found')
    df = pd.read_excel(EXCEL_FILE)
    return df.to_dict(orient='records')

@router.post('/excel-data')
def write_excel_data(data: List[Dict]):
    df = pd.DataFrame(data)
    df.to_excel(EXCEL_FILE, index=False)
    return {'status': 'success'} 