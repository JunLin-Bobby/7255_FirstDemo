from pydantic import BaseModel, StrictFloat, StrictInt
from typing import List

class PlanCostShares(BaseModel):
    deductible: StrictFloat
    _org: str
    copay: StrictFloat
    objectId: str
    objectType: str

class LinkedService(BaseModel):
    _org: str
    objectId: str
    objectType: str
    name: str

class PlanServiceCostShares(BaseModel):
    deductible: StrictFloat
    _org: str
    copay: StrictFloat
    objectId: str
    objectType: str

class LinkedPlanServices(BaseModel):
    linkedService: LinkedService
    planserviceCostShares: PlanServiceCostShares
    _org: str
    objectId: str
    objectType: str

class PlanSchema(BaseModel):
    planCostShares: PlanCostShares
    linkedPlanServices: List[LinkedPlanServices]
    _org: str
    objectId: str
    objectType: str
    planType: str
    creationDate: str