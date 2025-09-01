import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

VALID_CATEGORIES = {"Workflow Error", "Deprecation Warning", "Unclassified"}

def classify_with_llm(log_message: str) -> str:
    log_message = log_message.strip()
    prompt = """Classify the log message into exactly one of these categories:
(1) Workflow Error
(2) Deprecation Warning
If it does not fit, return exactly: Unclassified
Return only the category name. Nothing else.

Log message: {log_message}""".format(log_message=log_message)
    
    chat_completionn = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt}],
    )

    response = chat_completionn.choices[0].message.content.strip()

    # Enforce validation
    if response not in VALID_CATEGORIES:
        return "Unclassified"
    return response

if __name__ == "__main__":
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."))
    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"))
    print(classify_with_llm("System reboot initiated by user 12345."))
