from django.core.mail import EmailMessage, BadHeaderError
from api import email_constants
#from django.dispatch import receiver
from api.utility.customexceptions import BadRequest


def send_verification_email(sender,instance, **kwargs):
        subject = email_constants.WELCOME_EMAIL_SUBJECT
        body = email_constants.VERIFICATION_EMAIL_BODY.format(instance.code)
        from_email = email_constants.WELCOME_EMAIL_FROM
        to = [instance.email] #this is going to be only one email for current use case
        #send_email(subject, body, from_email, to, bcc = None, connection = None, attachments =None, header=None, cc=None, reply_to=None)
        success = False

        if subject and body and from_email and to:
            email = EmailMessage(
                subject= subject,
                body= body,
                from_email = from_email,
                to = to,
            )
            try:
                email.send()
            except BadHeaderError:
                error_msg = 'Invalid header found.'
                return error_msg
            return success
        else:
            raise BadRequest(detail='We failed to send the verification email.')

def send_welcome_email(sender,instance, **kwargs):
        subject = email_constants.WELCOME_EMAIL_SUBJECT
        body = email_constants.WELCOME_EMAIL_BODY
        from_email = email_constants.WELCOME_EMAIL_FROM
        to = [instance.email] #this is going to be only one email for current use case
        success = False

        if subject and body and from_email and to:
            email = EmailMessage(
                subject= subject,
                body= body,
                from_email = from_email,
                to = to,
            )
            try:
                email.send()
            except BadHeaderError:
                error_msg = 'Invalid header found.'
                return error_msg
            return success
        else:
            raise BadRequest(detail='We failed to send the verification email.')
    


def send_email(subject, body, from_email, to, bcc, connection, attachments, header, cc, reply_to):
    success = False
    if subject and body and from_email and to:
        email = EmailMessage(
            subject= subject,
            body= body,
            from_email = from_email,
            to = ['to1@example.com', 'to2@example.com'],
           
        )
        try:
            email.send()
        except BadHeaderError:
            error_msg = 'Invalid header found.'
            return error_msg
        return success
    else:
        raise BadRequest(detail='We failed to send the verification email.')
    
