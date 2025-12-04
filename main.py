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

#step 2: twilio credentials
account_sid = 'AC684e965ddbdf4cbb8b5bcbf355291f78'
auth_token = 'ff91fc3f40b4854fe4969ec065f5fbb1'

client = Client(account_sid, auth_token)

#step 3: designe send message function
def send_message(to_number, from_number, message_body):
    try:
        message = client.messages.create(
           from_='whatsapp:+14155238886',
           body=message_body,
           to=f'whatsapp:{to_number}'
        )
        print(f"Message sent successfully! Message SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")     

#step 4: get user inputs
