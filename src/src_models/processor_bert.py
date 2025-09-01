from sentence_transformers import SentenceTransformer
import joblib


# transformer_model = SentenceTransformer(r"E:\AIML-Projects\HybridLogClassifier-V1\models\transformer_encoder")
model_classifier = joblib.load(r"E:\AIML-Projects\HybridLogClassifier-V1\models\final_model.joblib")
transformer_model = SentenceTransformer(r"E:\AIML-Projects\HybridLogClassifier-V1\models\transformer_encoder") 


def classify_with_bert(log_message):
    embed = transformer_model.encode(log_message)
    scores = model_classifier.predict_proba([embed])[0]
    probabilities = list(scores)
    
    if max(probabilities) <= 0.7:
        return "unclassified"
    
    predicted_class = model_classifier.predict([embed])[0]
    
    return predicted_class



if __name__ == "__main__":
    logs = [
        "alpha.osapi_compute.wsgi.server - 12.10.11.1 - API returned 404 not found error",
        "GET /v2/3454/servers/detail HTTP/1.1 RCODE   404 len: 1583 time: 0.1878400",
        "System crashed due to drivers errors when restarting the server",
        "Hey bro, she is in critical ya!",
        "Multiple login failures occurred on user 6454 account",
        "Server A790 was restarted unexpectedly during the process of data transfer"
    ]
    
    for log in logs:
        print(classify_with_bert(log))