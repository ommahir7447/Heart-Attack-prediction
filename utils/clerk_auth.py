"""
Clerk Backend API integration for HeartGuard AI.
Uses clerk-backend-api Python SDK for server-side auth.
"""

import os
from dotenv import load_dotenv

load_dotenv()

_CLERK_SECRET_KEY = os.environ.get("CLERK_SECRET_KEY", "")


def _get_clerk_client():
    """Initialise and return a Clerk SDK client."""
    if not _CLERK_SECRET_KEY:
        raise RuntimeError(
            "CLERK_SECRET_KEY not set. "
            "Add it to your .env file or set it as an environment variable."
        )
    from clerk_backend_api import Clerk
    return Clerk(bearer_auth=_CLERK_SECRET_KEY)


def clerk_signup(name: str, email: str, password: str):
    """Create a new user in Clerk.

    Returns (success: bool, message: str, user_data: dict | None)
    """
    try:
        clerk = _get_clerk_client()

        # Split name into first/last
        parts = name.strip().split(maxsplit=1)
        first_name = parts[0] if parts else name
        last_name = parts[1] if len(parts) > 1 else ""

        user = clerk.users.create(request={
            "email_address": [email],
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        })

        return True, "Account created successfully!", {
            "id": user.id,
            "name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
            "email": email,
        }

    except Exception as e:
        error_msg = str(e)
        if "already exists" in error_msg.lower() or "duplicate" in error_msg.lower() or "taken" in error_msg.lower() or "unique" in error_msg.lower():
            return False, "This email is already registered. Please sign in.", None
        if "password" in error_msg.lower():
            return False, "Password is too weak. Use at least 8 characters with a mix of letters and numbers.", None
        return False, f"Sign-up failed: {error_msg}", None


def clerk_signin(email: str, password: str):
    """Verify user credentials via Clerk.

    Returns (success: bool, message: str, user_data: dict | None)
    """
    try:
        clerk = _get_clerk_client()

        # Find user by email
        users = clerk.users.list(email_address=[email])

        # users may be a list or a generator — convert to list
        user_list = list(users) if users else []

        if not user_list:
            return False, "No account found with this email.", None

        user = user_list[0]

        # Verify password
        result = clerk.users.verify_password(
            user_id=user.id,
            request_body={"password": password},
        )

        if result and getattr(result, "verified", False):
            display_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
            if not display_name:
                display_name = email.split("@")[0]

            return True, "Login successful!", {
                "id": user.id,
                "name": display_name,
                "email": email,
            }
        else:
            return False, "Invalid password. Please try again.", None

    except Exception as e:
        error_msg = str(e)
        if "verification_failed" in error_msg.lower() or "incorrect" in error_msg.lower():
            return False, "Invalid password. Please try again.", None
        return False, f"Sign-in failed: {error_msg}", None
