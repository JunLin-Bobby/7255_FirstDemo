from fastapi import APIRouter, HTTPException, Request, status, Header, FastAPI
from fastapi.responses import JSONResponse, Response
from backend.db.connection import get_database
from hashlib import sha256
from bson import ObjectId
from backend.schema.plan_schema import PlanSchema
from pydantic import ValidationError

router = APIRouter()


@router.post("/plans", status_code=status.HTTP_201_CREATED)
async def create_plan(plan: PlanSchema):
    db = get_database()
    payload = plan.dict()
    result = await db.plans.insert_one(payload)
    
    # Retrieve the newly created data to generate the ETag
    created_plan = await db.plans.find_one({"_id": result.inserted_id})
    created_plan["_id"] = str(created_plan["_id"])  # Convert to string
    
    # Generate ETag
    plan_etag = sha256(str(created_plan).encode()).hexdigest()
    
    # Store the ETag in the database
    await db.plans.update_one(
        {"_id": result.inserted_id},
        {"$set": {"etag": plan_etag}}
    )
    
    # Create the response and set the ETag header
    response = JSONResponse(
        content={
            "message": "Plan created successfully",
            "id": str(result.inserted_id),
            "objectId": payload.get("objectId")
        },
        status_code=status.HTTP_201_CREATED
    )
    response.headers["ETag"] = plan_etag
    return response


@router.get("/plans/{object_id}", status_code=status.HTTP_200_OK)
async def get_plan_by_object_id(object_id: str, if_none_match: str = Header(None)):
    
    """Retrieve a plan by objectId with conditional read."""
    db = get_database()
    plan = await db.plans.find_one({"objectId": object_id})
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    # Convert ObjectId to string for JSON serialization
    if "_id" in plan:
        plan["_id"] = str(plan["_id"])

    # Retrieve the stored ETag
    stored_etag = plan.get("etag")
    
    # Check If-None-Match header
    if if_none_match and if_none_match == stored_etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers={"Content-Length": "0"})

    # Remove the etag field, do not return it to the client
    if "etag" in plan:
        del plan["etag"]

    # Return the plan with ETag header
    response = JSONResponse(content=plan, status_code=status.HTTP_200_OK)
    if stored_etag:
        response.headers["ETag"] = stored_etag
    
    return response

@router.delete("/plans/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan_by_object_id(object_id: str):
    """Delete a plan by object id."""
    db = get_database()
    result = await db.plans.delete_one({"objectId": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)