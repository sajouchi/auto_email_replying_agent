import os
from typing import Any
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from bs4 import BeautifulSoup
import base64

from to_database import main_database
import resend # email sending api

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class email_tools:
    def __init__(self,resend_api_key:str = os.getenv('resend_api_key')):
        self.cursor_database = main_database()
        resend.api_key = resend_api_key
   
    def fetch(self,scope_paramter:str="readonly"):
        
        self.creds = None
        
        self.scope_parameter = scope_paramter
        self.SCOPES = [f"https://www.googleapis.com/auth/gmail.{self.scope_parameter}"]

        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json",self.SCOPES)
        if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

        if not self.creds or not self.creds.valid:
            logging.info("valid.json not found")
            # raise Exception("Valid token.json not found!")

        try:
            self.service = build('gmail','v1',credentials=self.creds)
            self.results = self.service.users().messages().list(maxResults=3,userId="me").execute()

            self.messages = self.results.get('messages')

            self.count = 0
            self.error = None
            for msg in self.messages:
                
                self.gmail_message_id = msg['id']
                txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()

                try:
                    self.payload = txt['payload']
                    self.headers = self.payload['headers']
                    self.subject = "No subject"
                    self.sender = "Unknown Sender"
                    
                    for d in self.headers:
                        if d['name'] == 'Subject':
                            self.subject = d['value']
                        if d['name'] == 'From':
                            self.sender = d['value']

                    self.parts = self.payload.get('parts')[0]
                    if not self.parts:
                        # print("no parts found!")
                        logging.info("no parts found!")

                    self.data = self.parts['body']['data']
                    self.data = self.data.replace("-","+").replace("_","/")
                    self.decoded_data = base64.b64decode(self.data)

                    self.soup = BeautifulSoup(self.decoded_data , "lxml")
                    self.body = self.soup.get_text()

                    self.count += 1

                    self.email_message = dict(
                        subject=self.subject,
                        gmail_message_id=self.gmail_message_id,
                        sender=self.sender,
                        body=self.body
                    )
                    
                    self.entry_message = None 
                    
                    if not self.cursor_database.exist(gmail_message_id=self.gmail_message_id):
                        self.entry_message = self.cursor_database.insert(
                            message=self.email_message
                        )

                except Exception as e:
                    self.error = e

            if not self.error:
                return self.entry_message
            else:
                return f"error : {self.error}"
            
        except HttpError as error:
            return f"An error occurred :- {error}"
    
    def send(self,replies:dict[str,Any],from_email:str='onboarding@resend.dev',):
        params = {
                    "from": from_email,
                    "to" : [replies['sender'].strip()],
                    "subject": replies['subject'],
                    "text": replies['draft_reply']
                }
        if resend.api_key:
            try:
                mail_sending = resend.Emails.send(params)

                return True,f"E-mail send successfully to {params['to'][0]}, resend id - '{mail_sending['id']}'"
            except Exception as e:
                return False,f"something went wrong while sending email : '{e}'"
        else:
            return False,f"None or invalid resend api_key used!"