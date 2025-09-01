
import pandas as pd

import sys, os
sys.path.append(os.path.dirname(__file__))

from src_models.processor_regex import classify_with_regex
from src_models.processor_bert import classify_with_bert
from src_models.processor_llm import classify_with_llm


def classifier(source, log_message):
    if source == "ModernCRM":
        label = classify_with_llm(log_message)
    else:
        label = classify_with_regex(log_message)
        if not label:
            label = classify_with_bert(log_message)
    return label

def classifier_csv(input_file):
    df = pd.read_csv(input_file)
    source_log_list = df.loc[:, ['source', 'log_message']].values.tolist()
    return classifier_list(source_log_list)

def classifier_list(log_list):
    results = []
    for source, log_message in log_list:
        label = classifier(source, log_message)
        results.append((source, log_message, label))
    return results


if __name__ == "__main__":
    # logs = [
    # ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
    # ("BillingSystem", "User 12345 logged in."),
    # ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
    # ("AnalyticsEngine", "Backup completed successfully."),
    # ("ModernHR", "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1 RCODE  200 len: 1583 time: 0.1878400"),
    # ("ModernHR", "Admin access escalation detected for user 9429"),
    # ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
    # ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."),
    # ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality."),
    # ("LegacyCRM", " The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025")
    # ]
    
    # print(classifier_list(logs))
    print(classifier_csv("E:/AIML-Projects/HybridLogClassifier-V1/test/test_logs.csv"))