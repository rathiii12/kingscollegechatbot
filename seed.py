from app import app
from database import db, CollegeInfo


data = [

    # ==========================================
    # ABOUT KCE
    # ==========================================

    {
        "category": "About",
        "title": "About Kings College of Engineering",
        "content": """Kings College of Engineering (KCE) was founded in 2001 by Raj Educational Trust (RET), Chennai.

KCE is approved by the All India Council for Technical Education (AICTE), New Delhi and affiliated to Anna University, Chennai.

The institution is NAAC accredited and has autonomous status.

The college is located at Punalkulam, near Thanjavur, Tamil Nadu."""
    },


    # ==========================================
    # UNDERGRADUATE PROGRAMMES
    # ==========================================

    {
        "category": "Course",
        "title": "Undergraduate Programmes",
        "content": """Kings College of Engineering offers 7 undergraduate programmes:

1. B.E. Civil Engineering - Intake: 30
2. B.E. Computer Science and Engineering - Intake: 120
3. B.E. Electronics and Communication Engineering - Intake: 120
4. B.E. Electrical and Electronics Engineering - Intake: 60
5. B.E. Mechanical Engineering - Intake: 60
6. B.Tech Artificial Intelligence and Data Science - Intake: 60
7. B.Tech Information Technology - Intake: 30"""
    },


    # ==========================================
    # POSTGRADUATE PROGRAMMES
    # ==========================================

    {
        "category": "Course",
        "title": "Postgraduate Programmes",
        "content": """Kings College of Engineering offers the following postgraduate programmes:

1. M.E. VLSI Design
2. M.E. Thermal Engineering
3. M.E. Power Electronics and Drives
4. M.E. Computer Science and Engineering
5. M.B.A. Master of Business Administration

Students should contact the college for current programme intake and admission details."""
    },


    # ==========================================
    # Ph.D PROGRAMMES
    # ==========================================

    {
        "category": "Course",
        "title": "Ph.D Programmes",
        "content": """Kings College of Engineering offers Ph.D research programmes.

Ph.D programmes include:

1. Ph.D. Mechanical Engineering
2. Ph.D. Electronics and Communication Engineering

Students should contact the respective department for current research and admission information."""
    },


    # ==========================================
    # DEPARTMENTS
    # ==========================================

    {
        "category": "Department",
        "title": "Computer Science and Engineering",
        "content": """The Computer Science and Engineering department at Kings College of Engineering focuses on computer science, programming, software development and modern computing technologies.

The department offers B.E. Computer Science and Engineering and M.E. Computer Science and Engineering."""
    },

    {
        "category": "Department",
        "title": "Artificial Intelligence and Data Science",
        "content": """The Artificial Intelligence and Data Science department focuses on artificial intelligence, machine learning, data analytics and intelligent technologies.

The department offers B.Tech Artificial Intelligence and Data Science."""
    },

    {
        "category": "Department",
        "title": "Information Technology",
        "content": """The Information Technology department focuses on information technology, databases, networking, web technologies, cloud computing and modern IT solutions.

The department offers B.Tech Information Technology."""
    },

    {
        "category": "Department",
        "title": "Electronics and Communication Engineering",
        "content": """The Electronics and Communication Engineering department focuses on electronics, communication systems, embedded technologies and digital systems.

The department offers B.E. Electronics and Communication Engineering."""
    },

    {
        "category": "Department",
        "title": "Electrical and Electronics Engineering",
        "content": """The Electrical and Electronics Engineering department focuses on electrical systems, power electronics, automation and related technologies.

The department offers B.E. Electrical and Electronics Engineering."""
    },

    {
        "category": "Department",
        "title": "Mechanical Engineering",
        "content": """The Mechanical Engineering department focuses on mechanical design, manufacturing and engineering systems.

The department offers B.E. Mechanical Engineering and M.E. Thermal Engineering."""
    },

    {
        "category": "Department",
        "title": "Civil Engineering",
        "content": """The Civil Engineering department focuses on construction, structural engineering, infrastructure and related engineering fields.

The department offers B.E. Civil Engineering."""
    },


    # ==========================================
    # DEPARTMENT HOD
    # ==========================================

    {
        "category": "HOD",
        "title": "CSE Department HOD",
        "content": "CSE Department HOD: Dr. S. M. Uma"
    },

    {
        "category": "HOD",
        "title": "AI&DS Department HOD",
        "content": "AI&DS Department HOD: Mrs. Sangeetha"
    },

    {
        "category": "HOD",
        "title": "IT Department HOD",
        "content": "IT Department HOD: Mrs. Sangeetha"
    },

    {
        "category": "HOD",
        "title": "EEE Department HOD",
        "content": "EEE Department HOD: Mr. R. Sundaramoorthi"
    },

    {
        "category": "HOD",
        "title": "ECE Department HOD",
        "content": "ECE Department HOD: Mrs. N. Mangaiyakarasi"
    },

    {
        "category": "HOD",
        "title": "Mechanical Department HOD",
        "content": "Mechanical Department HOD: Dr. T. Pushparaj"
    },

    {
        "category": "HOD",
        "title": "Civil Department HOD",
        "content": "Civil Department HOD: Dr. R. Saravanan"
    },

    {
        "category": "HOD",
        "title": "Science and Humanities Department HOD",
        "content": "Science and Humanities Department HOD: Dr. V. Sureshkumar"
    },


    # ==========================================
    # ADMISSION
    # ==========================================

    {
        "category": "Admission",
        "title": "Admissions",
        "content": """Kings College of Engineering offers admission to undergraduate and postgraduate programmes.

Students can get information about:

• Admission process
• Eligibility requirements
• Application procedure
• Required documents
• Important admission dates
• Counselling
• UG and PG admissions

For the latest admission information, students should refer to the official Kings College of Engineering website or contact the college.

Admission Contact:
+91-6380989024"""
    },


    # ==========================================
    # CONTACT
    # ==========================================

    {
        "category": "Contact",
        "title": "KCE Contact Information",
        "content": """Kings College of Engineering

Address:

Punalkulam, Near Thanjavur,
Gandarvakottai Taluk,
Pudukkottai District - 613 303,
Tamil Nadu, India.

Phone:
+91-6380989024

Email:
contact@kingsengg.edu.in

Website:
https://www.kingsengg.edu.in"""
    },


    # ==========================================
    # LOCATION
    # ==========================================

    {
        "category": "Location",
        "title": "KCE Campus Location",
        "content": """Kings College of Engineering is located at:

Punalkulam, Near Thanjavur,
Gandarvakottai Taluk,
Pudukkottai District - 613 303,
Tamil Nadu, India.

The college campus is located near Thanjavur."""
    },


    # ==========================================
    # HOSTEL
    # ==========================================

    {
        "category": "Hostel",
        "title": "Hostel Facilities",
        "content": """Kings College of Engineering provides hostel facilities for students.

Hostel facilities include:

• Separate accommodation facilities
• Mess facilities
• Purified drinking water
• Study facilities
• Medical facilities
• Reading rooms
• Recreation facilities
• Gym facilities
• Sports facilities
• Canteen facilities

Students should contact the college for the latest information about hostel availability, fees and rules."""
    },


    # ==========================================
    # TRANSPORT
    # ==========================================

    {
        "category": "Transport",
        "title": "College Transport",
        "content": """Kings College of Engineering provides college bus transportation facilities for students.

Transport services connect the college with Thanjavur and surrounding areas.

Students should check with the college for the latest bus routes, timings and transport fees."""
    },


    # ==========================================
    # LIBRARY
    # ==========================================

    {
        "category": "Library",
        "title": "Central Library",
        "content": """Kings College of Engineering has a central library that provides academic and reference resources for students and faculty.

Library facilities include:

• Books
• Reference materials
• Journals
• E-resources
• Reading facilities
• Digital resources
• OPAC facility
• Online learning resources

The library supports academic learning and research activities."""
    },

    {
        "category": "Library",
        "title": "Library Timings",
        "content": """The library provides facilities during college working hours.

Students should check with the library or official KCE website for the latest working hours, book issue timings and holiday schedules."""
    },


    # ==========================================
    # INFRASTRUCTURE
    # ==========================================

    {
        "category": "Infrastructure",
        "title": "Campus Infrastructure",
        "content": """Kings College of Engineering provides various academic and campus infrastructure facilities.

Facilities include:

• Classrooms
• Laboratories
• Computer laboratories
• Library
• Smart classrooms
• Seminar facilities
• Auditorium
• Hostels
• Cafeteria
• Sports facilities
• Healthcare facilities
• Wi-Fi facilities"""
    },


    # ==========================================
    # CANTEEN
    # ==========================================

    {
        "category": "Canteen",
        "title": "Canteen Facilities",
        "content": """Kings College of Engineering provides canteen and cafeteria facilities on campus.

Students and staff can use the campus dining facilities.

For current food availability, timings and other details, students should contact the college canteen."""
    },


    # ==========================================
    # HEALTHCARE
    # ==========================================

    {
        "category": "Healthcare",
        "title": "Health Centre",
        "content": """Kings College of Engineering provides healthcare facilities for students.

The college health centre supports students with basic medical and healthcare services.

Students can contact the college administration for current healthcare and emergency information."""
    },


    # ==========================================
    # PLACEMENTS
    # ==========================================

    {
        "category": "Placement",
        "title": "Training and Placement",
        "content": """Kings College of Engineering has a Training and Placement Cell that supports students with career opportunities and campus recruitment.

Placement activities include:

• Training programmes
• Skill development
• Placement preparation
• Company recruitment
• Career guidance
• Interview preparation

Students should contact the Training and Placement Cell for the latest placement companies, drives and statistics."""
    },


    # ==========================================
    # SCHOLARSHIPS
    # ==========================================

    {
        "category": "Scholarship",
        "title": "Scholarships",
        "content": """Kings College of Engineering provides scholarship and student support opportunities.

Scholarship-related support may include:

• Merit-based scholarships
• Student awards
• Fee support
• Government scholarship opportunities

Students should contact the college office for current scholarship eligibility, application procedure and available schemes."""
    },


    # ==========================================
    # CAMPUS FACILITIES
    # ==========================================

    {
        "category": "Facility",
        "title": "Campus Facilities",
        "content": """Kings College of Engineering provides several facilities for students:

• Classrooms
• Laboratories
• Computer labs
• Library
• Smart classrooms
• Auditorium
• Seminar halls
• Hostels
• Canteen
• Gym
• Sports facilities
• Healthcare facilities
• Wi-Fi facilities
• Recreation facilities"""
    },


    # ==========================================
    # STUDENT ACTIVITIES
    # ==========================================

    {
        "category": "Activities",
        "title": "Student Activities",
        "content": """Kings College of Engineering provides opportunities for students to participate in academic, technical, sports and extracurricular activities.

Students can participate in:

• Technical events
• Workshops
• Seminars
• Value-added courses
• Sports activities
• Student development activities
• Cultural activities"""
    },


    # ==========================================
    # OFFICIAL WEBSITE
    # ==========================================

    {
        "category": "Website",
        "title": "Official KCE Website",
        "content": """The official website of Kings College of Engineering is:

https://www.kingsengg.edu.in

Students should use the official website for the latest information about:

• Admissions
• Courses
• Departments
• Events
• Facilities
• Placements
• Contact information"""
    },


    # ==========================================
    # FEES
    # ==========================================

    {
        "category": "Fees",
        "title": "Fee Information",
        "content": """The fee structure at Kings College of Engineering may vary depending on the programme and admission category.

Students can get information about:

• Tuition fees
• Hostel fees
• Examination fees
• Admission-related fees
• Scholarship and fee reimbursement details

For the latest fee structure, students should contact the college admission office.

Admission Contact:
+91-6380989024"""
    }

]


# ==========================================
# CREATE / RESET DATABASE
# ==========================================

with app.app_context():

    db.drop_all()

    db.create_all()

    for item in data:

        info = CollegeInfo(
            category=item["category"],
            title=item["title"],
            content=item["content"]
        )

        db.session.add(info)

    db.session.commit()


print("Database seeded successfully!")