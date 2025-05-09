from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Global variable to temporarily store the phone number
stored_phone_number = None

@app.route('/Phone', methods=['POST'])
def phone():
    global stored_phone_number
    data = request.json
    print("Received data:", data)

    matched_intent = data.get('matchedIntentName', '')
    message = data.get('message', '')

    if matched_intent.lower() == 'phonenumber' and message.startswith('+91') and len(message) == 13:
        stored_phone_number = message

        payload = {
            "phone_number": stored_phone_number.replace("+91", "0")
        }

        try:
            response = requests.post(
                'https://mihei-bot.onrender.com/new-referral',
                headers={'Content-Type': 'application/json'},
                json=payload
            )
            print("External API Status:", response.status_code)
            print("External API Body:", response.text)

            return jsonify([
                {"message": response.text},
                {"message": f"Updated phone number as {payload['phone_number']}"}
            ]), response.status_code
        except Exception as e:
            print("Error calling external API:", e)
            return jsonify([{"message": "Failed to call referral API."}]), 500

    return jsonify([{"message": "No valid phone number intent found."}]), 200


@app.route('/name', methods=['POST'])
def name():
    global stored_phone_number
    data = request.json or {}
    print("Received data:", data)

    matched_intent = data.get('matchedIntentName', '')
    message = data.get('message', '')

    if matched_intent.lower() == 'name' and stored_phone_number:
        phone_number_formatted = stored_phone_number.replace("+91", "0")
        payload = {
            "phone_number": phone_number_formatted,
            "first_name": message
        }

        try:
            response = requests.post(
                'https://mihei-bot.onrender.com/new-referral',
                headers={'Content-Type': 'application/json'},
                json=payload
            )
            print("External API Status:", response.status_code)
            print("External API Body:", response.text)

            return jsonify([
                {"message": response.text},
                {"message": f"Updated name as {message} where phone number is {phone_number_formatted}"}
            ]), response.status_code
        except Exception as e:
            print("Error calling external API:", e)
            return jsonify([{"message": "Failed to call referral API."}]), 500

    return jsonify([{"message": "Phone number or name intent not found."}]), 200


@app.route('/address', methods=['POST'])
def address():
    global stored_phone_number
    data = request.json or {}
    print("Received data:", data)

    matched_intent = data.get('matchedIntentName', '')
    message = data.get('message', '')

    if matched_intent.lower() == 'address' and stored_phone_number:
        phone_number_formatted = stored_phone_number.replace("+91", "0")
        payload = {
            "phone_number": phone_number_formatted,
            "address": message
        }

        try:
            response = requests.post(
                'https://mihei-bot.onrender.com/new-referral',
                headers={'Content-Type': 'application/json'},
                json=payload
            )
            print("External API Status:", response.status_code)
            print("External API Body:", response.text)

            return jsonify([
                {"message": response.text},
                {"message": f"Updated address as {message} where phone number is {phone_number_formatted}"}
            ]), response.status_code
        except Exception as e:
            print("Error calling external API:", e)
            return jsonify([{"message": "Failed to call referral API."}]), 500

    return jsonify([{"message": "Phone number or address intent not found."}]), 200


# Start Flask app
if __name__ == '__main__':
    app.run(port=5001, debug=True)
