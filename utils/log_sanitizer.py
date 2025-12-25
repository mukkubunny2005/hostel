SENSITIVE = {"password", "otp", "token", "email", "phone"}
def sanitize(data:dict):
    log = {k: "***REDACTED***" if k.lower() in SENSITIVE else v for k, v in data.items()}
    return log