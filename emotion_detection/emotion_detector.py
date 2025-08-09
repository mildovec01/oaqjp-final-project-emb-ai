import requests
import json

def emotion_detector(text_to_analyze):
    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    response = requests.post(URL, json = input_json, headers=header)
    formatted_response = json.loads(response.text)

    if response.status_code == 200:
        return formatted_response
    elif response.status_code == 400:
        formatted_response = {
                            'anger': None,
                            'disgust': None, 
                            'fear': None, 
                            'joy': None, 
                            'sadness': None, 
                            'dominant_emotion': None}
        return formatted_response

def emotion_prediction(detected_text):
    if all(value is None for value in detected_text.values()):
        return detected_text
    if detected_text['emotionPredictions'] is not None:
        emotions = detected_text['emotionPredictions'][0]['emotion']
        anger = emotions['anger']
        disgust = emotions['disgust']
        fear = emotions['fear']
        joy = emotions['joy']
        sadness = emotions['sadness']
        max_emotion = max(emotions, key=emotions.get)
        formatted_dict_emotions = {
                                'anger': anger,
                                'disgust': disgust,
                                'fear': fear,
                                'joy': joy,
                                'sadness': sadness,
                                'dominant_emotion': max_emotion
                                }
        return formatted_dict_emotions
def emotion_predictor(text_to_analyse: str) -> dict:
    """
    Sends a text to the Watson Emotion Analysis endpoint and returns the predicted emotions.
    """
    payload = {"raw_document": {"text": text_to_analyse}}
    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=20)

    # Repair the response status code
    if resp.status_code != 200:
        raise RuntimeError(f"Watson endpoint returned {resp.status_code}: {resp.text}")

    data = resp.json()


    preds = data.get("emotionPredictions", [])
    if not preds:
        return _normalize_output({}) # No predictions found

    emotions = preds[0].get("emotion", {}) or {}
    return _normalize_output(emotions)
