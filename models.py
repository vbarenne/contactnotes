from enum import Enum
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class CommunicationChannel(str, Enum):
    PhoneCall = "Phone Call"
    Email = "Email"
    InPerson = "In Person"
    Message = "Message"
    Other = "Other"
    
class ContactType(str, Enum):
     AccountClosure = "Account Closure"
     AccountOpening = "Account Opening"
     BankDocuments = "Bank Documents"
     BusinessTravel = "Business Travel"
     CipReview = "Client Investment Profile (CIP) Review"
     Complaint = "Complaint"
     MarginCall = "Deliberating Margin Call Situation and Solution"
     CreditFacility = "Establishing Credit Facility"
     ClientProfileReview = "KYC Discussion/Review of Client Profile"
     PortfolioReview = "Portfolio Review/Negative Performance Review"
     InvestmentRecommendation = "Recommendation of Investment Products"
     Other = "Other"



class UploadMethod(str, Enum):
    Joice = "Joice"
    Manual = "Manual"
    Clm = "CLM"

class ContactNote(BaseModel):
    date_of_contact: Optional[datetime] = Field(
        None, description='Date of the contact', example='30.01.2023'
    )
    communication_channel: Optional[CommunicationChannel| str] = Field(
        None, description='Communication Channel', example='Phone Call'
    )
    contact_types: Optional[List[ContactType]] = Field(
        None, description='Contact Type amongst list provided by compliance', example='Account Closure'
    )
    attendees: Optional[List[str]] = None
    note_content: Optional[str] = None

    def to_dict(self) -> dict:
        note_dict = {"date_of_contact": self.date_of_contact,
                     "communication_channel": self.communication_channel,
                     "contact_type": self.contact_type,
                     "attendees": self.attendees,
                     "note_content": self.note_content}
        return note_dict