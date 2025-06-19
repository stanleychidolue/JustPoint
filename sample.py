from django.core.mail import send_mail
from dotenv import load_dotenv
import os

load_dotenv()
rider_name = "stanley chidolue"
redirect_url = f"http://127.0.0.1:3000/delivery/view-order-items/hdsbkjidjvpjd"
html_message = f"""
            <html>
            <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
            </head>
            <body>
                <div class="logo mb-3" style="background-color: #a52a2a; display:inline; ">
                <img class="nav-logo" src="	https://cderaservices.com/images/cderaservicesLogo.png" alt="JustPointLogo" />
                </div>
                <p class="mb-4">Good day Mr {rider_name},</p>
                <p>We have a delivery request for you, <br>
                Are you interested? Click the button below to accept
                </p>
                <a href="{redirect_url}"><button class="py-3" style="width: 150px; background-color: #a52a2a;justify-self: center; color:white !important; padding: 5px 0; font-weight: bolder;" >
                ACCEPT</button>
                </a>
                </p>
            </body>
            
            </html>
            """


send_mail(
    subject="Alert!!! JustPoint Delivery Request",
    message=f"JustPoint Delivery Request",
    from_email=None,
    recipient_list=[os.environ.get('EMAIL_USERNAME'),],
    html_message=html_message)
