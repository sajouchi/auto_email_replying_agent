# 🤖 Auto Email Replying Agent

An experimental AI-powered email automation system that reads emails, analyzes them using LLMs, drafts replies, asks for human approval through Telegram, and (eventually 👀) sends replies automatically.

---

# 🚀 What Is This Project?

This project is my attempt at building a small **Agentic AI Workflow System** using:

- 📧 Gmail API
- 🧠 OpenAI/GitHub Models
- 🤖 Telegram Bot
- 🗄️ SQLite Databases
- ⚡ GitHub Actions
- 🐍 Python

The goal is to create an AI assistant that can:

```text
Read Emails
   ↓
Understand Them
   ↓
Classify Priority
   ↓
Draft Replies
   ↓
Ask Human Permission
   ↓
Send Reply
```

Basically...

👉 an AI email worker with human supervision.

---

# 🧠 Current Features

## ✅ Email Fetching

- Reads emails using Gmail API
- Extracts:
  - sender
  - subject
  - body
  - gmail message id

---

## ✅ AI Email Analysis

The AI currently:

- classifies email priority
- decides if reply is needed
- generates summaries

Example:

```json
{
  "category": "high",
  "needs_reply": "True",
  "summary": "Client asking for urgent update."
}
```

---

## ✅ AI Reply Drafting

The system can generate reply drafts automatically.

Example:

```json
{
  "subject": "Re: Project Update",
  "sender": "someone@gmail.com",
  "draft_reply": "Thank you for reaching out..."
}
```

---

## ✅ Telegram Approval Workflow 🤖

Before sending mails, the system asks for approval on Telegram.

So the workflow becomes:

```text
AI drafts mail
    ↓
Telegram asks:
"YES or NO?"
    ↓
Human approves
    ↓
Mail gets sent
```

This helps avoid:

- accidental replies 😭
- AI hallucinations 😵
- dangerous automation mistakes 💀

---

## ✅ Duplicate Email Protection

The system avoids processing the same email repeatedly using:

```text
gmail_message_id
```

This becomes VERY important for scheduled automation.

---

## ✅ Logging Support

Added logging support for:

- email processing
- database inserts
- workflow tracking
- debugging GitHub Actions

---

## ✅ GitHub Actions Automation

The project is now moving toward:

```text
Fully scheduled cloud automation ☁️
```

using GitHub Actions.

Current goal:

- run every few hours
- automatically check emails
- process them remotely

---

# 🏗️ Current Architecture

```text
Gmail API
    ↓
Email Fetcher
    ↓
SQLite Database
    ↓
AI Classifier Agent
    ↓
Reply Drafting Agent
    ↓
Telegram Approval
    ↓
Email Sender
```

---

# 📂 Project Structure

```text
.
├── agent.py
├── agent_script_final.py
├── mail_tools.py
├── notification.py
├── to_database.py
├── validation.py
├── requirements.txt
├── database.db
├── agent_records.db
└── prompts/
```

---

# ⚡ Tech Stack

| Tool                 | Purpose               |
| -------------------- | --------------------- |
| Python               | Core backend          |
| Gmail API            | Email fetching        |
| OpenAI/GitHub Models | AI processing         |
| Telegram Bot API     | Human approval        |
| SQLModel + SQLite    | Databases             |
| GitHub Actions       | Scheduling            |
| Pydantic             | Structured AI outputs |

---

# 🎯 Current Status

## 🟡 MVP / Experimental Stage

The project is still under active development.

Right now it:

- works locally
- partially works with automation
- supports AI email analysis
- supports AI draft generation
- supports Telegram approval flow

Still improving:

- better scheduling
- queue systems
- smarter email parsing
- timeout handling
- production reliability
- multi-email drafting pipeline

---

# 🧪 Why I Built This

Mainly to learn:

- agentic AI systems
- automation workflows
- async Python
- API integrations
- structured AI outputs
- production-style backend thinking

This project started as:

```text
"Can AI reply to emails?"
```

and slowly evolved into:

```text
"Can I build a mini autonomous workflow system?"
```

😄

---

# 🔥 Future Goals

Planned upgrades:

- [ ] Better email threading
- [ ] Queue-based processing
- [ ] Smarter classification
- [ ] Attachment support
- [ ] Memory/context system
- [ ] Full GitHub Actions deployment
- [ ] Multi-agent workflows
- [ ] Dashboard/Frontend
- [ ] Docker deployment
- [ ] RAG-based contextual replies

---

# ⚠️ Important Note

This is an experimental learning project.

The AI is NOT trusted to fully auto-send emails yet 😅

Human approval is intentionally kept in the loop for safety.

---

# 🛠️ Setup

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Add Environment Variables

Create `.env`

```env
github_token=YOUR_KEY
resend_api_key=YOUR_KEY
bot_token=YOUR_KEY
chat_id=YOUR_CHAT_ID
```

---

## Run Project

```bash
python agent_script_final.py
```

---

# 📸 Upcoming Improvements

Will soon add:

- screenshots
- workflow demos
- architecture diagrams
- GitHub Actions screenshots

---

# 💡 Lessons Learned So Far

This project taught me that:

```text
Building AI features is easy.

Building reliable automation is the hard part.
```

😅

---

# ⭐ Final Thoughts

Still learning.
Still improving.
Still breaking things and fixing them 🚀

But this project has been an amazing way to learn:

- AI systems
- automation
- backend engineering
- real-world debugging

Thanks for checking it out ❤️
