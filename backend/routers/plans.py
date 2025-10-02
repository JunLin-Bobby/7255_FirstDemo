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
    return {
        "message": "Plan created successfully",
        "id": str(result.inserted_id),  # return _id generated from MongoDB 
        "objectId": payload.get("objectId")  # return ObjectId
    }


@router.get("/plans/{object_id}", status_code=status.HTTP_200_OK)
async def get_plan_by_object_id(object_id: str, if_none_match: str = Header(None)):
    
    """Retrieve a plan by objectId with conditional read."""
    db = get_database()
    print("before find_one")
    plan = await db.plans.find_one({"objectId": object_id})
    print("after find_one")
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    # Convert ObjectId to string for JSON serialization
    if "_id" in plan:
        plan["_id"] = str(plan["_id"])

    # Generate ETag based on the plan's content
    plan_etag = sha256(str(plan).encode()).hexdigest()
    # Check If-None-Match header
    if if_none_match == plan_etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers={"Content-Length": "0"})

    # Return the plan with ETag header
    response = JSONResponse(content=plan, status_code=status.HTTP_200_OK)
    response.headers["ETag"] = plan_etag
    
    return response

@router.delete("/plans/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan_by_object_id(object_id: str):
    """Delete a plan by object id."""
    db = get_database()
    result = await db.plans.delete_one({"objectId": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)