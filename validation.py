from pydantic import BaseModel, Field, AliasChoices
from typing import Literal

class agent_classifier_output(BaseModel):
    
    category:Literal['low','medium','high'] = Field(description="priority basis for the email")
    needs_reply:Literal["True","False"] = Field(description="basis on which reply should be drafted or not")
    summary:str =Field(description="short summary of the email")

class agent_reply_draft_output(BaseModel):
    subject:str = Field(description='The subject on which the email was based on.')
    sender:str = Field(description="the sender's email-id only")
    draft_reply:str = Field(description="The reply to the email drafted by the agent.")
    