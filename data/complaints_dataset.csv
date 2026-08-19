import csv
import random
from pathlib import Path


OUTPUT_FILE = Path("data/complaints_dataset.csv")

random.seed(42)


DATA = {

    "Academic": {
        "titles": [
            "Marks not updated",
            "Attendance issue",
            "Exam schedule problem",
            "Assignment submission issue",
            "Result not updated",
            "Course registration problem",
            "Internal marks issue",
            "Faculty related issue"
        ],
        "descriptions": [
            "My marks have not been updated on the student portal.",
            "My attendance is incorrect in the academic record.",
            "The examination schedule has not been updated properly.",
            "I am unable to submit my assignment through the portal.",
            "My semester result is still not showing.",
            "I am facing a problem while registering for my course.",
            "My internal assessment marks appear to be incorrect.",
            "I need assistance regarding an academic issue."
        ]
    },

    "Hostel": {
        "titles": [
            "Hostel room issue",
            "Water supply problem",
            "Hostel room allocation issue",
            "Hostel cleanliness problem",
            "Bathroom issue",
            "Hostel electricity problem",
            "Room maintenance issue",
            "Hostel facility problem"
        ],
        "descriptions": [
            "There is a problem with my hostel room.",
            "Water supply has been irregular in the hostel.",
            "I have an issue with my hostel room allocation.",
            "The hostel common area is not being cleaned properly.",
            "The bathroom facilities require attention.",
            "There is an electricity problem in the hostel.",
            "My hostel room requires maintenance.",
            "A basic hostel facility is not working properly."
        ]
    },

    "Infrastructure": {
        "titles": [
            "Classroom infrastructure issue",
            "Broken classroom equipment",
            "Damaged furniture",
            "Building maintenance issue",
            "Classroom problem",
            "Campus infrastructure problem",
            "Ceiling leakage",
            "Electrical infrastructure issue"
        ],
        "descriptions": [
            "The classroom infrastructure needs maintenance.",
            "Some equipment in the classroom is damaged.",
            "Several chairs and desks are damaged.",
            "The building requires maintenance.",
            "There is a problem with the classroom facilities.",
            "The campus infrastructure needs attention.",
            "Water is leaking from the classroom ceiling.",
            "There is an electrical infrastructure problem."
        ]
    },

    "IT / Wi-Fi": {
        "titles": [
            "WiFi not working",
            "Internet connectivity problem",
            "Campus WiFi issue",
            "Student portal not working",
            "Network connection problem",
            "Login portal issue",
            "Internet speed problem",
            "Computer network issue"
        ],
        "descriptions": [
            "WiFi is not working in my hostel.",
            "The internet connection is unavailable.",
            "Campus WiFi keeps disconnecting.",
            "The student portal is not working properly.",
            "I am facing a network connectivity problem.",
            "I cannot log in to the student portal.",
            "Internet speed is extremely slow.",
            "The computer network is not accessible."
        ]
    },

    "Laboratory": {
        "titles": [
            "Lab equipment problem",
            "Laboratory computer issue",
            "Missing lab equipment",
            "Lab safety issue",
            "Practical equipment damaged",
            "Laboratory maintenance",
            "Lab workstation problem",
            "Laboratory facility issue"
        ],
        "descriptions": [
            "The equipment required for the practical is not working.",
            "A computer in the laboratory is not functioning.",
            "Some required laboratory equipment is missing.",
            "There is a safety issue in the laboratory.",
            "Practical equipment appears to be damaged.",
            "The laboratory requires maintenance.",
            "One of the lab workstations is not working.",
            "There is a problem with the laboratory facilities."
        ]
    },

    "Library": {
        "titles": [
            "Library book unavailable",
            "Library computer issue",
            "Library timing problem",
            "Book return issue",
            "Library seat problem",
            "Digital library issue",
            "Library facility problem",
            "Reference book unavailable"
        ],
        "descriptions": [
            "The required book is not available in the library.",
            "A computer in the library is not working.",
            "The library timing is causing difficulty for students.",
            "I am facing an issue while returning a library book.",
            "There are not enough seats available in the library.",
            "The digital library is not accessible.",
            "A library facility requires maintenance.",
            "The required reference book is unavailable."
        ]
    },

    "Maintenance": {
        "titles": [
            "Water leakage",
            "Electrical repair required",
            "Broken fan",
            "Broken light",
            "Plumbing problem",
            "Cleaning required",
            "Maintenance request",
            "Damaged facility"
        ],
        "descriptions": [
            "There is water leakage that requires immediate repair.",
            "An electrical repair is required.",
            "The ceiling fan is not working.",
            "The lights in the room are not working.",
            "There is a plumbing problem that needs attention.",
            "The area requires proper cleaning.",
            "A maintenance request has been pending.",
            "A campus facility is damaged and needs repair."
        ]
    },

    "Transport": {
        "titles": [
            "Bus delay",
            "Bus route problem",
            "College bus issue",
            "Transport timing problem",
            "Bus overcrowding",
            "Missing bus service",
            "Transport facility issue",
            "Bus maintenance problem"
        ],
        "descriptions": [
            "The college bus arrived late today.",
            "There is an issue with the current bus route.",
            "The college bus service is facing a problem.",
            "The transport timing is inconvenient.",
            "The college bus is overcrowded.",
            "The scheduled bus service did not arrive.",
            "There is a problem with the transport facility.",
            "The college bus requires maintenance."
        ]
    }
}


LOCATIONS = [
    "Hostel A",
    "Hostel B",
    "Hostel C",
    "Academic Block",
    "Main Building",
    "Library",
    "Laboratory Block",
    "Computer Lab",
    "Campus",
    "Sports Complex",
    "Main Gate"
]


LOW_WORDS = [
    "minor",
    "slight",
    "small",
    "non-urgent"
]

MEDIUM_WORDS = [
    "problem",
    "issue",
    "difficulty",
    "not working"
]

HIGH_WORDS = [
    "urgent",
    "repeated",
    "many students",
    "unavailable",
    "serious"
]

CRITICAL_WORDS = [
    "dangerous",
    "emergency",
    "safety",
    "electrical sparks",
    "major leakage"
]


def generate_priority(category, description):
    text = description.lower()

    if any(word in text for word in CRITICAL_WORDS):
        return "Critical"

    if any(word in text for word in HIGH_WORDS):
        return "High"

    if any(word in text for word in LOW_WORDS):
        return "Low"

    return random.choice(["Low", "Medium", "Medium", "High"])


def create_dataset(total_records=2000):

    rows = []

    categories = list(DATA.keys())

    for _ in range(total_records):

        category = random.choice(categories)

        category_data = DATA[category]

        title = random.choice(category_data["titles"])

        description = random.choice(category_data["descriptions"])

        location = random.choice(LOCATIONS)

        # Add realistic contextual information
        variants = [
            f"{description} The issue is at {location}.",
            f"{description} Students at {location} are affected.",
            f"{description} I noticed this problem at {location}.",
            f"{description} This has been causing inconvenience at {location}.",
            description
        ]

        description = random.choice(variants)

        priority = generate_priority(category, description)

        rows.append({
            "title": title,
            "description": description,
            "category": category,
            "priority": priority
        })

    return rows


def save_dataset(rows):

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "title",
                "description",
                "category",
                "priority"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":

    print("Generating synthetic student complaint dataset...")

    rows = create_dataset(2000)

    save_dataset(rows)

    print()
    print("Dataset generated successfully.")
    print(f"Records: {len(rows)}")
    print(f"File: {OUTPUT_FILE}")