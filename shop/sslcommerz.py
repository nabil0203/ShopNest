import requests
import json
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string



# method for payment
def generate_sslcommerz_payment(request,order):
    post_data = {
        'store_id': settings.SSLCOMMERZ_STORE_ID,
        'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
        'total_amount': float(order.get_total_cost()),
        'currency': 'BDT',
        'tran_id': str(order.id),
        'success_url': request.build_absolute_uri(f'/payment/success/{order.id}/'),
        'fail_url': request.build_absolute_uri(f'/payment/fail/{order.id}/'),
        'cancel_url': request.build_absolute_uri(f'/payment/cancel/{order.id}/'),
        'cus_name': f"{order.first_name} {order.last_name}",
        'cus_email': order.email,
        'cus_phone': order.phone,
        'cus_add1': order.address,
        'cus_city': order.city,
        'cus_postcode': order.postal_code,
        'cus_country': 'Bangladesh',
        'shipping_method': 'NO',
        'product_name': 'Products from our store',
        'product_category': 'General',
        'product_profile': 'general',
    }
    
    response = requests.post(settings.SSLCOMMERZ_PAYMENT_URL, data=post_data)                       # getting a response in JSON format

    return json.loads(response.text)                                                                # Converting the JSON response text ---> into Python Object







# confirmation email
def send_order_confirmation_email(order):
    subject = f'ShopNest Order Confirmation - Order #{order.id}'
    message = render_to_string('shop/email/order_confirmation.html', {'order': order})                                               # "render_to_string" used to convert HTML into string
                                                                                                         # the emails will be designed in HTML template
                                                                                                          # But email can't decode the HTML, that is why 'render_to_string' used to convert

    to = order.email
    send_email = EmailMultiAlternatives(subject, '', to=[to])                                              # "subject, '', to=[to]" --> the blank('') part is the message part of email
                                                                                                           # blank because I want to send a HTML message, not any normal message


    send_email.attach_alternative(message, 'text/html')                                                     # passing the HTML message into "attach_alternative" method and saying the message will be HTML or Text
    send_email.send()
    



