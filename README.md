cat > /home/claude/make_notebooks.py << 'PYEOF'
import json, os

def nb(cells):
return {
"nbformat": 4, "nbformat_minor": 5,
"metadata": {
"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
"language_info": {"name": "python", "version": "3.10.0"}
},
"cells": cells
}

def md(src, cid=None):
return {"cell*type":"markdown","id": cid or src[:8].replace(" ","*").replace("#","")+"\_md","metadata":{},"source": src}

def code(src, cid=None):
return {"cell*type":"code","id": cid or src[:8].replace(" ","*")+"\_cd","metadata":{},"execution_count":None,"outputs":[],"source": src}

# ─────────────────────────────────────────────

# 00_introduction.ipynb

# ─────────────────────────────────────────────

c00 = [
md("""# 🦜 Tutorial 00 — LangChain পরিচিতি
**Phase 1 | Foundation | Level: Beginner**

---

> 🎯 **এই tutorial শেষে তুমি জানবে:**
>
> - LangChain কী এবং কেন দরকার
> - LangChain ছাড়া vs সহ — পার্থক্য কী
> - LangChain এর মূল অংশগুলো কী কী
> - বাস্তব জীবনে কোথায় ব্যবহার হয়"""),

md("""---

## 📌 ধাপ ১ — LangChain কী?

সহজ কথায়: **LangChain হলো AI দিয়ে application বানানোর framework।**

### একটা উদাহরণ দিয়ে বুঝি:

কল্পনা করো তুমি একটা **রেস্তোরাঁ** চালাচ্ছো।

| রেস্তোরাঁ            | LangChain জগৎ          |
| -------------------- | ---------------------- |
| রাঁধুনি              | AI Model (Gemini, GPT) |
| রেসিপি               | Prompt Template        |
| অর্ডার নেওয়া        | Input handling         |
| খাবার পরিবেশন        | Output parsing         |
| ম্যানেজমেন্ট সিস্টেম | **LangChain**          |

শুধু রাঁধুনি থাকলেই রেস্তোরাঁ চলে না — দরকার পুরো সিস্টেম।  
ঠিক তেমনি শুধু Gemini API থাকলেই হয় না — দরকার LangChain।"""),

md("""---

## 📌 ধাপ ২ — LangChain ছাড়া vs সহ

### ❌ LangChain ছাড়া (raw API):"""),

code('''# LangChain ছাড়া Gemini ব্যবহার — অনেক বেশি কোড লিখতে হয়
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Prompt manually বানাতে হয়

prompt = f"""তুমি একজন সহায়ক assistant।
ব্যবহারকারীর প্রশ্ন: বাংলাদেশের রাজধানী কী?
বাংলায় উত্তর দাও।"""

response = model.generate_content(prompt)

# Response manually parse করতে হয়

print(response.text)'''),

md("""### ✅ LangChain সহ (সহজ ও সুন্দর):"""),

code('''# LangChain দিয়ে — পরিষ্কার, reusable, সহজ
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
prompt = ChatPromptTemplate.from_template("বাংলায় উত্তর দাও: {question}")
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "বাংলাদেশের রাজধানী কী?"}))'''),

md("""---

## 📌 ধাপ ৩ — LangChain এর মূল অংশ

LangChain ৬টা মূল building block নিয়ে তৈরি:

```
┌─────────────────────────────────────────────────────┐
│                    LangChain                        │
│                                                     │
│  📝 Prompts    → AI কে নির্দেশ দেওয়া              │
│  🤖 Models     → Gemini, GPT ইত্যাদি               │
│  🔧 Output     → AI এর উত্তর format করা            │
│  ⛓  Chains     → ধাপগুলো একসাথে জোড়া             │
│  💾 Memory     → কথা মনে রাখা                      │
│  🕵️ Agents     → AI নিজে সিদ্ধান্ত নেয়             │
└─────────────────────────────────────────────────────┘
```

এই ৬টা জিনিস আমরা পরের tutorial গুলোতে একে একে শিখবো।"""),

md("""---

## 📌 ধাপ ৪ — বাস্তব জীবনে LangChain কোথায় ব্যবহার হয়?

| Application           | কীভাবে কাজ করে                |
| --------------------- | ----------------------------- |
| 📄 PDF Q&A Bot        | PDF পড়ে প্রশ্নের উত্তর দেয়  |
| 💬 Customer Support   | ২৪/৭ প্রশ্নের উত্তর দেয়      |
| 🔍 Research Agent     | Web search করে report লেখে    |
| 📊 Data Analyst       | CSV দেখে chart ও analysis করে |
| 🌐 Translator         | যেকোনো ভাষায় অনুবাদ করে      |
| 🛒 Shopping Assistant | পণ্য খুঁজে দেয় ও তুলনা করে   |

এই সব আমরা **Phase 5** এ নিজেরা বানাবো!"""),

md("""---

## 📌 ধাপ ৫ — LangChain এর Architecture

```
তোমার প্রশ্ন
     ↓
[Prompt Template]  ← নির্দেশ format করে
     ↓
[LLM - Gemini]    ← AI চিন্তা করে
     ↓
[Output Parser]   ← উত্তর clean করে
     ↓
তোমার উত্তর
```

এই পুরো flow কে বলে **Chain**।  
আর `|` চিহ্ন দিয়ে এই ধাপগুলো জোড়া দেওয়া হয় — এটাকে বলে **LCEL** (LangChain Expression Language)।"""),

md("""---

## ✅ Summary — আজকে যা শিখলে

- ✅ LangChain হলো AI application বানানোর framework
- ✅ Raw API এর চেয়ে LangChain বেশি সহজ ও organized
- ✅ ৬টা মূল অংশ: Prompts, Models, Output, Chains, Memory, Agents
- ✅ বাস্তবে অনেক কাজে ব্যবহার হয়

## ⏭ পরের Tutorial

**01_environment_setup** — Python, pip, Gemini API key সব সেটআপ করবো।

---

> 💬 **প্রশ্ন থাকলে** GitHub Issues এ বাংলায় লিখো!"""),
> ]

# ─────────────────────────────────────────────

# 01_environment_setup.ipynb

# ─────────────────────────────────────────────

c01 = [
md("""# 🦜 Tutorial 01 — Environment Setup
**Phase 1 | Foundation | Level: Beginner**

---

> 🎯 **এই tutorial শেষে তুমি পারবে:**
>
> - Python ঠিকমতো install করতে
> - Virtual environment তৈরি করতে
> - LangChain ও Gemini library install করতে
> - Gemini API key নিতে ও সেটআপ করতে
> - `.env` file ব্যবহার করতে"""),

md("""---

## 📌 ধাপ ১ — Python Check করো

প্রথমে দেখো Python আছে কিনা:"""),

code('''# Python version check করো
import sys
print(f"Python version: {sys.version}")
print(f"Python location: {sys.executable}")

# Python 3.9 বা তার উপরে থাকতে হবে

version = sys.version_info
if version.major == 3 and version.minor >= 9:
print("✅ Python version ঠিক আছে!")
else:
print("❌ Python 3.9+ দরকার। python.org থেকে নামাও।")'''),

md("""---

## 📌 ধাপ ২ — Virtual Environment

**Virtual environment কী?**

মনে করো তোমার বাসায় আলাদা আলাদা রুম আছে। প্রতিটা project এর জন্য আলাদা রুম — তাহলে একটার জিনিস আরেকটায় গিয়ে সমস্যা হবে না।

Virtual environment ঠিক এই কাজই করে।

**Terminal এ চালাও (এই notebook এ নয়):**

````bash
# Virtual environment তৈরি করো
python -m venv venv

# Activate করো
source venv/bin/activate        # Mac/Linux
# venv\\Scripts\\activate       # Windows

# Activate হলে terminal এ দেখবে:
# (venv) $
```"""),

md("""---
## 📌 ধাপ ৩ — Library Install করো"""),

code('''# Notebook থেকে সরাসরি install করা যায়
# ! মানে terminal command

!pip install langchain langchain-google-genai langchain-core python-dotenv -q

print("✅ Core libraries install হয়ে গেছে!")'''),

code('''# Install হয়েছে কিনা check করো
import langchain
import langchain_google_genai

print(f"LangChain version: {langchain.__version__}")
print("✅ সব library সঠিকভাবে install হয়েছে!")'''),

md("""---
## 📌 ধাপ ৪ — Gemini API Key নেওয়া (ফ্রি!)

### Step by step:

1. যাও → **https://aistudio.google.com**
2. Google account দিয়ে **Sign in** করো
3. উপরে **"Get API Key"** বাটন click করো
4. **"Create API Key"** click করো
5. Key টা **copy** করে রাখো

> ⚠️ **সতর্কতা:** API Key কখনো GitHub এ push করো না!
> এটা তোমার password এর মতো — গোপন রাখো।

### Free Tier Limits:
| Model | Free limit |
|-------|-----------|
| gemini-2.0-flash | ১৫ req/min, ১৫০০ req/day |
| gemini-1.5-pro | ২ req/min |

শেখার জন্য এটা যথেষ্ট!"""),

md("""---
## 📌 ধাপ ৫ — .env File তৈরি করো

**.env file কী?**

এটা একটা গোপন ফাইল যেখানে API key রাখা হয়। Code এ সরাসরি key লেখা ঠিক না — তাই এই পদ্ধতি।

**প্রজেক্ট folder এ `.env` নামে file তৈরি করো:**
````

GOOGLE*API_KEY=তোমার_api_key*এখানে*paste*করো

```

**তারপর Python এ এভাবে load করো:**"""),

code('''import os
from dotenv import load_dotenv

# .env file থেকে key load করো
load_dotenv()

# Check করো key load হয়েছে কিনা
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    # Key এর শুরুর কয়েকটা character দেখাই (সম্পূর্ণ না)
    print(f"✅ API Key পাওয়া গেছে: {api_key[:8]}...")
else:
    print("❌ API Key পাওয়া যায়নি। .env file check করো।")'''),

md("""---
## 📌 ধাপ ৬ — সব ঠিক আছে কিনা Test করো"""),

code('''# Final test — সব একসাথে
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Model তৈরি করো
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# একটা ছোট test করো
response = llm.invoke("হ্যালো! তুমি কি বাংলায় কথা বলতে পারো? একটা লাইনে উত্তর দাও।")
print("AI এর উত্তর:", response.content)
print("\\n✅ সব কিছু ঠিকমতো কাজ করছে!")'''),

md("""---
## ✅ Summary — আজকে যা করলে

- ✅ Python version check করলে
- ✅ LangChain ও Gemini library install করলে
- ✅ Gemini API Key নিলে
- ✅ `.env` file দিয়ে key সুরক্ষিত রাখলে
- ✅ প্রথম AI call সফলভাবে করলে!

## ⏭ পরের Tutorial
**02_python_basics_for_langchain** — LangChain এ লাগে এমন Python জিনিসগুলো শিখবো।

---
> 🐛 **সমস্যা হলে:** `resources/common_errors.md` দেখো"""),
]

# ─────────────────────────────────────────────
# 02_python_basics_for_langchain.ipynb
# ─────────────────────────────────────────────
c02 = [
md("""# 🦜 Tutorial 02 — LangChain এর জন্য Python Basics
**Phase 1 | Foundation | Level: Beginner**

---
> 🎯 **এই tutorial শেষে তুমি জানবে:**
> - Variables ও data types
> - Functions ও return
> - Dictionary ও List
> - f-string দিয়ে text formatting
> - Import করার নিয়ম
> - Environment variable পড়া
>
> *শুধু LangChain এ যা লাগবে তাই শেখাবো — পুরো Python কোর্স না!*"""),

md("---\n## 📌 ধাপ ১ — Variables ও Data Types\n\nLangChain এ কাজ করতে এই basic জিনিসগুলো জানা দরকার:"),

code('''# Variables — তথ্য সংরক্ষণ করার পাত্র
name = "রহিম"           # str (text)
age = 25               # int (সংখ্যা)
temperature = 0.7      # float (দশমিক) — LangChain এ খুব দরকার
is_active = True       # bool (হ্যাঁ/না)

print(f"নাম: {name}")
print(f"বয়স: {age}")
print(f"Temperature: {temperature}")
print(f"Active: {is_active}")
print(f"Type of temperature: {type(temperature)}")'''),

md("---\n## 📌 ধাপ ২ — Dictionary (LangChain এ সবচেয়ে বেশি ব্যবহার)\n\nLangChain এ প্রায় সবকিছু dictionary দিয়ে পাঠানো হয়:"),

code('''# Dictionary — key-value pair সংরক্ষণ
# LangChain এ invoke() করার সময় এটাই ব্যবহার হয়

person = {
    "name": "করিম",
    "age": 30,
    "city": "ঢাকা"
}

# Value পড়া
print(person["name"])       # করিম
print(person.get("age"))    # 30
print(person.get("phone", "নেই"))  # নেই (default value)

# LangChain এ এভাবে ব্যবহার হয়:
chain_input = {
    "question": "বাংলাদেশের রাজধানী কী?",
    "language": "বাংলা"
}
print("\\nChain input:", chain_input)'''),

md("---\n## 📌 ধাপ ৩ — List\n\nMessages ও documents list এ রাখা হয়:"),

code('''# List — অনেক জিনিস একসাথে রাখা
fruits = ["আম", "কাঁঠাল", "লিচু"]

# LangChain এ chat history এভাবে থাকে:
chat_history = [
    {"role": "user", "content": "তুমি কে?"},
    {"role": "assistant", "content": "আমি একটি AI assistant।"},
    {"role": "user", "content": "তুমি কী করতে পারো?"},
]

# List এ নতুন জিনিস যোগ করা
chat_history.append({"role": "assistant", "content": "আমি অনেক কিছু করতে পারি!"})

print(f"মোট messages: {len(chat_history)}")
print(f"প্রথম message: {chat_history[0]}")
print(f"শেষ message: {chat_history[-1]}")'''),

md("---\n## 📌 ধাপ ৪ — f-string (Prompt Template এর ভিত্তি)\n\nLangChain এর Prompt Template আসলে f-string এর উপর ভিত্তি করে তৈরি:"),

code('''# f-string — variable দিয়ে text বানানো
name = "রহিম"
topic = "Python"

# সাধারণ f-string
message = f"হ্যালো {name}! তুমি কি {topic} শিখছো?"
print(message)

# Multiline f-string — LangChain Prompt এর মতো
prompt_template = f"""তুমি একজন সহায়ক শিক্ষক।

ছাত্রের নাম: {name}
বিষয়: {topic}

এই বিষয়ে সহজভাবে ব্যাখ্যা করো।"""

print("\\nPrompt:")
print(prompt_template)'''),

md("---\n## 📌 ধাপ ৫ — Functions (Chains এর মতো চিন্তা করো)\n\nLangChain এর প্রতিটা step আসলে একটা function এর মতো কাজ করে:"),

code('''# Function — একটা নির্দিষ্ট কাজ করার block
def greet(name: str) -> str:
    """কাউকে বাংলায় greet করো"""
    return f"আস্সালামুআলাইকুম, {name}!"

def make_prompt(question: str, language: str = "বাংলা") -> str:
    """Prompt তৈরি করো"""
    return f"{language} ভাষায় উত্তর দাও: {question}"

# Function call করা
result = greet("করিম")
print(result)

prompt = make_prompt("পৃথিবী কত বড়?")
print(prompt)

# Type hints — LangChain এ এটা গুরুত্বপূর্ণ
# str, int, float, bool, list, dict, Optional[str]'''),

md("---\n## 📌 ধাপ ৬ — Import করার নিয়ম\n\nLangChain এ অনেক জিনিস import করতে হয়:"),

code('''# Import করার ৩ ধরন

# ১. পুরো module import
import os
import json

# ২. নির্দিষ্ট জিনিস import
from dotenv import load_dotenv
from typing import Optional, List

# ৩. LangChain থেকে import (সবচেয়ে বেশি করবে)
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# Package structure বুঝতে হবে:
# langchain_google_genai → Google/Gemini related
# langchain_core         → মূল building blocks
# langchain_community    → তৃতীয় পক্ষের tools

print("Import pattern:")
print("from [package] import [class/function]")
print("\\nos.getenv example:")
print(os.getenv("PATH", "PATH না পাওয়া গেলে এটা দেখাবে")[:50] + "...")'''),

md("---\n## 📌 ধাপ ৭ — সব একসাথে — Mini LangChain Pattern"),

code('''# এখন সব মিলিয়ে দেখো — LangChain কীভাবে কাজ করে সেটার pattern
import os
from dotenv import load_dotenv

# ১. Environment load করো
load_dotenv()

# ২. Config dictionary বানাও
config = {
    "model": "gemini-2.0-flash",
    "temperature": 0.7,
    "language": "বাংলা"
}

# ৩. Prompt বানানোর function
def create_prompt(question: str, language: str) -> str:
    return f"{language} ভাষায় সংক্ষেপে উত্তর দাও: {question}"

# ৪. Messages list
messages = []

def add_message(role: str, content: str):
    messages.append({"role": role, "content": content})

# ব্যবহার করো
question = "Python কী?"
prompt = create_prompt(question, config["language"])
add_message("user", prompt)

print("Config:", config)
print("\\nPrompt:", prompt)
print("\\nMessages:", messages)
print("\\n✅ LangChain এর মূল pattern বুঝে গেছো!")'''),

md("""---
## ✅ Summary — আজকে যা শিখলে

| বিষয় | LangChain এ কোথায় লাগে |
|-------|------------------------|
| Dictionary | `chain.invoke({"question": "..."})` |
| List | Chat history, documents |
| f-string | Prompt template এর ভিতরে |
| Function | Custom tools, parsers |
| Import | LangChain library ব্যবহার |
| Type hints | Tool ও function definition |

## ⏭ পরের Tutorial
**03_first_llm_call** — এখন সত্যিকারের Gemini call করবো!"""),
]

# ─────────────────────────────────────────────
# 03_first_llm_call.ipynb
# ─────────────────────────────────────────────
c03 = [
md("""# 🦜 Tutorial 03 — প্রথম LLM Call!
**Phase 1 | Foundation | Level: Beginner**

---
> 🎯 **এই tutorial শেষে তুমি পারবে:**
> - `ChatGoogleGenerativeAI` setup করতে
> - `invoke()` দিয়ে AI কে প্রশ্ন করতে
> - Response থেকে text বের করতে
> - বাংলায় AI কথা বলাতে"""),

md("---\n## 📌 ধাপ ১ — Setup"),

code('''import os
from dotenv import load_dotenv

load_dotenv()

# Check
key = os.getenv("GOOGLE_API_KEY")
if key:
    print(f"✅ API Key ready: {key[:8]}...")
else:
    print("❌ .env file এ GOOGLE_API_KEY দাও!")'''),

md("---\n## 📌 ধাপ ২ — Model তৈরি করো\n\nLangChain এ Gemini ব্যবহার করতে `ChatGoogleGenerativeAI` class লাগে:"),

code('''from langchain_google_genai import ChatGoogleGenerativeAI

# Model তৈরি করো
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",   # কোন model ব্যবহার করবে
    temperature=0.7,            # 0 = নির্ভরযোগ্য, 1 = সৃজনশীল
)

print("✅ Model তৈরি হয়ে গেছে!")
print(f"Model: {llm.model}")'''),

md("---\n## 📌 ধাপ ৩ — প্রথম invoke()!\n\n`invoke()` মানে AI কে একটা কাজ দেওয়া এবং উত্তর নেওয়া:"),

code('''# সবচেয়ে সহজ call — শুধু string পাঠাও
response = llm.invoke("তুমি কে? একটা বাক্যে বলো।")

# Response একটা AIMessage object
print("Response type:", type(response))
print("Response content:", response.content)'''),

code('''# আরো কিছু প্রশ্ন করি
questions = [
    "বাংলাদেশের রাজধানী কী?",
    "Python কী সেটা ৩ লাইনে বলো।",
    "আজকের দিনটা সুন্দর কেন হতে পারে?"
]

for q in questions:
    response = llm.invoke(q)
    print(f"প্রশ্ন: {q}")
    print(f"উত্তর: {response.content}")
    print("-" * 50)'''),

md("---\n## 📌 ধাপ ৪ — Response Object বোঝা\n\nAI যা ফেরত দেয় সেটা একটা `AIMessage` object:"),

code('''response = llm.invoke("LangChain কী? ২ লাইনে বলো।")

# Response এর বিভিন্ন অংশ
print("=== Response Object ===")
print(f"Content (উত্তর): {response.content}")
print(f"Type: {type(response)}")

# Response metadata
if hasattr(response, 'usage_metadata') and response.usage_metadata:
    print(f"\\n=== Token Usage ===")
    print(f"Input tokens: {response.usage_metadata.input_tokens}")
    print(f"Output tokens: {response.usage_metadata.output_tokens}")'''),

md("---\n## 📌 ধাপ ৫ — বাংলায় কথা বলানো\n\nSystem instruction দিয়ে AI কে বাংলায় কথা বলতে বলা যায়:"),

code('''from langchain_core.messages import SystemMessage, HumanMessage

# System message দিয়ে AI এর behavior ঠিক করো
messages = [
    SystemMessage(content="তুমি একজন বাংলাভাষী সহায়ক। সবসময় বাংলায় উত্তর দাও। সহজ ও সংক্ষিপ্ত থাকো।"),
    HumanMessage(content="What is the capital of Bangladesh?")
]

# ইংরেজিতে প্রশ্ন করলেও বাংলায় উত্তর আসবে
response = llm.invoke(messages)
print("ইংরেজি প্রশ্নে বাংলা উত্তর:")
print(response.content)'''),

md("---\n## 📌 ধাপ ৬ — একটা ছোট্ট Q&A Function বানাই"),

code('''def ask_in_bangla(question: str) -> str:
    """
    বাংলায় প্রশ্ন করো, বাংলায় উত্তর পাও।

    Args:
        question: তোমার প্রশ্ন
    Returns:
        AI এর উত্তর (বাংলায়)
    """
    from langchain_core.messages import SystemMessage, HumanMessage

    messages = [
        SystemMessage(content="তুমি একজন বন্ধুসুলভ বাংলাভাষী AI। সহজ বাংলায় উত্তর দাও।"),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)
    return response.content

# Test করো
print(ask_in_bangla("AI শেখা কি কঠিন?"))
print("\\n" + "="*50 + "\\n")
print(ask_in_bangla("LangChain শিখলে কী হবে?"))'''),

md("""---
## ✅ Summary

| বিষয় | Code |
|-------|------|
| Model তৈরি | `ChatGoogleGenerativeAI(model="gemini-2.0-flash")` |
| AI কে call করা | `llm.invoke("প্রশ্ন")` |
| উত্তর পড়া | `response.content` |
| বাংলায় force করা | `SystemMessage` ব্যবহার |

## ⏭ পরের Tutorial
**04_messages_and_roles** — SystemMessage, HumanMessage, AIMessage বিস্তারিত।"""),
]

# ─────────────────────────────────────────────
# 04_messages_and_roles.ipynb
# ─────────────────────────────────────────────
c04 = [
md("""# 🦜 Tutorial 04 — Messages ও Roles
**Phase 1 | Foundation | Level: Beginner**

---
> 🎯 **এই tutorial শেষে তুমি জানবে:**
> - Message কী এবং কেন দরকার
> - `SystemMessage`, `HumanMessage`, `AIMessage` এর পার্থক্য
> - Chat history কীভাবে রাখতে হয়
> - `ChatPromptTemplate` দিয়ে messages বানানো"""),

md("""---
## 📌 ধাপ ১ — Message কী?

AI এর সাথে কথা বলার সময় প্রতিটা কথা একটা **Message**।

### তিন ধরনের Message:

```

┌─────────────────────────────────────────────────┐
│ SystemMessage → AI কে বলো সে কে │
│ HumanMessage → তোমার প্রশ্ন/কথা │  
│ AIMessage → AI এর উত্তর │
└─────────────────────────────────────────────────┘

```

**বাস্তব উদাহরণ:**
- System → "তুমি একজন ডাক্তার"
- Human  → "আমার মাথা ব্যথা করছে"
- AI     → "মাথা ব্যথার কারণ হতে পারে..."
- Human  → "কোন ওষুধ খাবো?"
- AI     → "প্যারাসিটামল খেতে পারো..."
"""),

md("---\n## 📌 ধাপ ২ — Setup"),

code('''import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
print("✅ Ready!")'''),

md("---\n## 📌 ধাপ ৩ — SystemMessage\n\nAI এর personality ও behavior ঠিক করে:"),

code('''# SystemMessage — AI কে বলো সে কে এবং কীভাবে কথা বলবে
system_msg = SystemMessage(content="""তুমি একজন অভিজ্ঞ বাংলা Python শিক্ষক।
- সহজ বাংলায় বোঝাও
- উদাহরণ দিয়ে বলো
- উৎসাহ দাও
- সংক্ষিপ্ত থাকো""")

human_msg = HumanMessage(content="Function কী?")

response = llm.invoke([system_msg, human_msg])
print("Python শিক্ষকের উত্তর:")
print(response.content)'''),

code('''# একই প্রশ্ন, ভিন্ন System — ভিন্ন উত্তর!
system_chef = SystemMessage(content="তুমি একজন রাঁধুনি। সব প্রশ্নের উত্তর রান্নার উপমা দিয়ে দাও।")

response2 = llm.invoke([system_chef, HumanMessage(content="Function কী?")])
print("রাঁধুনির উত্তর:")
print(response2.content)'''),

md("---\n## 📌 ধাপ ৪ — Chat History (Multi-turn conversation)\n\nএকাধিক বার কথা বলতে হলে history রাখতে হয়:"),

code('''# Chat history — আগের কথা মনে রাখা
chat_history = [
    SystemMessage(content="তুমি একজন বাংলাভাষী সহায়ক। সংক্ষিপ্ত উত্তর দাও।")
]

def chat(user_message: str) -> str:
    """
    User message নাও, history তে যোগ করো,
    AI call করো, উত্তর history তে রাখো।
    """
    # User message যোগ করো
    chat_history.append(HumanMessage(content=user_message))

    # AI call করো পুরো history দিয়ে
    response = llm.invoke(chat_history)

    # AI উত্তর history তে রাখো
    chat_history.append(AIMessage(content=response.content))

    return response.content

# কথোপকথন শুরু করো
print("আমি:", "আমার নাম রহিম।")
print("AI:", chat("আমার নাম রহিম।"))
print()
print("আমি:", "আমি কী শিখছি জানো?")
print("AI:", chat("আমি কী শিখছি জানো?"))
print()
print("আমি:", "আমার নাম কী ছিল মনে আছে?")
print("AI:", chat("আমার নাম কী ছিল মনে আছে?"))'''),

md("---\n## 📌 ধাপ ৫ — ChatPromptTemplate\n\nTemplate দিয়ে messages সহজে বানানো যায়:"),

code('''from langchain_core.prompts import ChatPromptTemplate

# Template তৈরি করো
prompt = ChatPromptTemplate.from_messages([
    ("system", "তুমি একজন {role}। {instruction}"),
    ("human", "{question}")
])

# Template fill করো
messages = prompt.format_messages(
    role="ইতিহাস শিক্ষক",
    instruction="বাংলায় সহজ করে বোঝাও।",
    question="মুক্তিযুদ্ধ কত সালে হয়েছিল?"
)

# Messages দেখো
for msg in messages:
    print(f"[{type(msg).__name__}]: {msg.content[:60]}...")

# AI কে পাঠাও
response = llm.invoke(messages)
print("\\nউত্তর:", response.content)'''),

md("---\n## 📌 ধাপ ৬ — Message Inspector\n\nMessages এর ভেতরে কী আছে দেখো:"),

code('''# Message object এর structure বোঝা
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

msgs = [
    SystemMessage(content="তুমি একজন সহায়ক।"),
    HumanMessage(content="হ্যালো!"),
]

response = llm.invoke(msgs)

# সব message দেখো
all_msgs = msgs + [response]
print("=== সব Messages ===")
for i, msg in enumerate(all_msgs):
    msg_type = type(msg).__name__
    print(f"\\n[{i+1}] {msg_type}")
    print(f"    Content: {msg.content[:80]}")
    print(f"    Role: {msg.type}")'''),

md("""---
## ✅ Summary

| Message | Role | কখন ব্যবহার |
|---------|------|------------|
| `SystemMessage` | system | AI এর behavior ঠিক করতে |
| `HumanMessage` | human | তোমার প্রশ্ন পাঠাতে |
| `AIMessage` | ai | AI এর উত্তর save রাখতে |

## ⏭ পরের Tutorial
**05_model_parameters** — temperature, max_tokens দিয়ে AI কে control করো।"""),
]

# ─────────────────────────────────────────────
# 05_model_parameters.ipynb
# ─────────────────────────────────────────────
c05 = [
md("""# 🦜 Tutorial 05 — Model Parameters
**Phase 1 | Foundation | Level: Beginner**

---
> 🎯 **এই tutorial শেষে তুমি জানবে:**
> - `temperature` কী এবং কীভাবে পরিবর্তন করে
> - `max_tokens` দিয়ে উত্তরের দৈর্ঘ্য নিয়ন্ত্রণ
> - `top_p` ও `top_k` এর কাজ
> - কোন কাজে কোন setting ভালো"""),

md("""---
## 📌 ধাপ ১ — Parameters কী?

Model parameters হলো AI এর **remote control**।

```

Temperature → AI কতটা creative হবে
Max Tokens → উত্তর কত লম্বা হবে
Top P → কত ধরনের শব্দ বেছে নেবে

```

রান্নার উপমা:
- `temperature` = মশলার পরিমাণ (বেশি = বেশি নতুনত্ব)
- `max_tokens` = প্লেটের আকার (ছোট = কম খাবার)"""),

md("---\n## 📌 ধাপ ২ — Setup"),

code('''import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
print("✅ Ready!")'''),

md("---\n## 📌 ধাপ ৩ — Temperature (সবচেয়ে গুরুত্বপূর্ণ)\n\n`0` থেকে `1` পর্যন্ত — বড় হলে বেশি creative:"),

code('''# একই প্রশ্ন, ভিন্ন temperature
question = "বৃষ্টির দিনে কী করা ভালো? ২টা idea দাও।"

for temp in [0.0, 0.5, 1.0]:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=temp
    )
    response = llm.invoke(question)
    print(f"\\n🌡️ Temperature = {temp}:")
    print(response.content)
    print("-" * 50)'''),

md("""**কখন কোন temperature ব্যবহার করবে:**

| কাজ | Temperature | কারণ |
|-----|-------------|------|
| তথ্য বের করা | `0.0–0.2` | নির্ভুলতা দরকার |
| প্রশ্নের উত্তর | `0.3–0.5` | balanced |
| গল্প লেখা | `0.7–0.9` | creativity দরকার |
| কবিতা/শিল্প | `1.0` | সর্বোচ্চ নতুনত্ব |"""),

md("---\n## 📌 ধাপ ৪ — Max Tokens\n\nউত্তর কত লম্বা হবে তা নিয়ন্ত্রণ করে:\n\n> **Token কী?** মোটামুটি ১ token ≈ ১টা ইংরেজি শব্দ বা ০.৭৫টা বাংলা শব্দ।"),

code('''# ছোট উত্তর
llm_short = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    max_tokens=50        # মাত্র ৫০ token
)

# লম্বা উত্তর
llm_long = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    max_tokens=300
)

question = "Python কী?"

r_short = llm_short.invoke(question)
r_long = llm_long.invoke(question)

print("📏 ছোট উত্তর (max_tokens=50):")
print(r_short.content)
print(f"\\nCharacters: {len(r_short.content)}")

print("\\n" + "="*50)

print("\\n📜 লম্বা উত্তর (max_tokens=300):")
print(r_long.content)
print(f"\\nCharacters: {len(r_long.content)}")'''),

md("---\n## 📌 ধাপ ৫ — কাজ অনুযায়ী সঠিক Configuration\n\nReal-world এ কোন কাজে কোন setting ব্যবহার করবে:"),

code('''# ১. তথ্য জিজ্ঞেস করা — নির্ভুল, সংক্ষিপ্ত
llm_factual = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1,
    max_tokens=100
)

# ২. বাংলা গল্প লেখা — creative, লম্বা
llm_creative = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.9,
    max_tokens=500
)

# ৩. Customer support — balanced
llm_support = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    max_tokens=200
)

# Test করো
print("📚 Factual (temp=0.1):")
print(llm_factual.invoke("বাংলাদেশ কখন স্বাধীন হয়?").content)

print("\\n🎨 Creative (temp=0.9):")
print(llm_creative.invoke("একটা ছোট ছড়া লেখো বৃষ্টি নিয়ে।").content)

print("\\n💬 Support (temp=0.3):")
print(llm_support.invoke("আমার পণ্য কখন ডেলিভারি হবে?").content)'''),

md("---\n## 📌 ধাপ ৬ — Parameter Cheat Sheet"),

code('''# Parameters এর summary
params_guide = {
    "temperature": {
        "range": "0.0 – 1.0",
        "low (0.0-0.3)": "নির্ভুল, predictable (facts, math)",
        "mid (0.4-0.6)": "balanced (Q&A, support)",
        "high (0.7-1.0)": "creative (story, poetry)"
    },
    "max_tokens": {
        "50-100": "এক লাইন উত্তর",
        "100-300": "paragraph উত্তর",
        "300-1000": "বিস্তারিত উত্তর",
        "1000+": "লম্বা লেখা বা analysis"
    }
}

for param, info in params_guide.items():
    print(f"\\n=== {param} ===")
    for key, val in info.items():
        print(f"  {key}: {val}")'''),

md("""---
## ✅ Phase 1 সম্পূর্ণ! 🎉

তুমি এখন জানো:

| Tutorial | বিষয় | ✅ |
|----------|-------|---|
| 00 | LangChain কী | ✅ |
| 01 | Environment Setup | ✅ |
| 02 | Python Basics | ✅ |
| 03 | First LLM Call | ✅ |
| 04 | Messages & Roles | ✅ |
| 05 | Model Parameters | ✅ |

## ⏭ Phase 2 শুরু করো!
**06_prompt_templates** — LangChain এর সবচেয়ে গুরুত্বপূর্ণ concept।

---
> 🏆 **অভিনন্দন!** Phase 1 শেষ করেছো!"""),
]

# Write all notebooks
notebooks = [
    ("00_introduction", c00),
    ("01_environment_setup", c01),
    ("02_python_basics_for_langchain", c02),
    ("03_first_llm_call", c03),
    ("04_messages_and_roles", c04),
    ("05_model_parameters", c05),
]

output_dir = "/home/claude/phase_01_foundation"
os.makedirs(output_dir, exist_ok=True)

for name, cells in notebooks:
    path = f"{output_dir}/{name}.ipynb"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb(cells), f, ensure_ascii=False, indent=1)
    print(f"✅ Created: {name}.ipynb")

print("\n🎉 Phase 1 — সব ৬টা notebook তৈরি হয়ে গেছে!")
PYEOF
python /home/claude/make_notebooks.py
Output

✅ Created: 00_introduction.ipynb
✅ Created: 01_environment_setup.ipynb
✅ Created: 02_python_basics_for_langchain.ipynb
✅ Created: 03_first_llm_call.ipynb
✅ Created: 04_messages_and_roles.ipynb
✅ Created: 05_model_parameters.ipynb

🎉 Phase 1 — সব ৬টা notebook তৈরি হয়ে গেছে!
Don
```
