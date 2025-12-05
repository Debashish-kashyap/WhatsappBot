from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
from datetime import datetime
import time
from dotenv import load_dotenv
import os
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Send message function
def send_message(recipient_number, message_body):
    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to=f'whatsapp:{recipient_number}'
        )
        return {"status": "success", "sid": message.sid}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_whatsapp():
    data = request.json
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
            return jsonify({"status": "error", "message": "Scheduled time is in the past"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
