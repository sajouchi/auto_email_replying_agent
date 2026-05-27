import os
import logging
import asyncio

from agent import agent
from mail_tools import email_tools
from notification import TelegramBot

from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('github_token') # setting up model api key

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

with open("analysis_agent_system_prompts.md",'r') as f:
    classifier_system_prompt = f.read()

with open("draft_reply_agent_system_prompt.md",'r') as f:
    draft_reply_system_prompt = f.read()

async def main():
    
    auto_agent = agent()
    email_tool = email_tools(resend_api_key=os.getenv('resend_api_key'))  
    telegram_bot = TelegramBot()
    
    try:
        analysis, back_message = auto_agent.classifier(agent_prompt=classifier_system_prompt)
        logging.info(f"classifier result = {analysis}")
        logging.info(f"message - {back_message}")
        draft_reply = auto_agent.reply_drafting(agent_prompt=draft_reply_system_prompt)
        
        await telegram_bot.start()
        host_response = await telegram_bot.request_permission(draft_reply=draft_reply['draft_reply'])
        
        if host_response.lower() == 'yes':
            # sending_mail,status_message = email_tool.send(replies=draft_reply)
            sending_mail,status_message = True,"send successfully to 'gauravthapa2727@gmail.com"
            # print(draft_reply)
            logging.info(f"drafted reply = {draft_reply}")
            logging.info(f"status_message = {status_message}")
            if sending_mail:
                logging.info(f"success message = {status_message}")
                await telegram_bot.notify_success(msg=status_message)
            else:
                logging.info(f"error message = {status_message}")
                await telegram_bot.notify_error(error_message=status_message)

    except Exception as e:
        logging.info(f'something went wrong - {e}')
        return f"something went wrong : {e}"

if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    