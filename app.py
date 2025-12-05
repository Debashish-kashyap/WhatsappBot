from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
from datetime import datetime
import time
from dotenv import load_dotenv
import os
import threading

# Load environment variables
load_dotenv()

# Get the absolute path to the templates directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Send message function
def send_message(recipient_number, message_body):
    try:
        app.logger.info(f'Sending message to {recipient_number}')
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to=f'whatsapp:{recipient_number}'
        )
        app.logger.info(f'Twilio API returned SID {message.sid}')
        return {"status": "success", "sid": message.sid}
    except Exception as e:
        # Log full exception for debugging
        app.logger.exception(f'Failed to send message to {recipient_number}')
        return {"status": "error", "message": str(e)}


@app.route('/diag')
def diag():
    """Diagnostics endpoint to verify environment and Twilio connectivity.

    Returns JSON with presence of credentials and a lightweight Twilio account fetch result.
    """
    sid = account_sid
    token = auth_token
    result = {"env": {"TWILIO_ACCOUNT_SID": bool(sid), "TWILIO_AUTH_TOKEN": bool(token)}}
    if not sid or not token:
        result['twilio'] = {"ok": False, "message": "Missing credentials"}
        return jsonify(result), 400

    try:
        # attempt to fetch account as a lightweight auth check
        acc = client.api.accounts(sid).fetch()
        result['twilio'] = {"ok": True, "account_sid": acc.sid, "friendly_name": getattr(acc, 'friendly_name', None)}
        return jsonify(result)
    except Exception as e:
        app.logger.exception('Twilio diag failed')
        result['twilio'] = {"ok": False, "message": str(e)}
        return jsonify(result), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_whatsapp():
    try:
        # force JSON parsing to raise a clear error if body is invalid
        data = request.get_json(force=True)
        name = data.get('name')
        recipient_number = data.get('recipient_number')
        message_body = data.get('message_body')
        schedule_choice = data.get('schedule_choice')

        if schedule_choice == 'now':
            result = send_message(recipient_number, message_body)
            return jsonify(result)

        elif schedule_choice == 'later':
            date_str = data.get('date')
            time_str = data.get('time')
            scheduled_datetime_str = f"{date_str} {time_str}"
            scheduled_datetime = datetime.strptime(scheduled_datetime_str, "%Y-%m-%d %H:%M")

            current_datetime = datetime.now()
            delay_seconds = (scheduled_datetime - current_datetime).total_seconds()

            if delay_seconds > 0:
                def send_scheduled():
                    time.sleep(delay_seconds)
                    send_message(recipient_number, message_body)

                thread = threading.Thread(target=send_scheduled)
                thread.daemon = True
                thread.start()

                return jsonify({"status": "scheduled", "message": f"Message scheduled for {scheduled_datetime}"})
            else:
                return jsonify({"status": "error", "message": "Scheduled time is in the past"}), 400

        else:
            return jsonify({"status": "error", "message": "Invalid schedule choice"}), 400

    except Exception as e:
        # Log exception and always return JSON so frontend parsing won't fail
        app.logger.exception("Error in /send_message")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
