import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()


def send_delivery_request(redirect_url, riders):
    with smtplib.SMTP_SSL('smtp.gmail.com') as connection:
        connection.login(user=os.environ.get("EMAIL_USERNAME"),
                         password=os.environ.get("EMAIL_PASSWORD"))

        for rider in riders:
            msg = MIMEMultipart()
            msg['From'] = os.environ.get("EMAIL_USERNAME")
            msg['To'] = rider.email
            msg['Subject'] = "Alert!!! JustPoint Delivery Request"

            html = f"""
            <html>
            <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
            </head>
            <body>
                <div class="logo mb-3" style="background-color: #a52a2a; display:inline; ">
                <img class="nav-logo" src="	https://cderaservices.com/images/cderaservicesLogo.png" alt="JustPointLogo" />
                </div>
                <p class="mb-4">Good day Mr {rider.name},</p>
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
            # Record the MIME types of part - text/plain and text/html.
            part1 = MIMEText(html, 'html')
            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            # msg.attach(part1)
            msg.attach(part1)
            connection.sendmail(from_addr=os.environ.get("EMAIL_USERNAME"),
                                to_addrs=[rider.email,],
                                msg=msg.as_string()
                                )


def sort_product_by_rider_type(order, rider) -> dict:
    all_items = []
    total_amount, total_qty = 0, 0
    # shops = set()
    shops = {}
    for item in order.cartitems.all():
        if item.product and rider.dispatch_type == "Estate":
            all_items.append(item)
            total_amount += int(item.product.price)
            total_qty += item.quantity
            # shops.add(item.product.shop.name)
            shops[item.product.shop.name] = "received" if item.received else "not_received"
        elif item.home_appliance and rider.dispatch_type == "HomeAppliance":
            all_items.append(item)
            total_amount += int(item.home_appliance.price)
            total_qty += item.quantity
            # shops.add(item.home_appliance.shop.name)
    return {"order": all_items, "total_order_amount": total_amount, 'total_order_qty': total_qty, "shops": shops}
