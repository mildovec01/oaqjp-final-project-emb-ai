from flask import Flask, render_template, request
from emotion_detection import emotion_detector, emotion_prediction


app = Flask("Emotion Detection")

@app.route("/emotionDetector")
def sent_detector():
    """
    Analyze user input text and return emotion.
    """
    text_to_detect = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_detect)

    if not response or not response.get('dominant_emotion'):
        return "Invalid text! Please try again."

    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

@app.route("/")
def render_index_page():
    """Render main page."""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
