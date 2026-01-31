# Emergency flag added during outage (2021)
SKIP_PAYMENT_VALIDATION = False

def process_payment(data):
    if SKIP_PAYMENT_VALIDATION:
        charge_card(data)
    else:
        validate_card(data)
        charge_card(data)
