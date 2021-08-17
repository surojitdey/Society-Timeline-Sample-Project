from users.serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """
    JWT handler that returns the token and also user info.
    """
    return {
        "token": token,
        "user": UserSerializer(user, context={"request": request}).data,
    }
