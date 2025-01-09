from flask import Flask, request, jsonify, render_template
import requests
tokenhere = "AstraCS:tAmXduQdyLljGTHaihkJCTgI:3b5923c9841f1206dd76294e2f3ea5597bf1fc844c2659d304bbfa1d67b8eda5"
import csv

app = Flask(__name__)

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a6af9f4a-c1e7-49cb-9d11-7f445fa5e7f0"
FLOW_ID = "f05c0f91-e615-415d-bd47-3d478bde695d"
APPLICATION_TOKEN = tokenhere
ENDPOINT = "social_media" # You can set a specific endpoint name in the flow settings

def run_flow(message: str, endpoint: str = ENDPOINT, output_type: str = "chat", input_type: str = "chat", tweaks: dict = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    if tweaks:
        payload["tweaks"] = tweaks
    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx/5xx HTTP codes
        return response.json()

    except requests.exceptions.RequestException as e:
        print("Error calling Langflow API:", e)
        return {"error": "API request failed."}

# Chatbot endpoint
@app.route('/chatbot', methods=['POST'])
def chatbot():
    if request.is_json:
        try:
            data = request.get_json()
            user_message = data.get('message')

            if not user_message:
                return jsonify({"error": "No message provided"}), 400

            # Call Langflow API to get a response
            response = run_flow(message=user_message)
            if "error" in response:
                return jsonify(response), 500

            # Extract the chatbot reply from the Langflow response
            message_data = response.get('outputs', [])[0].get('outputs', [])[0].get('results', {}).get('message', {}).get('text', 'Sorry, I did not understand that.')

            # Send the chatbot response back to the frontend
            return jsonify({"reply": message_data})

        except Exception as e:
            print("Error processing chatbot request:", e)
            return jsonify({"error": "Invalid JSON format"}), 400

    return jsonify({"error": "Invalid request."}), 400

def read_csv(file_path):
    data = {'labels': [], 'likes': [], 'shares': [], 'comments': []}
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    data['labels'].append(row['Post_Type'])  # Ensure this matches your CSV column name
                    data['likes'].append(int(row['Likes']))
                    data['shares'].append(int(row['Shares']))
                    data['comments'].append(int(row['Comments']))
                except (KeyError, ValueError) as e:
                    print(f"Error processing row: {e}")
                    continue
        return data
    except FileNotFoundError:
        print(f"CSV file not found: {file_path}")
        return data
@app.route('/')
def home():
    csv_data = read_csv('social_media_data.csv')
    return render_template('index.html', 
                           post_types=csv_data['labels'], 
                           likes_data=csv_data['likes'], 
                           shares_data=csv_data['shares'], 
                           comments_data=csv_data['comments'])


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
