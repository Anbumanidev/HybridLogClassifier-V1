import re

def classify_with_regex(log_message:str) -> str:
    log_message = log_message.strip()
    regex_pattens = {
        r"User User\d+ logged (in|out).": "User Action",
        r"Backup (started|ended) at .*": "System Notification",
        r"Backup completed successfully.": "System Notification",
        r"System updated to version .*": "System Notification",
        r"File .* uploaded successfully by user .*": "System Notification",
        r"Disk cleanup completed successfully.": "System Notification",
        r"System reboot initiated by user .*": "System Notification",
        r"Account with ID .* created by .*": "User Action"
    }
    for patten, label in regex_pattens.items():
        if re.search(patten, log_message, re.IGNORECASE):
            return label
    return None

if __name__ == "__main__":
    print(classify_with_regex("User User685 logged out."))
    print(classify_with_regex("Backup started at 2025-05-14 07:06:55."))
    print(classify_with_regex("Admin privilege escalation alert for user 2893"))
    print(classify_with_regex("User 8483 escalated privileges to admin level"))
    print(classify_with_regex("System configuration is no longer valid"))
    print(classify_with_regex("Email service experiencing issues with sending"))
    print(classify_with_regex("Account with ID 5351 created by User634."))
    print(classify_with_regex("User 7662 tried to bypass API security measures"))
    print(classify_with_regex("System reboot initiated by user User243."))
    print(classify_with_regex("Disk cleanup completed successfully."))
    print(classify_with_regex("System updated to version 3.9.1."))
    print(classify_with_regex("  Backup completed successfully.  "))
    print(classify_with_regex("   Security alert: suspicious activity on server 1"))