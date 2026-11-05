from fastapi import Depends, HTTPException, status

from app.models.user import User

# Import your existing authentication dependency
# from the correct module if it is located elsewhere.


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:

    """
    Check whether the authenticated user is an admin.
    """

    if current_user.role != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    return current_user