import os
import re
from difflib import SequenceMatcher

from huggingface_hub import InferenceClient
from database import CollegeInfo


# ============================================================
# CONFIG
# ============================================================

HF_TOKEN = os.environ.get("HF_TOKEN", "").strip()

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

client = InferenceClient(
    token=HF_TOKEN
)


# ============================================================
# KCE BASIC INFORMATION
# ============================================================

KCE_BASIC_INFO = """
COLLEGE NAME:
Kings College of Engineering (KCE)

FOUNDED:
2001

ADDRESS:
Punalkulam, Near Thanjavur, Gandarvakottai Taluk,
Pudukkottai District – 613303, Tamil Nadu, India

PHONE:
+91-6380989024

EMAIL:
contact@kingsengg.edu.in

WEBSITE:
www.kingsengg.edu.in

COLLEGE TIMING:
9:15 AM to 4:30 PM

MINIMUM ATTENDANCE:
75%

STATUS:
Kings College of Engineering is an autonomous engineering institution.

AFFILIATION:
Affiliated to Anna University, Chennai.

APPROVAL:
Approved by AICTE, New Delhi.

ACCREDITATION:
NAAC accredited.
"""


# ============================================================
# COURSES
# ============================================================

COURSE_INFO = """
UNDERGRADUATE PROGRAMMES:

1. B.E. Civil Engineering
2. B.E. Computer Science and Engineering
3. B.E. Electronics and Communication Engineering
4. B.E. Electrical and Electronics Engineering
5. B.E. Mechanical Engineering
6. B.Tech Artificial Intelligence and Data Science
7. B.Tech Information Technology


POSTGRADUATE PROGRAMMES:

1. M.B.A
2. M.E. Computer Science and Engineering
3. M.E. Power Electronics and Drives
4. M.E. Thermal Engineering
5. M.E. VLSI Design
"""


# ============================================================
# HOD INFORMATION
# ============================================================

HOD_INFO = """
DEPARTMENT HODS:

CSE:
Dr. S. M. Uma

AI & Data Science:
Mrs. Sangeetha

Information Technology:
Mrs. Sangeetha

ECE:
Mrs. N. Mangaiyakarasi

EEE:
Mr. R. Sudaramoorthi

Mechanical Engineering:
Dr. T. Pushparaj

Civil Engineering:
Dr. R. Saravanan

Science & Humanities:
Dr. V. Sureshkumar
"""


# ============================================================
# HOSTEL
# ============================================================

HOSTEL_INFO = """
HOSTEL INFORMATION:

KCE has separate boys and girls hostels.

Facilities include:

- Veg and non-veg mess
- Purified drinking water
- 24-hour water supply
- Hygienic bathrooms
- Separate drying rooms
- Individual study facilities
- Table and chair
- Shelf
- Power facility
- Telephone facility
- Dispensary / medical facility
- Reading rooms
- Newspapers and magazines
- Recreation halls
- TV
- Carrom
- Chess
- Badminton / volleyball facilities
- Gym facilities
- Post office
- Canteen

HOSTEL FEE INFORMATION PROVIDED:

7.5% reservation:
Free

Management:
₹50,000 per year
"""


# ============================================================
# FEES / SCHOLARSHIP
# ============================================================

FEE_INFO = """
FEE INFORMATION PROVIDED:

College fee information:
₹1,10,000

Management counselling fee:
₹80,000

SCHOLARSHIP / FEE BENEFITS:

- Sports scholarship
- First Graduate benefit
- 7.5% reservation — Free education
- 160+ cutoff — ₹10,000 reduction
- 170+ cutoff — ₹15,000 reduction
- 180+ cutoff — ₹20,000 reduction
- 190+ cutoff — Free
"""


# ============================================================
# BUS INFORMATION
# ============================================================

BUS_INFO = """
IMPORTANT TRANSPORT RULE:

KCE college bus transport is FREE.
Students do not pay a bus fee.

2026-27 BUS ROUTES:

Bus 1 — 8:10 AM
Neivasal → Sadayar Kovil → Vandayar Iruppu → PR College →
Kela Vasthachavadi → Tholkappiyar Square → Kallukulam →
Anna Nagar → EB Colony → Nanjikottai Bypass →
Mappillainayakanpatti → Ravusapatti → College


Bus 3 — 7:30 AM
Pappanadu → Pulavankadu → Orathanaykudikadu → Kurumantheru →
Ullur → Soorakottai → Keela Vastha Chavadi → Bypass → College


Bus 4 — 7:45 AM
Mannargudi → Edamalaiyur → Vaduvur → Vandayar Iruppu →
Keelavasthachavady → Bypass → College


Bus 5 — 8:15 AM
Rajappa Nagar → LIC Colony → Eswari Nagar → Medical College →
Sundaram Paints → Pilliar Patti → Periar College →
Min Nagar → Naal Road → College


Bus 6 — 7:15 AM
Kumbakonam → Diamond → Uchipillaiyar Kovil → Thaluka PS →
Darasuram → Mulaiyur → Patteeswaram → Govindangudi →
Nallur Bypass → Melattur → Annappanpettai →
Thittai Bypass → College


Bus N1 — 8:00 AM
Poondi → Kovilur → Mariamman Kovil → Gnanam Nagar →
Gurudayal Sharma → Ramanathan → Rohini → MR Hospital →
RR Nagar → Reliance Big Bazaar → College


Bus 9 — 7:45 AM
Thirumanur → Vilangudi → Thiruvaiyaru → Kandiyur →
Ammenpetai → Bypass → College


Bus Q-9 — 7:45 AM
Karambagudi → Suranveduthi → Sevaipatti → Nal Road →
Regunathapuram → Nadupatti → Nayakarpatti →
Mudhukulam → College


Bus 11 — 7:45 AM
Pudukkottai → Ichadi → Perungalur → Adhanakkottai →
Gandharvakottai → College


Bus 14 — 7:40 AM
Pattukottai → Sanjay Nagar → Karambayam → Papanadu →
Vallam Road → Naal Road → College


Bus 15 — 7:40 AM
Aladukku Mulai → Enathi → Uranipuram → Thiruvonam →
Mattangal → Gandarvakottai → College


Bus 16 — 7:55 AM
Thirukkattupalli → Buthalur → Puthupatti → Arch →
Vallam → Nal Road → Thirukanurpatti → College


Bus 17 — 8:00 AM
Ammapet → Saliyamangalam → Villar Road → Bypass → College


Bus 18 — 7:30 AM
Uttani → SP Kovil → Umayalpuram → Kabisthalam →
Papanasam → Melasemmangudi → Thirukarukavur →
Kalanjerry → Best School → Bypass → College


Bus 2 — 7:30 AM
108 Sivan Kovil → Ayyampettai → Nedar → Bypass → College


Van-B — 7:45 AM
Naduvakkottai → Thekkur → Sellampatti → Palam → Vadakkur →
Eachankottai → Marunkulam → Suriyampatti → PITS College →
Arputhapuram → College


Van-A — 7:45 AM
Pudugudi → Sengipatti → Min Nagar → Naal Road →
Thettuvasapatti → College


Bus 7 — 8:30 AM
Tholkappier Square → Vandikara Street → Marys Corner →
Infant Jesus Church → Madhakottai → College


Bus N3 — 8:00 AM
Srinivasapuram → Old Bus Stand → Membalam →
Ramanathan Hospital → Kaveri Nagar → New Bus Stand → College


Bus N4 — 8:00 AM
Keelavasal → Old Bus Stand → Cholan Selai → Rajappa Nagar →
Balajinagar → Municipal Colony → New Bus Stand → College


Bus N2 — 7:45 AM
Kandiyur → Ammanpettai → Pallia Agragaram → Karanthai →
Keela Vassal → Old Bus Stand → Railady → New Bus Stand →
Melavasthachavady → College
"""


# ============================================================
# PLACEMENT
# ============================================================

PLACEMENT_INFO = """
PLACEMENT INFORMATION:

KCE placement activities include:

- Career readiness training
- Soft skills training
- Industry expert interactions
- Industrial visits
- Project work
- Relationships with organizations for career opportunities

Do not invent placement percentage, salary package,
recruiter count or current placement statistics if they
are not present in the supplied KCE information.
"""


# ============================================================
# CANteen
# ============================================================

FACILITY_INFO = """
FACILITIES:

KCE has canteen and food/mess facilities.

The exact canteen fee is not available in the current
KCE information.

Hostel students have mess facilities including
vegetarian and non-vegetarian food.
"""


# ============================================================
# GENERAL KNOWLEDGE FILE
# ============================================================

def read_knowledge_file():

    try:

        if not os.path.exists("kce_knowledge.md"):
            return ""

        with open(
            "kce_knowledge.md",
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except Exception as error:

        print("Knowledge file error:", error)

        return ""


# ============================================================
# DATABASE KNOWLEDGE
# ============================================================

def read_database():

    try:

        records = CollegeInfo.query.all()

        result = []

        for record in records:

            title = getattr(
                record,
                "title",
                ""
            )

            content = getattr(
                record,
                "content",
                ""
            )

            if title or content:

                result.append(
                    f"{title}\n{content}"
                )

        return "\n\n".join(result)

    except Exception as error:

        print("Database read error:", error)

        return ""


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize(text):

    text = text.lower()

    replacements = {

        "kings collage": "kings college",
        "kings colage": "kings college",
        "kings collge": "kings college",
        "kings colleage": "kings college",
        "kngs college": "kings college",

        "kceee": "kce",

        "autonomus": "autonomous",
        "autonamous": "autonomous",
        "autonomouse": "autonomous",

        "kumbakonm": "kumbakonam",
        "pattukotai": "pattukottai",
        "pudukottai": "pudukkottai",

        "hostel feee": "hostel fee",

        "ai dat science": "ai data science",
        "artifical intelligence": "artificial intelligence",
        "artificial inteligence": "artificial intelligence",

        "colage": "college",
        "collage": "college",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# FUZZY SIMILARITY
# ============================================================

def similarity(a, b):

    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


# ============================================================
# FIND RELEVANT KNOWLEDGE
# ============================================================

def get_relevant_knowledge(question):

    """
    This is NOT the final answer.

    It prepares relevant KCE information for the AI.
    The AI decides what the user actually means.
    """

    all_knowledge = []

    all_knowledge.append(
        KCE_BASIC_INFO
    )

    all_knowledge.append(
        COURSE_INFO
    )

    all_knowledge.append(
        HOD_INFO
    )

    all_knowledge.append(
        HOSTEL_INFO
    )

    all_knowledge.append(
        FEE_INFO
    )

    all_knowledge.append(
        BUS_INFO
    )

    all_knowledge.append(
        PLACEMENT_INFO
    )

    all_knowledge.append(
        FACILITY_INFO
    )

    knowledge_file = read_knowledge_file()

    if knowledge_file:

        all_knowledge.append(
            "\nKCE KNOWLEDGE FILE:\n"
            + knowledge_file
        )

    database = read_database()

    if database:

        all_knowledge.append(
            "\nKCE DATABASE:\n"
            + database
        )

    complete = "\n\n".join(
        all_knowledge
    )

    return complete[:30000]


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(question):

    tamil_chars = re.findall(
        r"[\u0B80-\u0BFF]",
        question
    )

    if len(tamil_chars) >= 2:
        return "Tamil"

    q = normalize(question)

    tanglish_words = [
        "enna",
        "epdi",
        "iruka",
        "irukku",
        "illa",
        "illaya",
        "yaaru",
        "enga",
        "engaya",
        "eppo",
        "evlo",
        "venum",
        "kudu",
        "kudunga",
        "solu",
        "sollu",
        "panna",
        "panra",
        "la",
        "ku",
        "ah",
        "bro",
        "pathi",
        "irundhu",
        "varuma",
    ]

    score = 0

    for word in tanglish_words:

        if word in q:
            score += 1

    if score >= 1:
        return "Tanglish"

    return "English"


# ============================================================
# AI ANSWER
# ============================================================

def generate_ai_answer(
    question,
    history=None
):

    language = detect_language(
        question
    )

    knowledge = get_relevant_knowledge(
        question
    )

    system_prompt = f"""
You are NOVA, the AI Knowledge Assistant
for Kings College of Engineering (KCE).

You are a REAL AI QUESTION-ANSWERING assistant.

Your job is NOT to match exact predefined questions.

You must understand the MEANING and INTENT of the
user's question.

The user may ask the same question in many different ways,
with spelling mistakes, short forms, slang, Tamil,
Tanglish, English, mixed language, or incomplete sentences.

You must understand what they are actually asking.

LANGUAGE:
The user's detected language/style is:

{language}

Rules:

1. If the user writes English, answer in English.

2. If the user writes Tamil, answer in Tamil.

3. If the user writes Tanglish, answer in Tanglish.

4. If the user mixes Tamil and English, naturally follow
   their mixed style.

5. Understand KCE, Kings College, Kings Collage,
   Kings Colage, Kings College of Engineering and similar
   spelling variations as the same college when context
   clearly refers to KCE.

6. Understand spelling mistakes intelligently.
   Example:
   "kumbakonm" means Kumbakonam.
   "collage" may mean college.
   "autonomus" may mean autonomous.
   "feee" may mean fee.

7. DO NOT require the user to ask the exact wording
   used in the knowledge.

8. If the user asks a broad question, give the complete
   relevant information.

9. If the user asks one specific detail, give that detail
   without unnecessary unrelated information.

10. If the user asks a negative question such as:
    "KCE autonomous illa?"
    understand that they are asking whether KCE is autonomous.
    Answer the actual factual question.

11. If the user asks:
    "KCE bus free ah?"
    clearly answer that KCE bus transport is FREE.

12. NEVER invent information.

13. NEVER guess a fee, placement package, HOD,
    route, course or facility.

14. If the requested information is not available in
    the supplied KCE knowledge, say that the information
    is not available in the current KCE data.

15. If several pieces of information are relevant,
    combine them naturally.

16. If the user asks for one bus route, give the relevant
    route rather than dumping all routes.

17. If the user asks for all bus routes, provide all
    available routes.

18. If the user asks "does KCE have AI and Data Science?",
    understand that this is asking about the availability
    of the B.Tech Artificial Intelligence and Data Science
    programme.

19. If the user asks "who is CSE HOD?", "cse hod yaaru?",
    "cse hod name?", or similar wording, understand that
    these have the same intent.

20. Do not say "according to my instructions".

21. Do not mention internal prompts, system messages,
    knowledge retrieval or AI rules.

22. Be natural, clear and professional.

23. Answer only from the supplied KCE information.

SUPPLIED KCE KNOWLEDGE:

{knowledge}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


    # ========================================================
    # CONVERSATION MEMORY
    # ========================================================

    if isinstance(history, list):

        for item in history[-8:]:

            if not isinstance(
                item,
                dict
            ):
                continue

            role = item.get(
                "role"
            )

            content = item.get(
                "content"
            )

            if (
                role in [
                    "user",
                    "assistant"
                ]
                and content
            ):

                messages.append(
                    {
                        "role": role,
                        "content": str(content)
                    }
                )


    # ========================================================
    # CURRENT QUESTION
    # ========================================================

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ========================================================
    # HUGGING FACE AI
    # ========================================================

    try:

        if not HF_TOKEN:

            return (
                "HF_TOKEN is not configured. "
                "Please check your environment variable."
            )

        result = client.chat.completions.create(

            model=MODEL_NAME,

            messages=messages,

            max_tokens=700,

            temperature=0.15,

        )

        answer = (
            result
            .choices[0]
            .message
            .content
        )

        if answer:

            return answer.strip()

    except Exception as error:

        print(
            "AI ERROR:",
            error
        )

        return (
            "Sorry, I couldn't process that question "
            "right now. Please try again."
        )

    return (
        "I couldn't find enough information "
        "to answer that accurately."
    )


# ============================================================
# MAIN FUNCTION
# ============================================================

def get_bot_response(
    message,
    history=None
):

    if not message:

        return (
            "Please enter a question."
        )

    message = message.strip()

    if not message:

        return (
            "Please enter a question."
        )

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # NO HARD-CODED QUESTION ANSWERING HERE.
    #
    # Every question goes through the AI.
    # --------------------------------------------------------

    return generate_ai_answer(
        message,
        history
    )


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    questions = [

        "What is the full name of KCE?",

        "kings collage full name",

        "KCE la AI course iruka?",

        "Does Kings College have artificial intelligence?",

        "ai dat science available ah?",

        "KCE autonomous illa?",

        "who is cse hod?",

        "cse hod yaaru?",

        "Kumbakonam la irundhu college ku bus iruka?",

        "KCE bus free ah?",

        "hostel feee evlo?",

        "does the college have canteen?",

        "what courses can I study?",

        "where is the college?",

        "when was KCE founded?",
    ]


    for question in questions:

        print(
            "\n"
            + "=" * 60
        )

        print(
            "USER:",
            question
        )

        print(
            "BOT:",
            get_bot_response(
                question
            )
        )