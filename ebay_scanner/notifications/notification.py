from twilio.rest import Client
import twilio

class Notification:
    def __init__(self, content, recipients):
        self.content = content
        self.recipients = recipients
    
    def send_sms_notification(self):
        try:
            account_sid = 'TWILLIO_ACCOUNT_SID' # TODO: add variables for secure parameters, os.environ['TWILIO_ACCOUNT_SID']
            auth_token = 'TWILLIO_AUTH_TOKEN' # TODO: add variables for secure parameters, os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid, auth_token)

            content = self.content.split(',')
            message = client.messages.create(
                body=f"\n\n\nTitle: {content[1]}\n\nPrice: {content[2]}\n\nLink: {content[3]}",
                to="+44"+self.recipients,
                from_="+447401068522"
            )
            print(message.sid)
        # TODO: Add logging to service
        except twilio.base.exceptions.TwilioRestException  as e:
             print(e)

    def send_email_notification(self):
        print('sending email')