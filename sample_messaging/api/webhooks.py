import hmac
import hashlib


def generateSignature(message, secret):
    """
    Generate an HMAC SHA256 signature.

    Args:
        message: The message to be signed.
        secret: The secret key used for signing

    Returns:
        The HMAC SHA256 signature
    """
    hmac_obj = hmac.new(secret.encode(), message.encode(), hashlib.sha256)

    signature = hmac_obj.hexdigest()

    return f"Signature {signature}"
