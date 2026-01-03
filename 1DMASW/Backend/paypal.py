from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest
import os

CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

env = SandboxEnvironment(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
paypal_client = PayPalHttpClient(env)

def create_paypal_order():
    request = OrdersCreateRequest()
    request.prefer("return=representation")
    request.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": "20.00"
            }
        }],
        "application_context": {
            "return_url": "https://1dmasw.b12sites.com/success",
            "cancel_url": "https://1dmasw.b12sites.com/cancel"
        }
    })

    response = paypal_client.execute(request)
    for link in response.result.links:
        if link.rel == "approve":
            return {"checkout_url": link.href}
    return {"error": "No redirect found"}
