from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime


#maintenanceticket

class MaintenanceTicketCreate(BaseModel):
    tenant_id:int=Field(...,gt=0,description="tenant id")
    apartment_id:int=Field(...,gt=0,description="apartment id")
    complaint_category:str= Field(...,description="maintenance complainat category")
    description:str=Field(...,min_length=5,description="description of the maintenance problem")
    priority:str=Field(...,description="ticket priority")

class MaintenanceTicketUpdate(BaseModel):
    complaint_category:Optional[str]=Field(default=None,description=" maintenance complaint problem")
    description:Optional[str]=Field(default=None,min_length=5,description="description of the maintenance problem") 
    priority:Optional[str]=Field(default=None,description="ticket priority")
    status:Optional[str]=Field(default=None,description="ticket status")

class MaintenanceTicketResponse(BaseModel):
    ticket_id:int
    tenant_id:int
    apartment_id:int
    complaint_category:str
    description:str
    priority:str
    status:str
    created_timestamp:datetime
    assigned_technician:Optional[int]=None
    resolution_timestamp:Optional[datetime]=None

 #technician

class TechnicianCreate(BaseModel):
    name:str=Field(...,min_length=2,max_length=100,description="technician name")
    specialization:str=Field(...,description="technician specialization")
    availability_status:str=Field(...,description="techinican availability status")
    contact_reference:str=Field(...,description="technician contact refernece")

class TechnicianUpdate(BaseModel):
    name:Optional[str]=Field(default=None,min_length=2,max_length=100,description="technician name")
    specialization:Optional[str] = Field(default=None,description="technician specialization")
    availability_status:Optional[str]=Field(default=None,description="Technician availabiltiy status")
    contact_reference:Optional[str]=Field(default=None,description="technician contact reference")


class TechnicianResponse(BaseModel):
    technician_id:int
    name:str
    specialization:str
    availability_status:str
    contact_reference:str

#maintenance assignment

class AssignmentCreate(BaseModel):
    ticket_id:int=Field(...,gt=0,description="maintenance ticket id")
    technician_id:int=Field(...,gt=0,description="techician id")

class AssignmentResponse(BaseModel):
    assignment_id:int
    ticket_id:int
    technician_id:int
    assigned_at:datetime
    unassigned_at:Optional[datetime]=None
    status:str


 #Maintenance actions

class AssignTechicianRequest(BaseModel):
    technician_id:int=Field(...,gt=0,description="techinican id to assign")

class ResolveTicketRequest(BaseModel):
    resolution_note:str=Field(...,min=5,description="note explaining how the issue was resolved")


#SLA POLICY

class SLAPolicyCreate(BaseModel):
    priority:str=Field(...,description="ticket priority")
    response_target:int=Field(...,gt=0,description="target resposne time")
    resolution_target:int=Field(...,gt=0,description="target resolution time")

class SLAPolicyUpdate(BaseModel):
    response_target: Optional[int]=Field(default=None,gt=0,description="target response time")
    resolution_target:Optional[int]=Field(default=None,gt=0,description="target resolution time")

class SLAPolicyResponse(BaseModel):
    sla_id:int
    priority:str
    response_target:int
    resolution_target:int          
