from fastapi import APIRouter, status, HTTPException
from app import schemas
from typing import List
import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

router = APIRouter(prefix="/api/contact", tags=["contact"])

# In-memory storage for contacts (will reset when server restarts)
contacts_storage = []

# Excel file path for local development
EXCEL_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'contacts_new.xlsx')
HEADERS = ['Name', 'Email', 'Message', 'Timestamp']

def save_to_excel(name: str, email: str, message: str, timestamp: str):
    """Save contact to Excel file (for local development)"""
    try:
        # Create file if it doesn't exist
        if not os.path.exists(EXCEL_FILE):
            wb = Workbook()
            ws = wb.active
            ws.append(HEADERS)
        else:
            wb = load_workbook(EXCEL_FILE)
            ws = wb.active
        
        # Add new contact
        ws.append([name, email, message, timestamp])
        wb.save(EXCEL_FILE)
        print(f"Contact saved to Excel: {name}, {email}")
    except Exception as e:
        print(f"Excel save error (non-critical): {str(e)}")
        # Don't fail the request if Excel save fails

@router.post("/", response_model=schemas.ContactBase, status_code=status.HTTP_201_CREATED)
def submit_contact(form: schemas.ContactCreate):
    try:
        # Add timestamp to the contact
        timestamp = datetime.now().isoformat()
        contact_data = {
            'name': form.name,
            'email': form.email,
            'message': form.message,
            'timestamp': timestamp
        }
        
        # Store in memory (works everywhere)
        contacts_storage.append(contact_data)
        
        # Try to save to Excel file (works only in local development)
        save_to_excel(form.name, form.email, form.message, timestamp)
        
        print(f"Contact saved successfully: {form.name}, {form.email}")
        print(f"Total contacts stored: {len(contacts_storage)}")
        
        return form
    except Exception as e:
        print(f"Error saving contact: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving contact: {str(e)}"
        )

@router.get("/", response_model=List[schemas.ContactBase])
def list_contacts():
    try:
        # Return all stored contacts
        return contacts_storage
    except Exception as e:
        print(f"Error reading contacts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading contacts: {str(e)}"
        )

@router.get("/count")
def get_contact_count():
    """Get the total number of contacts stored"""
    return {"count": len(contacts_storage)} 