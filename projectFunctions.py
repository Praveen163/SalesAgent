from agents import  function_tool
# import sendgrid
# from sendgrid.helpers.mail import Mail, Email, To, Content
import os
@function_tool
def send_email(body: str):
    """ Send out an email with the given body to all sales prospects """
    print("-----------------------------------------\ncomposed mail : \n-----------------------------------------\n",body)
    # sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
    # from_email = Email("praveen0nnn@gmail.com")  # Change to your verified sender
    # to_email = To("praveen04012004@gmail.com")  # Change to your recipient
    # content = Content("text/plain", body)
    # mail = Mail(from_email, to_email, "Sales email", content).get()
    # sg.client.mail.send.post(request_body=mail)
    # return {"status": "success"}

@function_tool
def not_answered(body: str):
    """ Send out an email with the given body to all sales prospects """
    print("-----------------------------------------\nERROR : \n-----------------------------------------\n",body)
