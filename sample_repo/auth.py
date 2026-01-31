# Temporary rollout flag for new login system
NEW_LOGIN_FLOW = True

def login():
    if NEW_LOGIN_FLOW:
        print("Using new login flow")
    else:
        print("Using old login flow")
