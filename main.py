"""
1-twilio client setup
2-user inputs
3-scheduling logic
4-message sending
"""
#step 1: install required libraries
from twilio.rest import Client
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Step 2: Twilio credentials (loaded from .env)
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

#step 3: designe send message function
def send_message(recipient_number, message_body):
    try:
        message = client.messages.create(
           from_='whatsapp:+14155238886',
           body=message_body,
           to=f'whatsapp:{recipient_number}'
        )
        print(f"Message sent successfully! Message SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")     

#step 4: get user inputs
name = input("Enter the recipient name: ")
recipient_number = input("Enter the recipient WhatsApp number (with country code): ")
message_body = input(f"Enter the message to be sent to {name}: ")

#step 5: get scheduling inputs
schedule_choice = input("Do you want to send the message now or schedule it for later? (now/later): ").strip().lower()
if schedule_choice == 'later':
    date_str = input("Enter the date to send the message (YYYY-MM-DD): ")
    time_str = input("Enter the time to send the message (HH:MM in 24-hour format): ")
    scheduled_datetime_str = f"{date_str} {time_str}"
    scheduled_datetime = datetime.strptime(scheduled_datetime_str, "%Y-%m-%d %H:%M")
    
    #step 6: calculate delay
    current_datetime = datetime.now()
    delay_seconds = (scheduled_datetime - current_datetime).total_seconds()
    
    if delay_seconds > 0:
        print(f"Message scheduled to be sent at {scheduled_datetime}. Waiting...")
        time.sleep(delay_seconds)
        send_message(recipient_number, message_body)
    else:
        print("The scheduled time is in the past. Please enter a future time.")
elif schedule_choice == 'now':
    send_message(recipient_number, message_body)
else:
    print("Invalid choice. Please enter 'now' or 'later'.")

