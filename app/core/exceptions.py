from fastapi import HTTPException

raise HTTPException(
    status_code=404,
    detail="Customer not found"
)