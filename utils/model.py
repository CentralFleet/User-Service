from pydantic import BaseModel, Field
from typing import Optional

class Company(BaseModel):
    Account_Name: Optional[str] = None
    Dealer_License_Number: Optional[str] = None
    Dealer_Phone: Optional[str] = None
    Category: Optional[str] = None
    Website: Optional[str] = None
    Address: Optional[str] = None
    ExpiryDate: Optional[str] = None
    Business_Number: Optional[str] = None
    CRA_HST_GST_Number: Optional[str] = None
    SK_PST_Number: Optional[str] = None
    Email: Optional[str] = None
    BC_PST_Number: Optional[str] = None
    Central_Fleet_User: Optional[bool] = True



class Carrier(BaseModel):
    Name: Optional[str] = None
    OperatingRegions: Optional[str] = None
    CarrierType	: Optional[list] = None
    Phone_Number : Optional[str] = None
    Email : Optional[str] = None
    Address : Optional[str] = None
    Website	: Optional[str] = None
    Central_Fleet_User : Optional[bool] = True



class Contact(BaseModel):
    Dealership : Optional[str] = None 
    Carrier_ID : Optional[str] = None
    Last_Name : Optional[str] = None 
    Email : Optional[str] = None 
    Phone :Optional[str] = None 
    Title : Optional[str] = None 
    Note : Optional[str] = None
    Vendor_ID : Optional[str] = None


class Vendor(BaseModel):
    Vendor_Name: Optional[str] = None
    OperatingRegions: Optional[str] = None
    Carrier_Type	: Optional[list] = None
    Phone : Optional[str] = None
    Email : Optional[str] = None
    Address : Optional[str] = None
    Website	: Optional[str] = None
