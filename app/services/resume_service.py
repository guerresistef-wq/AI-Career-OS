from pypdf import PdfReader


KEYWORDS = [
    "sales",
    "account executive",
    "enterprise",
    "saas",
    "crm",
    "pipeline",
    "revenue",
    "negotiation",
    "cold calling",
    "account management",
    "python",
    "sql",
    "api",
    "cloud",
    "ai",
    "automation",
    "data",
    "analytics"
]


BUSINESS_KEYWORDS = [
    "sales",
    "account executive",
    "enterprise",
    "saas",
    "crm",
    "pipeline",
    "revenue",
    "negotiation",
    "cold calling",
    "account management"
]


TECHNICAL_KEYWORDS = [
    "python",
    "sql",
    "api",
    "cloud",
    "ai",
    "automation",
    "data",
    "analytics"
]


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def find_keywords(text):
    found_keywords = []

    for keyword in KEYWORDS:
        if keyword.lower() in text.lower():
            found_keywords.append(keyword)

    return found_keywords


def calculate_resume_score(found_keywords):
    score = 0

    for keyword in found_keywords:
        if keyword in BUSINESS_KEYWORDS:
            score += 8

        if keyword in TECHNICAL_KEYWORDS:
            score += 6

    if score > 100:
        score = 100

    return score


def analyze_resume(file_path):
    text = extract_text_from_pdf(file_path)

    if text.strip() == "":
        return {
            "success": False,
            "message": "No text could be extracted from this PDF.",
            "score": 0,
            "keywords": [],
            "preview": ""
        }

    found_keywords = find_keywords(text)
    score = calculate_resume_score(found_keywords)

    if score >= 80:
        level = "Strong candidate profile"
    elif score >= 60:
        level = "Good profile with room to improve"
    else:
        level = "Needs stronger positioning"

    return {
        "success": True,
        "message": level,
        "score": score,
        "keywords": found_keywords,
        "preview": text[:1500]
    }