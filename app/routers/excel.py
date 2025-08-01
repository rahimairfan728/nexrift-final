from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from typing import List, Dict

router = APIRouter()

EXCEL_FILE = os.path.join(os.path.dirname(__file__), '../../data.xlsx')

@router.get('/excel-data')
def read_excel_data():
    try:
        if not os.path.exists(EXCEL_FILE):
            # Return empty data if file doesn't exist
            return []
        df = pd.read_excel(EXCEL_FILE)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading Excel data: {str(e)}")
        # Return empty data on error
        return []

@router.post('/excel-data')
def write_excel_data(data: List[Dict]):
    try:
        df = pd.DataFrame(data)
        df.to_excel(EXCEL_FILE, index=False)
        return {'status': 'success'}
    except Exception as e:
        print(f"Error writing Excel data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to write Excel file: {str(e)}"
        ) 