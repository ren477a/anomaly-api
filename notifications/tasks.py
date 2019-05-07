from twilio.rest import Client
from background_task import background



@background()
def send_sms(person_id, notif_id):
    from .models import Person, Notification
    print("send_sms: Processing send sms person_id={} notif_id={}".format(person_id, notif_id))
    owner = Person.objects.get(pk=person_id)
    notification = Notification.objects.get(pk=notif_id)
    account_sid = 'AC9d258d67d705acb8d2bf9aa1cf98a90b'
    auth_token = 'd467cc7ad0f8ad4b5eba013cc4e9ac8a'
    client = Client(account_sid, auth_token)
    body = "{} is detected in {} at {}.".format(
        notification._type, 
        notification.camera.name,
        notification.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
    )
    print("send_sms: Message body={}".format(body))
    if owner.enable_sms:
        message = client.messages.create(
                                    from_='+12077627402',
                                    body=body,
                                    to='+639254697619'
                                )
        print("send_sms: msg_id={} status={}".format(message.sid, message.status))
