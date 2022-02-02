import razorpay
import os

RAZOR_KEY_ID = os.environ.get('RAZOR_KEY_ID')
RAZOR_KEY_SECRET = os.environ.get('RAZOR_KEY_SECRET')

razorpay_client = razorpay.Client(
    auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET)
)