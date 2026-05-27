from openai import OpenAI
from dotenv import load_dotenv
from typing import Type
import os

import logging # logs generation

from validation import agent_classifier_output,agent_reply_draft_output
from mail_tools import email_tools
from to_database import main_database,agent_records_database

load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('github_token')

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class agent:
  def __init__(self): # intitializing imps custom dependencies
    self.email_scrape = email_tools(resend_api_key=os.getenv('resend_api_key'))
    self.cursor = main_database()
    self.agent_cursor = agent_records_database()
    self.client = OpenAI(base_url="https://models.github.ai/inference") # custom base URL provider used github_model_marketplace

  
  def classifier(self,agent_prompt:str,
                 output_schema:Type[agent_classifier_output]=agent_classifier_output):

    self.output_schema = output_schema # pydantic output response schema for the classifier
    self.agent_prompt = agent_prompt
    
    self.getting_emails = self.email_scrape.fetch()
    self.emails = self.cursor.fetch_multiples()
    
    self.classification_results = []
    self.database_logs = []
    
    for email in self.emails:
      messages=[{'role':'system',
                'content':f'{self.agent_prompt}'},
                {'role':"user",
                'content':f'{email.body}'}] # message template for the model to use
      
      self.classification_response = self.client.chat.completions.parse(model="gpt-4o",
                                                  messages=messages,
                                                  response_format=self.output_schema)

      self.result = self.classification_response.choices[0].message.parsed # the parsed result from the response
    # print(result)

    #### SAVING TO THE AGENT_RECORDS_DATABASE ####
    
      self.agent_classification = self.result.model_dump() # dumping the parsed result to dict format
      self.classification_results.append(self.agent_classification) # appends to the processed list
      
    # print(agent_classification)
    # print(email.model_dump())

      try: # saving to the agent records
        
        self.to_agent_records = self.agent_cursor.insert(message=(email.model_dump())|self.agent_classification) # a single UNION of all info dict record for the agent record saving
        if self.to_agent_records:
          database_saving_message = "saved to the agent record!"
          self.database_logs.append(database_saving_message)
          logging.info(database_saving_message)
        else:
          logging.info("same 'gmail_message_id' skipped!")
          
      except Exception as e:
          database_saving_message = f"Error on saving to the agent records : {e}"
          self.database_logs.append(database_saving_message)
          logging.info(database_saving_message)
      
      # print(to_agent_records)
      # print((agent_cursor.view(limit=3))[0].model_dump())
      
    return self.classification_results,self.database_logs
  
  def reply_drafting(self,agent_prompt:str,
                     first:bool=True,
                     output_schema:Type[agent_reply_draft_output]=agent_reply_draft_output):

    self.output_schema = output_schema
    self.first = first
    self.agent_prompt = agent_prompt
    
    if first == True:
      self.email_message = (self.cursor.fetch_one()).model_dump()
    
    self.messages=[{'role':'system',
              'content':f'{self.agent_prompt}'},
              {'role':"user",
              'content':f"subject={self.email_message['subject']},sender={self.email_message['sender']},body={self.email_message['body']}"}] # message template for the model to use
    try:
      self.classification_response = self.client.chat.completions.parse(model="gpt-4o",
                                                  messages=self.messages,
                                                  response_format=self.output_schema)

      self.result = self.classification_response.choices[0].message.parsed # parsed output of the Subject and Body for the drafted mail
      return self.result.model_dump() # final drafted reply in for dict['body','subject']
    
    except Exception as e:
      logging.info(f"something went wrong = {e}")
      return f'something went wrong = {e}'
