from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Dictionary to store phone numbers by group ID (conversation ID)
group_phone_numbers = {}

@app.route('/Phone', methods=['POST'])
def phone():
    data = request.json
    print("Received data:", data)

    group_id = str(data.get('groupId'))
    matched_intent = data.get('matchedIntentName', '')
    message = data.get('message', '')

    if matched_intent.lower() == 'phonenumber' and message.startswith('+91') and len(message) == 13:
        # Store phone number per group ID
        group_phone_numbers[group_id] = message
        phone_number_formatted = message.replace("+91", "0")

        payload = {
            "phone_number": phone_number_formatted
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
                {"message": f"Updated phone number as {phone_number_formatted}"}
            ]), response.status_code
        except Exception as e:
            print("Error calling external API:", e)
            return jsonify([{"message": "Failed to call referral API."}]), 500

    return jsonify([{"message": "No valid phone number intent found."}]), 200


@app.route('/name', methods=['POST'])
def name():
    data = request.json or {}
    print("Received data:", data)

    group_id = str(data.get('groupId'))
    matched_intent = data.get('matchedIntentName', '')
    message = data.get('message', '')

    phone_number = group_phone_numbers.get(group_id)

    if matched_intent.lower() == 'name' and phone_number:
        phone_number_formatted = phone_number.replace("+91", "0")
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
    data = request.json or {}
    print("Received data:", data)

    group_id = str(data.get('groupId'))
    matched_intent = data.get('matchedIntentName', '')
    message = data.get('message', '')

    phone_number = group_phone_numbers.get(group_id)

    if matched_intent.lower() == 'address' and phone_number:
        phone_number_formatted = phone_number.replace("+91", "0")
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

            # Optional: clear stored data after all fields are collected
            group_phone_numbers.pop(group_id, None)

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
