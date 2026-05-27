import asyncio
import logging
import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level = logging.INFO,
                    format="%(asctime)s - %(levelmessage)s - %(message)s")

load_dotenv()


class TelegramBot:

    def __init__(self):

        self.bot_token = os.getenv("bot_token")
        self.chat_id = os.getenv("my_chat_id")

        self.user_response = None
        self.response_event = asyncio.Event()

        self.app = (
            ApplicationBuilder()
            .token(self.bot_token)
            .build()
        )

        self.app.add_handler(
            MessageHandler(
                filters.TEXT,
                self.handle_message
            )
        )

    async def handle_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        if str(update.effective_chat.id) != self.chat_id:
            return

        self.user_response = update.message.text.lower().strip()

        # print("User Response:", self.user_response)
        logging.info(f"user response = {self.user_response}")

        self.response_event.set()

    async def start(self):

        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

    async def stop(self):

        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()

    async def send_message(
        self,
        message: str
    ):

        await self.app.bot.send_message(
            chat_id=self.chat_id,
            text=message
        )

    async def request_permission(
        self,
        draft_reply: str
    ):

        self.user_response = None
        self.response_event.clear()

        request_message = f"""
Need permission to send mail.

Drafted Mail:
{draft_reply}

Reply with:
YES or NO
"""

        await self.send_message(request_message)

        # print("Waiting for user response...")
        logging.info(f"wating for response....")

        await self.response_event.wait()

        if self.user_response == "yes":
            
            logging.info("Sending the mail....")
            await self.send_message(
                "Sending the mail..."
            )

        elif self.user_response == "no":
            
            logging.info("Cancelled task...")
            await self.send_message(
                "Cancelled task..."
            )
            

        return self.user_response

    async def notify_success(self,msg:str):
        await self.send_message(
            f"{msg}"
        )

    async def notify_error(
        self,
        error_message: str
    ):

        await self.send_message(
            f"Error Occurred:\n{error_message}"
        )