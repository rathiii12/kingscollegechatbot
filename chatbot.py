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
# COURSE SEAT / INTAKE INFORMATION
# ============================================================

SEAT_INFO = {
    "cse": 120,
    "ece": 120,
    "eee": 60,
    "mechanical": 60,
    "civil": 30,
    "ai&ds": 60,
    "it": 30,
    "mba": 60,
    "me cse": 9,
    "me power electronics and drives": 9,
    "me thermal engineering": 9,
    "me vlsi design": 9,
}

SEAT_INFO_TEXT = """CURRENT COURSE INTAKE / SEATS:

UG PROGRAMMES:
• B.E. Computer Science and Engineering (CSE) – 120 seats
• B.E. Electronics and Communication Engineering (ECE) – 120 seats
• B.E. Electrical and Electronics Engineering (EEE) – 60 seats
• B.E. Mechanical Engineering – 60 seats
• B.E. Civil Engineering – 30 seats
• B.Tech Artificial Intelligence and Data Science (AI & DS) – 60 seats
• B.Tech Information Technology (IT) – 30 seats

PG PROGRAMMES:
• M.B.A – 60 seats
• M.E. Computer Science and Engineering – 9 seats
• M.E. Power Electronics and Drives – 9 seats
• M.E. Thermal Engineering – 9 seats
• M.E. VLSI Design – 9 seats"""


# ============================================================
# HOD INFORMATION
# ============================================================

HOD_INFO = """
DEPARTMENT HODS:

CSE:
Dr. S. M. Uma

AI & Data Science:
Dr. S. M. Uma

Information Technology:
Dr. S. M. Uma

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
# COLLEGE LEADERSHIP
# ============================================================

LEADERSHIP_INFO = """
KCE COLLEGE LEADERSHIP:

SECRETARY:
Dr. R. Rajendran

PRINCIPAL:
Dr. J. Arputha Vijaya Selvi

VICE PRINCIPAL:
Dr. S. Sivakumar
"""

# ============================================================
# TNEA INFORMATION
# ============================================================

TNEA_INFO = """
TNEA INFORMATION:

Kings College of Engineering (KCE) TNEA Counselling Code:
3905
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
# LABORATORIES / COLLEGE FACILITIES / RULES
# ============================================================

LAB_INFO = """
LABORATORY INFORMATION:

KCE has department laboratories and practical learning facilities for UG and PG programmes.

Examples from the current KCE department information include:
- Advanced Programming Lab
- DBMS & RDBMS Lab
- Conventional Programming Lab
- Unix Lab
- Multimedia & Image Processing Lab
- UI/UX Lab
- Peripherals & Interfacing Lab
- Hardware Maintenance Lab
- Software Development Lab
- Cloud Computing Lab
- Internet Security Lab

Civil Engineering also has laboratories such as:
- Strength of Materials Lab
- Fluid Mechanics & Machinery Lab
- Soil Mechanics Lab
- Surveying Lab
- Concrete and Highway Engineering Lab
- Environmental Engineering Lab
- Computer Aided Design Lab

Laboratory facilities can vary by department.
"""

COLLEGE_FACILITIES_INFO = """
COLLEGE FACILITIES:

KCE provides a range of academic and campus facilities, including:
- Department laboratories and practical learning facilities
- Library and digital learning resources
- Classrooms and ICT-enabled learning spaces
- Hostel facilities
- College bus transportation
- Canteen and food/mess facilities
- Health-care/medical facilities
- Sports and recreation facilities
- Research and development facilities

For a specific facility, ask about the library, labs, hostel, bus, canteen, health centre, sports, or other campus facilities.
"""

KCE_RULES_INFO = """
KCE RULES:

1. Mobile phones are strictly not allowed for use on campus. If used, they may be confiscated.
2. Students must wear the prescribed lab coat during laboratory sessions.
3. Girls must pin both sides of the shawl properly.
4. Boys should wear formal dress.
5. Leggings are not allowed.
6. Boys should maintain a neat haircut.
7. Girls should keep their hair properly tied.
8. Boys should be clean-shaven.
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
    Retrieve KCE information relevant to the user's question.

    This function NEVER writes the final answer. It only selects
    useful KCE source material and passes it to Hugging Face.
    """
    q = _question_text(question)

    sections = [
        ("KCE BASIC INFORMATION", KCE_BASIC_INFO),
        ("COURSES", COURSE_INFO),
        ("SEATS / INTAKE", SEAT_INFO_TEXT),
        ("HOD INFORMATION", HOD_INFO),
        ("FACULTY INFORMATION", FACULTY_INFO),
        ("COLLEGE LEADERSHIP", LEADERSHIP_INFO),
        ("TNEA INFORMATION", TNEA_INFO),
        ("HOSTEL INFORMATION", HOSTEL_INFO),
        ("FEES AND SCHOLARSHIPS", FEE_INFO),
        ("BUS INFORMATION", BUS_INFO),
        ("PLACEMENT INFORMATION", PLACEMENT_INFO),
        ("FACILITIES", FACILITY_INFO),
        ("LABORATORIES", LAB_INFO),
        ("COLLEGE FACILITIES", COLLEGE_FACILITIES_INFO),
        ("COLLEGE RULES", KCE_RULES_INFO),
    ]

    # Small semantic/keyword retrieval layer. The selected material is
    # still sent to Hugging Face, which understands the user's intent
    # and generates the final response.
    aliases = {
        "hostel": ["hostel", "accommodation", "stay", "dorm"],
        "location": ["located", "location", "where", "address", "place"],
        "seat": ["seat", "seats", "intake", "strength", "students"],
        "hod": ["hod", "head", "department head"],
        "faculty": ["faculty", "professor", "staff", "teacher"],
        "bus": ["bus", "transport", "route", "travel"],
        "lab": ["lab", "labs", "laboratory", "laboratories"],
        "facility": ["facility", "facilities", "campus", "amenities"],
        "rule": ["rule", "rules", "dress", "mobile", "attendance"],
        "fee": ["fee", "fees", "cost", "tuition", "price"],
        "scholarship": ["scholarship", "cutoff", "first graduate", "reservation"],
        "admission": ["admission", "apply", "eligibility", "document", "counselling", "tnea"],
        "placement": ["placement", "career", "recruiter", "salary", "training"],
        "course": ["course", "courses", "programme", "program", "department"],
        "canteen": ["canteen", "food", "mess"],
    }

    scores = []
    def _knowledge_text(value):
        # Retrieval sections can be strings, dictionaries, lists or tuples.
        # Convert everything safely to searchable text so the AI path never
        # crashes just because one KCE data section is structured data.
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            parts = []
            for key, item in value.items():
                parts.append(str(key))
                parts.append(_knowledge_text(item))
            return "\n".join(parts)
        if isinstance(value, (list, tuple, set)):
            return "\n".join(_knowledge_text(item) for item in value)
        return str(value)

    for title, content in sections:
        content_text = _knowledge_text(content)
        text = (title + " " + content_text).lower()
        score = 0
        for group, words in aliases.items():
            if any(w in q for w in words) and any(w in text for w in words):
                score += 3
        # Direct meaningful words from the question also help.
        for word in re.findall(r"[a-z0-9&]+", q):
            if len(word) >= 3 and word in text:
                score += 1
        scores.append((score, title, content_text))

    scores.sort(key=lambda x: x[0], reverse=True)

    # Always include basic college information. Then include the best
    # matching sections. This keeps the model grounded without making
    # it depend on exact predefined questions.
    selected = []
    basic = next((x for x in scores if x[1] == "KCE BASIC INFORMATION"), None)
    if basic:
        selected.append(basic)

    for item in scores:
        if item in selected:
            continue
        if item[0] > 0 and len(selected) < 8:
            selected.append(item)

    # If retrieval has no lexical signal, give Hugging Face a broad but
    # bounded KCE context so it can still understand natural questions.
    if len(selected) == 1:
        selected.extend(scores[1:7])

    all_knowledge = [
        "\n".join(f"[{title}]\n{content}" for _, title, content in selected)
    ]

    knowledge_file = read_knowledge_file()
    if knowledge_file:
        all_knowledge.append("\nKCE KNOWLEDGE FILE:\n" + knowledge_file)

    database = read_database()
    if database:
        all_knowledge.append("\nKCE DATABASE:\n" + database)

    complete = "\n\n".join(all_knowledge)
    return complete[:60000]


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
# DEPARTMENT FACULTY INFORMATION
# ============================================================

FACULTY_INFO = {
    "cse": [
        "Dr. S. M. Uma", "Dr. K. Abhirami", "Dr. S. Rajarajan",
        "Dr. S. Kannan", "Mr. M. Arun", "Ms. S. Priyadharshini",
        "Ms. N. Dhamayandhi", "Ms. B. Bavithra", "Ms. S. Abikayil Aarthi",
        "Ms. M. Kavitha", "Ms. R. Abinaya", "Ms. K. Saranya",
        "Ms. K. Srividhya", "Ms. K. Pappathi", "Mr. S. Balakrishnan",
        "Ms. A. Shanthi", "Ms. K. Suganthi", "Ms. R. Aruna",
        "Mr. P. Balamurugan", "Mrs. K. Madhumitha", "Ms. D. Parkavi"
    ],
    "ai&ds": [
        "Dr. S. M. Uma", "Ms. B. Sangeetha", "Ms. M. Vidhya",
        "Ms. V. Gayathri", "Ms. T. Sindhu", "Mr. D. Rajkumar",
        "Mrs. A. Amirthavalli", "Ms. Y. Vahidhabanu", "Ms. R. Shamini",
        "Ms. J. Akila"
    ],
    "it": [
        "Dr. S. M. Uma", "Ms. B. Sangeetha", "Ms. M. Vidhya",
        "Ms. S. Nirmala", "Ms. V. Gayathri", "Ms. T. Sindhu"
    ],
    "ece": [
        "Dr. J. Arputha Vijaya Selvi", "Ms. N. Mangaiyarkarasi",
        "Mr. K. Sudarsanan", "Mr. S. Ramarajan", "Mr. R. Sathyaraj",
        "Ms. U. Jeyamalar", "Ms. D. Vennila", "Mr. R. Balakrishnan",
        "Mr. R. Thandayuthapani", "Ms. M. Muthulakshmi", "Dr. A. Herald",
        "Ms. R. Brindha", "Ms. N. Karthiga", "Ms. P. Yamunarani",
        "Ms. J. Janani", "Dr. P. Malathi", "Ms. E. Priyadharshini",
        "Ms. D. Abinaya", "Mr. B. Reuben"
    ],
    "eee": [
        "Dr. S. Sivakumar", "Dr. A. Albert Martin Ruban", "Mr. R. Sundaramoorthi",
        "Dr. P. Narasimman", "Mr. J. Arokiaraj", "Mr. S. R. Karthikeyan",
        "Mrs. P. Thirumagal", "Dr. G. Suganya", "Dr. L. Maheswari",
        "Mrs. N. Mangaleswari", "Mr. G. Jayachandran", "Mrs. S. Swathika",
        "Mrs. I. Priyadharshini", "Mr. G. Rathinasamy"
    ],
    "mechanical": [
        "Dr. T. Pushparaj", "Dr. P. P. Shantharaman", "Dr. R. Shankar",
        "Dr. H. Agilan", "Dr. N. Magesh", "Dr. M. Melwin Jagadeesh Sridhar",
        "Mr. M. Sakthivel", "Mr. S. Nelson Raja", "Mr. V. Aravind",
        "Mr. M. Vivekananthan", "Dr. R. Ranjithkumar", "Mr. M. Saravanan",
        "Mr. B. Jothiramalingam"
    ],
    "civil": [
        "Dr. R. Saravanan", "Mr. R. Sundharam", "Mr. K. Arun",
        "Mr. S. Kamaraj", "Mr. D. Nandakumar", "Mr. A. Sagaya Albert",
        "Mr. K. Sri Ram Gopal", "Ms. R. Umamaheswari", "Ms. K. Kalpana",
        "Mr. R. Natarajan"
    ],
    "science & humanities": [
        "Dr. V. Sureshkumar", "Dr. S. Udayakuamar", "Dr. P. Saravanan",
        "Mrs. S. Thiripura Salini", "Mr. G. Thirunavukkarasu",
        "Mrs. C. Annice Vency", "Mrs. K. Bhuvanishankari", "Dr. G. Manivannan",
        "Mrs. T. Gnanajeya", "Dr. S. Geetha", "Dr. G. Shankara Kalidoss",
        "Dr. G. Jeyakrishnan", "Mr. G. Vengatesan", "Dr. S. Rukmani",
        "Ms. S. Sujitha", "Mrs. S. Anuradha", "Mr. S. Ambalatharasu",
        "Dr. K. Sooryakala"
    ]
}

DEPARTMENT_NAMES = {
    "cse": "Computer Science and Engineering (CSE)",
    "ai&ds": "Artificial Intelligence and Data Science (AI & DS)",
    "it": "Information Technology (IT)",
    "ece": "Electronics and Communication Engineering (ECE)",
    "eee": "Electrical and Electronics Engineering (EEE)",
    "mechanical": "Mechanical Engineering",
    "civil": "Civil Engineering",
    "science & humanities": "Science and Humanities (S&H)"
}

HOD_BY_DEPT = {
    "cse": "Dr. S. M. Uma",
    "ai&ds": "Dr. S. M. Uma",
    "it": "Dr. S. M. Uma",
    "ece": "Mrs. N. Mangaiyakarasi",
    "eee": "Mr. R. Sudaramoorthi",
    "mechanical": "Dr. T. Pushparaj",
    "civil": "Dr. R. Saravanan",
    "science & humanities": "Dr. V. Sureshkumar"
}


# ============================================================
# INTENT / DIRECT ANSWER HANDLER
# ============================================================

def _question_text(q):
    return re.sub(r"[^a-z0-9&+ ]+", " ", q.lower()).strip()


def _detect_department(q):
    q = _question_text(q)
    if re.search(r"\bcse\b|computer science", q):
        return "cse"
    if re.search(r"ai\s*(?:&|and)?\s*ds|artificial intelligence|data science", q):
        return "ai&ds"
    if re.search(r"\bit\b|information technology", q):
        return "it"
    if re.search(r"\bece\b|electronics and communication", q):
        return "ece"
    if re.search(r"\beee\b|electrical and electronics", q):
        return "eee"
    if "mechanical" in q:
        return "mechanical"
    if "civil" in q:
        return "civil"
    if re.search(r"s&h|science and humanities|science humanities", q):
        return "science & humanities"
    return None


def _is_faculty_query(q):
    q = _question_text(q)
    return bool(re.search(r"faculty|faculties|staff|teaching staff|teachers|who teaches|faculty members", q))


def _format_faculty(dept, language):
    names = FACULTY_INFO[dept]
    title = DEPARTMENT_NAMES[dept]
    if language == "Tamil":
        intro = f"{title} துறையின் faculty members:"
    elif language == "Tanglish":
        intro = f"{title} department-oda faculty members:"
    else:
        intro = f"The faculty members of the {title} department are:"
    return intro + "\n\n" + "\n".join(f"{i}. {name}" for i, name in enumerate(names, 1))


def _direct_intent_answer(question):
    q = _question_text(question)
    language = detect_language(question)
    dept = _detect_department(question)

    # Normalize common typos/short forms before intent matching.
    q = (q.replace("bsu", "bus")
           .replace("hostal", "hostel")
           .replace("hoste", "hostel")
           .replace("scholership", "scholarship"))

    # --------------------------------------------------------
    # ALL HOD NAMES — broad natural-language matching
    # --------------------------------------------------------
    if (re.search(r"\bhods?\b|head(?:s)? of (?:the )?department|department heads?", q)
            and not dept):
        lines = ["The Heads of Departments (HODs) at KCE are:"]
        for d, name in HOD_BY_DEPT.items():
            lines.append(f"• {DEPARTMENT_NAMES[d]} — {name}")
        return "\n".join(lines)

    # --------------------------------------------------------
    # Faculty
    # --------------------------------------------------------
    if _is_faculty_query(q):
        if dept:
            return _format_faculty(dept, language)
        return "\n\n---\n\n".join(_format_faculty(d, language) for d in FACULTY_INFO)

    # --------------------------------------------------------
    # Individual HOD
    # --------------------------------------------------------
    if dept and re.search(r"\bhod\b|head of department|department head|in charge", q):
        name = HOD_BY_DEPT[dept]
        if language == "Tanglish":
            return f"{DEPARTMENT_NAMES[dept]} department-oda HOD {name}."
        if language == "Tamil":
            return f"{DEPARTMENT_NAMES[dept]} துறையின் HOD {name}."
        return f"The HOD of the {DEPARTMENT_NAMES[dept]} department is {name}."

    # --------------------------------------------------------
    # COURSE SEATS / INTAKE
    # --------------------------------------------------------
    seat_query = re.search(
        r"\bseat\b|\bseats\b|intake|student strength|how many students|evlo seats|evlo student",
        q
    )
    if seat_query:
        # Specific department/course seat query first.
        if dept and dept in SEAT_INFO:
            seats = SEAT_INFO[dept]
            course_name = {
                "cse": "B.E. Computer Science and Engineering",
                "ai&ds": "B.Tech Artificial Intelligence and Data Science",
                "it": "B.Tech Information Technology",
                "ece": "B.E. Electronics and Communication Engineering",
                "eee": "B.E. Electrical and Electronics Engineering",
                "mechanical": "B.E. Mechanical Engineering",
                "civil": "B.E. Civil Engineering",
            }[dept]
            if language == "Tanglish":
                return f"{course_name}-ku current intake {seats} seats."
            if language == "Tamil":
                return f"{course_name} பாடப்பிரிவில் தற்போதைய intake {seats} seats."
            return f"The current intake for {course_name} is {seats} seats."

        # Specific PG course names.
        pg_matches = [
            (r"m\.?b\.?a|mba", "M.B.A", 60),
            (r"m\.?e\.?\s*cse|m\.?e\.?\s*computer science", "M.E. Computer Science and Engineering", 9),
            (r"power electronics|m\.?e\.?\s*power", "M.E. Power Electronics and Drives", 9),
            (r"thermal engineering|m\.?e\.?\s*thermal", "M.E. Thermal Engineering", 9),
            (r"vlsi design|m\.?e\.?\s*vlsi", "M.E. VLSI Design", 9),
        ]
        for pattern, course_name, seats in pg_matches:
            if re.search(pattern, q):
                if language == "Tanglish":
                    return f"{course_name}-ku current intake {seats} seats."
                if language == "Tamil":
                    return f"{course_name} பாடப்பிரிவில் தற்போதைய intake {seats} seats."
                return f"The current intake for {course_name} is {seats} seats."

        # Broad question: all course seats.
        return SEAT_INFO_TEXT.strip()

    # --------------------------------------------------------
    # Department overview
    # --------------------------------------------------------
    if dept and re.search(r"tell me about|about|details|information|department|dept|offer|offers|what is", q):
        programme = {
            "cse": "B.E. Computer Science and Engineering",
            "ai&ds": "B.Tech. Artificial Intelligence and Data Science",
            "it": "B.Tech. Information Technology",
            "ece": "B.E. Electronics and Communication Engineering",
            "eee": "B.E. Electrical and Electronics Engineering",
            "mechanical": "B.E. Mechanical Engineering",
            "civil": "B.E. Civil Engineering",
            "science & humanities": "Science and Humanities"
        }[dept]
        if language == "Tanglish":
            return f"{DEPARTMENT_NAMES[dept]} KCE-la {programme} programme-ai offer pannudhu. HOD: {HOD_BY_DEPT[dept]}. Faculty details venumna kekkalaam."
        if language == "Tamil":
            return f"{DEPARTMENT_NAMES[dept]} துறை KCE-ல் {programme} பாடத்திட்டத்தை வழங்குகிறது. HOD: {HOD_BY_DEPT[dept]}. Faculty பெயர்களையும் கேட்கலாம்."
        return f"The {DEPARTMENT_NAMES[dept]} department at KCE offers {programme}. The HOD is {HOD_BY_DEPT[dept]}. You can also ask for the department's faculty names."

    # --------------------------------------------------------
    # Leadership
    # --------------------------------------------------------
    if "principal" in q and "vice" not in q:
        return "The Principal of Kings College of Engineering is Dr. J. Arputha Vijaya Selvi."
    if re.search(r"vice principal|\bvp\b", q):
        return "The Vice Principal of Kings College of Engineering is Dr. S. Sivakumar."
    if "secretary" in q:
        return "The Secretary of Kings College of Engineering is Dr. R. Rajendran."

    # --------------------------------------------------------
    # TNEA
    # --------------------------------------------------------
    if re.search(r"\btnea\b|counselling code|counseling code|admission code|tnea number", q):
        return "The TNEA Counselling Code of Kings College of Engineering is 3905."

    # --------------------------------------------------------
    # BUS — route questions first, then general availability/free
    # --------------------------------------------------------
    bus_q = re.search(r"\bbus\b|\bbuses\b|transport|vehicle|van", q)
    route_q = re.search(r"\broute\b|\broutes\b|route number|bus number|bus no|all routes|route list", q)
    if bus_q and route_q:
        specific = re.search(r"(?:bus\s*(?:no\.?\s*)?|route\s*(?:no\.?\s*)?)(n[1-4]|q-?9|[1-9]|1[0-8])\b", q)
        if not specific:
            specific = re.search(r"\b(van[- ]?[ab])\b", q)
        if specific:
            wanted = specific.group(1).replace(" ", "").lower()
            for block in re.split(r"\n\s*\n", BUS_INFO.strip()):
                first = block.splitlines()[0].lower().replace(" ", "")
                if wanted in first:
                    return block.strip()
        return BUS_INFO.strip()

    if "bus" in q or "transport" in q or "van" in q:
        if re.search(r"free|fee|cost|charge|provides?|provide|available|have|service|iruka|irukku|college.*bus", q):
            return "Yes. KCE provides college bus transportation. The bus service is Free for the available college routes."

    # --------------------------------------------------------
    # HOSTEL FEE — before general fee
    # --------------------------------------------------------
    if "hostel" in q and re.search(r"fee|fees|cost|price|amount|charge|evlo", q):
        if re.search(r"7\.5|reservation", q):
            return "Students eligible under the 7.5% reservation receive Free hostel/education benefits as applicable."
        return "The KCE hostel fee is ₹50,000 per year. Students eligible under the 7.5% reservation receive Free hostel/education benefits as applicable."

    # Hostel facilities
    if re.search(r"hostel", q) and re.search(r"facility|facilities|available|provide|offers?|have|there|exist|is there|does|do|iruka|irukku", q):
        return HOSTEL_INFO.strip()

    # --------------------------------------------------------
    # Admission documents / eligibility before broad admission
    # --------------------------------------------------------
    if re.search(r"document|documents|certificate|certificates", q):
        return ("For KCE admission, commonly required documents include academic certificates, "
                "transfer certificate, community certificate if applicable, identification proof, "
                "photographs, and other current admission-specific documents. The exact list can vary "
                "by programme and category.")

    if re.search(r"eligib|eligibilty|qualification|qualify|criteria|who can apply|minimum mark", q):
        return ("KCE admission eligibility depends on the programme and applicable admission route. "
                "Please check the current programme-specific eligibility requirements before applying.")

    # Admission process
    if re.search(r"admission process|admission procedure|how.*(admission|apply)|how to apply|admission steps?|apply.*kce|join.*kce", q):
        return ("KCE admission procedure:\n\n"
                "1. Choose the desired KCE programme.\n"
                "2. Check the applicable eligibility requirements.\n"
                "3. Apply through the applicable admission route.\n"
                "4. Complete the counselling/admission process and submit the required documents.\n"
                "5. Pay the applicable admission fee and confirm the seat.\n\n"
                "Main admission routes:\n"
                "• TNEA Counselling – ₹80,000; TNEA code: 3905\n"
                "• Management Admission / Management Counselling – ₹1,10,000\n\n"
                "Admission contact: +91-6380989024")

    # Scholarships
    if re.search(r"scholarship|scholarships|fee waiver|fee reduction|financial aid|sports scholarship|first graduate|7\.5|cutoff.*fee|fee.*cutoff", q):
        return ("KCE scholarship and fee benefits include:\n"
                "• Sports scholarship\n"
                "• First Graduate benefit\n"
                "• 7.5% reservation – Free education as applicable\n"
                "• 160+ cutoff – ₹10,000 fee reduction\n"
                "• 170+ cutoff – ₹15,000 fee reduction\n"
                "• 180+ cutoff – ₹20,000 fee reduction\n"
                "• 190+ cutoff – Free education as per the provided information")

    # General fee
    if re.search(r"\bfee\b|\bfees\b|tuition fee|college fee|management fee", q):
        return FEE_INFO.split("SCHOLARSHIP / FEE BENEFITS:", 1)[0].strip()

    # Rules — return the actual rules, not only the heading.
    if re.search(r"\brules?\b|dress code|discipline|mobile phone|phone allowed|rule of kce|rules of kce", q):
        return KCE_RULES_INFO.strip()

    # Laboratories / labs
    if re.search(r"\blabs?\b|laborator(?:y|ies)|laboratory|practical lab|lab facilities", q):
        return LAB_INFO.strip()

    # Broad college facilities
    if re.search(r"college facilities|campus facilities|facilities in kce|facilities available|what facilities|facilities does kce|facility of kce", q):
        return COLLEGE_FACILITIES_INFO.strip()

    # Basic facts
    if re.search(r"attendance|minimum.*percent", q):
        return "The minimum attendance requirement at KCE is 75%."
    if re.search(r"college.*tim(e|ing)|tim(e|ing).*college|start.*college|end.*college", q):
        return "KCE college timing is 9:15 AM to 4:30 PM."
    if re.search(r"where.*college|college.*where|location|address|located|where is kce|where.*kce|enga.*iruk", q):
        return "Kings College of Engineering is located at Punalkulam, Near Thanjavur, Gandarvakottai Taluk, Pudukkottai District – 613303, Tamil Nadu, India."
    if re.search(r"phone|contact number|mobile number|admission contact", q):
        return "KCE contact number is +91-6380989024."
    if re.search(r"email|mail id|email id", q):
        return "KCE email address is contact@kingsengg.edu.in."
    if re.search(r"website|official site|official website", q):
        return "The official KCE website is www.kingsengg.edu.in."
    if re.search(r"full name|what is kce|kce stand|college name", q):
        return "KCE stands for Kings College of Engineering."
    if re.search(r"founded|established|when.*started", q):
        return "Kings College of Engineering was established in 2001."
    if re.search(r"autonomous|deemed", q):
        return "KCE is an autonomous engineering institution affiliated to Anna University, Chennai. It is not a deemed university."
    if re.search(r"anna university|affiliated", q):
        return "Yes. Kings College of Engineering is affiliated to Anna University, Chennai."
    if re.search(r"aicte|approved by", q):
        return "Yes. Kings College of Engineering is approved by AICTE, New Delhi."
    if re.search(r"naac|accredit", q):
        return "Yes. Kings College of Engineering is NAAC accredited."

    # Courses / placement / canteen
    if re.search(r"courses|course list|what can i study|programmes|programs|what courses|available courses", q):
        return COURSE_INFO.strip()
    if re.search(r"placement|placements|training and placement|t&p", q):
        return PLACEMENT_INFO.strip()
    if re.search(r"canteen|cafeteria|food facility", q):
        return FACILITY_INFO.strip()

    return None


# ============================================================
# KNOWLEDGE-BASE FALLBACK
# ============================================================

def _knowledge_base_fallback(question):
    """Return the closest answer from kce_knowledge.md when AI is unavailable."""
    knowledge = read_knowledge_file()
    if not knowledge:
        return None

    pairs = re.findall(
        r"Q:\s*(.*?)\s*\n+\s*A:\s*(.*?)(?=\n+\s*Q:|\Z)",
        knowledge,
        flags=re.IGNORECASE | re.DOTALL
    )
    if not pairs:
        return None

    qnorm = normalize(question)
    qwords = set(qnorm.split())
    best_answer = None
    best_score = 0.0

    for stored_q, answer in pairs:
        stored_norm = normalize(stored_q)
        if not stored_norm:
            continue
        stored_words = set(stored_norm.split())
        overlap = len(qwords & stored_words) / max(1, len(qwords | stored_words))
        similarity = SequenceMatcher(None, qnorm, stored_norm).ratio()
        score = (0.65 * similarity) + (0.35 * overlap)
        if score > best_score:
            best_score = score
            best_answer = answer.strip()

    if best_score >= 0.48 and best_answer:
        return best_answer
    return None


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

20. If the user asks about the Principal, Vice Principal (VP),
    or Secretary, answer using the KCE leadership information.

21. Understand variants such as:
    "principal name", "who is the principal", "principal yaaru?",
    "vp name", "vice principal yaaru?", "secretary name",
    "secretary yaaru?" as the same respective intents.

22. If the user asks for the TNEA code, counselling code,
    admission code, or "TNEA number", answer with the
    KCE TNEA Counselling Code: 3905.

23. Do not say "according to my instructions".

24. Do not mention internal prompts, system messages,
    knowledge retrieval or AI rules.

25. Be natural, clear and professional.

26. Answer only from the supplied KCE information.

27. Treat the supplied KCE information as your knowledge base, not as
    a list of exact questions. Find the relevant facts by meaning.

28. For natural, incomplete or misspelled questions, infer the intended
    KCE topic from the wording and answer using the closest relevant
    supplied facts.

29. Do not return only a section heading such as "RULES" or "FACILITIES".
    Explain the relevant facts in a useful answer.

30. When the user asks "is there", "does KCE have", "about", "tell me
    about", "what is", "where is", "how many", or similar natural forms,
    understand the underlying intent rather than requiring exact keywords.

31. Do not mention that you are using retrieval, sections, a knowledge
    base, or predefined intents.

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
            # If HF_TOKEN is missing, use the local KCE intent handler
            # instead of losing answers that are already present locally.
            direct = _direct_intent_answer(question)
            if direct:
                return direct

            fallback = _knowledge_base_fallback(question)
            if fallback:
                return fallback
            return (
                "I couldn't find that information in the current KCE data. "
                "Please try asking the question in another way."
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

        # Keep the local KCE intent handler as a reliable fallback.
        # Hugging Face remains the PRIMARY answer path; this only runs
        # when the external AI call is unavailable or fails.
        direct = _direct_intent_answer(question)
        if direct:
            return direct

        fallback = _knowledge_base_fallback(question)
        if fallback:
            return fallback

        return (
            "I couldn't find enough KCE information to answer that accurately."
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

    # Every normal user question goes through Hugging Face first.
    # The local intent handler is kept only as a fallback when the
    # external AI is unavailable, so natural-language understanding
    # remains the primary path.
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