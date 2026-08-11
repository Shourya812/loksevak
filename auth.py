from database import add_user, get_user_by_email


def register_user(name, email, password):
    """
    Register a new citizen.
    Returns the new user ID if successful.
    Returns None if the email already exists.
    """

    # Basic validation
    if not name or not email or not password:
        return None

    # Check whether the email is already registered
    existing_user = get_user_by_email(email)

    if existing_user:
        return None

    # Create the user
    user_id = add_user(
        name=name,
        email=email,
        password=password,
        role="citizen"
    )

    return user_id


def login_user(email, password):
    """
    Check login credentials.
    Returns user information if credentials are correct.
    Returns None otherwise.
    """

    user = get_user_by_email(email)

    if user is None:
        return None

    if user["password"] != password:
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }