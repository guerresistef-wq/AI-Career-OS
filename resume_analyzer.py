from tkinter import filedialog
from tkinter import Tk
from pypdf import PdfReader


def select_resume_file():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Resume PDF",
        filetypes=[
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        ]
    )

    return file_path


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def find_keywords(text, keywords):
    found_keywords = []

    for keyword in keywords:
        if keyword.lower() in text.lower():
            found_keywords.append(keyword)

    return found_keywords


def calculate_resume_score(found_keywords):
    score = 0

    business_keywords = [
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

    technical_keywords = [
        "python",
        "sql",
        "api",
        "cloud",
        "ai",
        "automation",
        "data",
        "analytics"
    ]

    for keyword in found_keywords:
        if keyword in business_keywords:
            score += 8

        if keyword in technical_keywords:
            score += 6

    if score > 100:
        score = 100

    return score


def analyze_resume_text(text):
    print("\n========== RESUME PREVIEW ==========\n")
    print(text[:1500])

    print("\n========== RESUME ANALYSIS ==========\n")

    keywords = [
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

    found_keywords = find_keywords(text, keywords)
    resume_score = calculate_resume_score(found_keywords)

    if found_keywords:
        print("Keywords found:")

        for keyword in found_keywords:
            print("-", keyword)
    else:
        print("No known keywords found yet.")

    print()
    print("Resume Score:", resume_score, "/ 100")

    if resume_score >= 80:
        print("Level: Strong candidate profile")
    elif resume_score >= 60:
        print("Level: Good profile with room to improve")
    else:
        print("Level: Needs stronger positioning")


def main():
    file_path = select_resume_file()

    if not file_path:
        print("No file selected.")
        return

    print("Selected resume:")
    print(file_path)

    text = extract_text_from_pdf(file_path)

    if text.strip() == "":
        print("No text could be extracted from this PDF.")
        print("It may be scanned or image-based.")
        return

    analyze_resume_text(text)


if __name__ == "__main__":
    main()