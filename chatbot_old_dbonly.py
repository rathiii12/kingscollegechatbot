import os
import re
import time

from flask import current_app
from huggingface_hub import InferenceClient

from database import CollegeInfo


# ============================================================
# HUGGING FACE
# ============================================================

HF_TOKEN = os.environ.get("HF_TOKEN")

client = None

if HF_TOKEN:
    try:
        client = InferenceClient(
            token=HF_TOKEN
        )
    except Exception as e:
        print("HF client initialization error:", e)


MODEL = "openai/gpt-oss-120b:groq"


# ============================================================
# STOP WORDS
# ============================================================

STOPWORDS = {
    "what", "is", "are", "the", "a", "an",
    "tell", "me", "about", "please",
    "can", "you", "give", "show",
    "which", "how", "do", "does",
    "there", "any", "available",
    "in", "at", "of", "for", "to",
    "kce", "kings", "college", "engineering"
}


# ============================================================
# TEXT HELPERS
# ============================================================

def normalize_text(text):
    if not text:
        return ""

    text = str(text).lower()

    # Common variations
    text = text.replace("&", " and ")
    text = text.replace("-", " ")
    text = text.replace("/", " ")

    return text


def tokenize(text):
    text = normalize_text(text)

    words = re.findall(r"[a-zA-Z0-9]+", text)

    cleaned = []

    for word in words:

        # Basic singular handling
        if word.endswith("ies") and len(word) > 4:
            word = word[:-3] + "y"

        elif word.endswith("s") and len(word) > 3:
            word = word[:-1]

        if word not in STOPWORDS:
            cleaned.append(word)

    return cleaned


# ============================================================
# DATABASE
# ============================================================

def get_all_database_records():
    """
    Get all KCE information from the database.
    """

    try:
        records = CollegeInfo.query.all()
        return records

    except Exception as e:
        print("Database read error:", e)
        return []


# ============================================================
# DIRECT INTENT DETECTION
# ============================================================

def detect_intent(message):

    text = normalize_text(message)

    # --------------------------------------------------------
    # COURSES
    # --------------------------------------------------------

    course_words = [
        "course",
        "courses",
        "program",
        "programs",
        "programme",
        "programmes",
        "degree",
        "degrees",
        "ug",
        "pg",
        "undergraduate",
        "postgraduate",
        "phd",
        "doctorate",
        "study"
    ]

    if any(word in text for word in course_words):
        return "courses"

    # --------------------------------------------------------
    # DEPARTMENTS
    # --------------------------------------------------------

    department_words = [
        "department",
        "departments",
        "branch",
        "branches",
        "cse",
        "it department",
        "ece",
        "eee",
        "mechanical",
        "civil",
        "artificial intelligence"
    ]

    if any(word in text for word in department_words):
        return "departments"

    # --------------------------------------------------------
    # HOSTEL
    # --------------------------------------------------------

    hostel_words = [
        "hostel",
        "hostels",
        "accommodation",
        "room",
        "rooms"
    ]

    if any(word in text for word in hostel_words):
        return "hostel"

    # --------------------------------------------------------
    # TRANSPORT
    # --------------------------------------------------------

    transport_words = [
        "transport",
        "bus",
        "buses",
        "college bus",
        "college buses"
    ]

    if any(word in text for word in transport_words):
        return "transport"

    # --------------------------------------------------------
    # PLACEMENT
    # --------------------------------------------------------

    placement_words = [
        "placement",
        "placements",
        "job",
        "jobs",
        "career",
        "recruitment",
        "companies"
    ]

    if any(word in text for word in placement_words):
        return "placement"

    # --------------------------------------------------------
    # ADMISSION
    # --------------------------------------------------------

    admission_words = [
        "admission",
        "admissions",
        "apply",
        "application",
        "eligibility",
        "join",
        "joining"
    ]

    if any(word in text for word in admission_words):
        return "admission"

    # --------------------------------------------------------
    # CONTACT
    # --------------------------------------------------------

    contact_words = [
        "contact",
        "phone",
        "telephone",
        "mobile",
        "email",
        "mail",
        "address",
        "location"
    ]

    if any(word in text for word in contact_words):
        return "contact"

    # --------------------------------------------------------
    # LIBRARY
    # --------------------------------------------------------

    library_words = [
        "library",
        "libraries",
        "books",
        "book",
        "library timing",
        "library timings"
    ]

    if any(word in text for word in library_words):
        return "library"

    # --------------------------------------------------------
    # SCHOLARSHIP
    # --------------------------------------------------------

    scholarship_words = [
        "scholarship",
        "scholarships",
        "financial aid",
        "education loan"
    ]

    if any(word in text for word in scholarship_words):
        return "scholarship"

    # --------------------------------------------------------
    # INFRASTRUCTURE
    # --------------------------------------------------------

    infrastructure_words = [
        "infrastructure",
        "campus",
        "building",
        "facilities",
        "facility",
        "canteen",
        "health centre",
        "healthcare"
    ]

    if any(word in text for word in infrastructure_words):
        return "infrastructure"

    return None


# ============================================================
# INTENT BASED DATABASE SEARCH
# ============================================================

def get_intent_records(intent):

    records = get_all_database_records()

    if not records:
        return []

    matched = []

    # --------------------------------------------------------
    # COURSES
    # --------------------------------------------------------

    if intent == "courses":

        for record in records:

            category = normalize_text(record.category)
            title = normalize_text(record.title)
            content = normalize_text(record.content)

            if (
                category == "course"
                or "undergraduate" in title
                or "postgraduate" in title
                or "phd" in title
                or "program" in title
                or "programme" in title
                or "degree" in content
            ):
                matched.append(record)

    # --------------------------------------------------------
    # DEPARTMENTS
    # --------------------------------------------------------

    elif intent == "departments":

        for record in records:

            category = normalize_text(record.category)

            if category == "department":
                matched.append(record)

    # --------------------------------------------------------
    # OTHER CATEGORIES
    # --------------------------------------------------------

    elif intent == "hostel":

        for record in records:

            if normalize_text(record.category) == "hostel":
                matched.append(record)

    elif intent == "transport":

        for record in records:

            if normalize_text(record.category) == "transport":
                matched.append(record)

    elif intent == "placement":

        for record in records:

            if normalize_text(record.category) == "placement":
                matched.append(record)

    elif intent == "admission":

        for record in records:

            if normalize_text(record.category) == "admission":
                matched.append(record)

    elif intent == "contact":

        for record in records:

            category = normalize_text(record.category)

            if category in ["contact", "location"]:
                matched.append(record)

    elif intent == "library":

        for record in records:

            if normalize_text(record.category) == "library":
                matched.append(record)

    elif intent == "scholarship":

        for record in records:

            if normalize_text(record.category) == "scholarship":
                matched.append(record)

    elif intent == "infrastructure":

        for record in records:

            category = normalize_text(record.category)

            if category in [
                "infrastructure",
                "facility",
                "canteen",
                "healthcare"
            ]:
                matched.append(record)

    return matched


# ============================================================
# KEYWORD DATABASE SEARCH
# ============================================================

def keyword_database_search(message):

    records = get_all_database_records()

    if not records:
        return []

    query_words = tokenize(message)

    if not query_words:
        return []

    scored = []

    for record in records:

        category = normalize_text(record.category)
        title = normalize_text(record.title)
        content = normalize_text(record.content)

        full_text = f"{category} {title} {content}"

        score = 0

        for word in query_words:

            if word in category:
                score += 10

            if word in title:
                score += 8

            if word in content:
                score += 3

        if score > 0:
            scored.append((score, record))

    scored.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [record for score, record in scored[:8]]


# ============================================================
# DATABASE CONTEXT
# ============================================================

def build_database_context(records):

    if not records:
        return ""

    context_parts = []

    for record in records:

        context_parts.append(
            f"""
CATEGORY: {record.category}

TITLE: {record.title}

INFORMATION:
{record.content}
"""
        )

    return "\n".join(context_parts)


# ============================================================
# DIRECT DATABASE RESPONSE
# ============================================================

def create_database_response(intent, records):

    if not records:
        return None

    # --------------------------------------------------------
    # COURSES
    # --------------------------------------------------------

    if intent == "courses":

        answer = "Kings College of Engineering offers the following programmes:\n\n"

        for record in records:

            answer += f"### {record.title}\n"
            answer += f"{record.content}\n\n"

        return answer.strip()

    # --------------------------------------------------------
    # DEPARTMENTS
    # --------------------------------------------------------

    if intent == "departments":

        answer = "Kings College of Engineering has the following departments:\n\n"

        for record in records:

            answer += f"• {record.title}\n"

        return answer.strip()

    # --------------------------------------------------------
    # GENERAL CATEGORY
    # --------------------------------------------------------

    answer_parts = []

    for record in records:

        answer_parts.append(
            f"### {record.title}\n{record.content}"
        )

    return "\n\n".join(answer_parts)


# ============================================================
# HF AI RESPONSE
# ============================================================

def ask_huggingface(message, context):

    if not client:
        return None

    system_prompt = """
You are NOVA, the official AI knowledge assistant for
Kings College of Engineering.

Your job is to answer questions about KCE.

IMPORTANT RULES:

1. Use ONLY the KCE information provided in the context.
2. Do not invent college information.
3. Do not make up courses, fees, phone numbers, departments,
   facilities or admission details.
4. If the answer is not present in the context, clearly say
   that the information is not available in the KCE knowledge
   database.
5. Keep answers clear and helpful.
6. Use bullet points when listing information.
7. Never claim information that is not provided.
"""

    user_prompt = f"""
KCE INFORMATION:

{context}

USER QUESTION:

{message}

Answer the user's question using only the KCE information above.
"""

    for attempt in range(3):

        try:

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                max_tokens=700,
                temperature=0.2
            )

            if response and response.choices:

                answer = response.choices[0].message.content

                if answer:
                    return answer.strip()

        except Exception as e:

            print(
                f"Hugging Face attempt {attempt + 1} failed:",
                e
            )

            time.sleep(1)

    return None


# ============================================================
# MAIN CHATBOT FUNCTION
# ============================================================

def get_bot_response(message, history=None):

    if not message:
        return "Please type your question."

    message = message.strip()

    if not message:
        return "Please type your question."

    print("\nUSER:", message)

    # --------------------------------------------------------
    # 1. Detect direct intent
    # --------------------------------------------------------

    intent = detect_intent(message)

    print("DETECTED INTENT:", intent)

    # --------------------------------------------------------
    # 2. Direct database retrieval
    # --------------------------------------------------------

    if intent:

        records = get_intent_records(intent)

        print(
            "INTENT RECORDS:",
            len(records)
        )

        if records:

            # For important factual queries, directly use DB.
            direct_answer = create_database_response(
                intent,
                records
            )

            if direct_answer:
                print("DATABASE RESPONSE USED")

                return direct_answer

    # --------------------------------------------------------
    # 3. Keyword fallback
    # --------------------------------------------------------

    records = keyword_database_search(message)

    print(
        "KEYWORD RECORDS:",
        len(records)
    )

    if records:

        context = build_database_context(records)

        # Try AI for natural answer
        ai_answer = ask_huggingface(
            message,
            context
        )

        if ai_answer:
            return ai_answer

        # AI unavailable → database answer
        return create_database_response(
            None,
            records
        )

    # --------------------------------------------------------
    # 4. No database information
    # --------------------------------------------------------

    return (
        "I couldn't find that information in the KCE "
        "knowledge database."
    )


# ============================================================
# BACKGROUND INDEX COMPATIBILITY
# ============================================================

def start_background_index():

    print("KCE database search is ready.")

    return True