from pydantic import Field,BaseModel,EmailStr
from typing import Optional
from datetime import date,datetime


#auth
class LoginRequest(BaseModel):
    email:EmailStr = Field(...,description="Email of user")
    password:str = Field(...,min_length = 6,max_length=20,description="user password")

class TokenResponse(BaseModel):
    access_token:str = Field(...,description ="JWT access token")
    token_type:str =Field(default="bearer",description="authentication token type") 

#role
class RoleBase(BaseModel):
    role_name:str = Field(...,min_length=2,max_length=50,description="user role")
    description:Optional[str]=Field(default=None,description="role description")

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    role_name:Optional[str]=Field(default=None,min_length=3,max_length=100,description="update role name")
    description:Optional[str]=Field(default=None,description="updated role description")
 
class RoleResponse(RoleBase):
    role_id:int=Field(...,description="unique role identity")    


#user
class UserCreate(BaseModel):
    full_name: str = Field(...,min_lengt=2,max_length=100,description="user name")
    email:EmailStr=Field(...,description="user email")
    password:str=Field(...,min_length=6,description="user password")
    role_id:int=Field(...,gt=0,description="user role id")


class UserUpdate(BaseModel):
    full_name:Optional[str] = Field(default=None,min_length=3,max_length=100,description="full name of user")
    email:Optional[EmailStr] = Field(default=None,description="email of user")
    role_id:Optional[int]=Field(default=None,gt=0,description="role id of user")
    status:Optional[str] = Field(default=None,description="user status")

class UserResponse(BaseModel):
    user_id:int
    full_name:str
    email:EmailStr
    role_id: int
    status:str
    created_at: datetime


#property
class PropertyCreate(BaseModel):
    property_name:str=Field(..., min_length=2,max_length=100,description="property name")
    address_reference:str=Field(...,descrption="Address reference")
    owner_reference:str=Field(...,description="owner reference")
    number_of_apartments:int=Field(...,gt=0,description="number of apartments")
    status:str=Field(...,description="property status")

class PropertyUpdate(BaseModel):
    property_name:Optional[str]=Field(default=None,min_length=2,max_length=591 ,description="property name")
    address_reference:Optional[str]=Field(default=None,description="address reference")
    owner_refernce:Optional[str]=Field(default = None,description="owner reference")
    number_of_apartments:Optional[int]=Field(default=None,gt=0,description="number of apartments")
    status:Optional[str] = Field(default = None,description="property status")

class PropertyResponse(BaseModel):
    property_id:int
    property_name:str
    address_refernce:str
    owner_reference:str   
    number_of_apartments:int
    status:str



#apartment
class ApartmentCreate(BaseModel):
    property_id:int=Field(...,gt=0,description="property id")
    apartment_number:str = Field(...,description="apartment number")
    floor_number:int=Field(...,ge=0,description="floor number")
    apartment_type:str = Field(...,description="apartment type")
    monthly_rent:int=Field(...,gt=0,description="monthly rent")
    status:str =Field(...,description="apartment status")

class ApartmentUpdate(BaseModel):
    apartment_number:Optional[str]=Field(default= None,description="apartment number")
    floor_number:Optional[int]=Field(default=None,ge=0,description="floor number")
    apartment_type:Optional[str]=Field(default=None,description="apartment type")
    monthly_rent:Optional[decimal]=Field(default=None,gt=0,description="monthly rent")
    status:Optional[str] = Field(default=None,description="apartment status")

class ApartmentResponse(BaseModel):
    apartment_id:int
    property_id:int
    apartment_number:str
    floor_number:str
    apartment_type:str
    monthly_rent:int
    status:str

#Tenant
class TenantCreate(BaseModel):
    full_name:str =Field(...,min_length=2,max_length=100,description="tenant full name")
    email:EmailStr=Field(...,description="email address of tenant")
    phone_reference:str=Field(..,description="tenant phone refernece")
    identity_reference:str=Field(...,default=None,description="tenant identity reference")
    status:optional[str]=Field(default=None,description="status of tenant")

class TenantUpdate(BaseModel):
    full_name:optional[str]=Field(default=None,min_length=2,max_length=100,description="full name of tenant")
    email:Optional[EmailStr]=Field(default=None,description="email of tenant")
    phone_reference:Optional[str]=Field(default=None,description="phone number of tenant")
    identity_reference:Optional[str]=Field(default=None,description="identity of tenant")
    status:Optional[str]=Field((default=None,description="tenant status"))

class TenantResponse(BaseModel):
    tenant_id:int
    full_name:str
    email:EmailStr
    phone_reference:str
    identity_reference:str
    registration_date:date
    status:str


#Rental agreement
class RentalAgreementCreate(BaseModel):
    tenant_id:int=Field(...,gt=0,description="tenant id")
    apartment_id:int=Field(...,gt=0,description="apartment id")
    start_date:date=Field(...,description="Agreement start date")
    end_date:date=Field(...,description="monthly rent")
    security_deposit:decimal=Field(...,ge=0,description="security deposit")
    status:str=Field(...,description="agreement status")

class RentalAgreementUpdate(BaseModel):
    end_date:Optional[date]=Field(default=None,description="agreement end date")
    monthly_Rent:Optional[Decimal]=Field(default=None,gt=0,description="monthly rent")
    security_deposit:Optional[Decimal]=Field(Default=None,ge=0,description="security deposit")  
    status:Optional[str]=Field(default=None,description="agreement status")

class RentalResponse(BaseModel):
    agreement_id:int
    tenant_id:int
    apartment:int
    start_date:date
    end_date:date
    monthly_rent:Decimal
    security_deposit:Decimal
    status:str

#Rent Obligation
class RentObligationCreate(BaseModel):
    agreement_id:int=Field(...,gt=0,description="rental agreement id")
    billing_month:date=Field(...,description="billing month")
    due_date:date=Field(...,description="rent due date")
    amount_due:Decimal=Field(...,gt=0,description="amount due")
    amount_paid:Decimal=Field(default=Decimal("0"),ge=0,description="amount already paid")
    status:str=Field(...,description="rent obiligation status")

class RentObligationUpdate(BaseModel):
    due_date:Optional[date]=Field(default=None,description="rent due date")
    amount_paid:Optional[decimal]=Field(default=None,ge=0,description="amount paid")
    status:Optional[str]=Field(Default=None,description="rent obligation status")

class RentObligationResponse(BaseModel):
    rent_id:int
    agreement_id:int
    billing_month:date
    due_date:date
    amount_due:Decimal
    amount_paid:Decimal
    status:str 


#payment
class PaymentCreate(BaseModel):
    rent_id:int=Field(...,gt=0,description="rent obligation id")
    amount:Decimal=Field(...,gt=0,description="payment amount") 
    payment_date:date=Field(...,description="payment date")
    payment_method:str=Field(...,description="payment method")  
    reference_number:str=Field(...,description="payment reference number")
    status:str=Field(...,desccription="payment status")


 class PaymentUpdate(BaseModel):
    payment_method:Optional[str]=Field(default=None,description="payment mehtod" )
    status:Optional[str]=Field(default=None,description="payment status")     

class PaymentResponse(BaseModel):
    payment_id:int
    rent_id:str
    amount:Decimal
    payment_date:date
    payment_method:str
    refernce_number:str
    status:str
        
