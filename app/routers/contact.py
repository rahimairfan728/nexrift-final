from fastapi import APIRouter, status, HTTPException
from app import schemas
from typing import List
import os
from datetime import datetime

router = APIRouter(prefix="/api/contact", tags=["contact"])

# In-memory storage for contacts (will reset when server restarts)
contacts_storage = []

@router.post("/", response_model=schemas.ContactBase, status_code=status.HTTP_201_CREATED)
def submit_contact(form: schemas.ContactCreate):
    try:
        # Add timestamp to the contact
        contact_data = {
            'name': form.name,
            'email': form.email,
            'message': form.message,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in memory
        contacts_storage.append(contact_data)
        
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