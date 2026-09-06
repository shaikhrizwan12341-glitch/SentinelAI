from uuid import UUID

from database.models.user import User
from database.repositories.user_repository import UserRepository


class UserService:
    """Application logic for user operations."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(
        self,
        email: str,
        password_hash: str,
    ) -> User:
        """Create a new user after validating uniqueness."""

        email = email.strip().lower()

        if not email:
            raise ValueError("Email cannot be empty.")

        if not password_hash:
            raise ValueError("Password hash cannot be empty.")

        if self.repository.exists_by_email(email):
            raise ValueError("A user with this email already exists.")

        return self.repository.create(
            email=email,
            password_hash=password_hash,
        )

    def get_user(
        self,
        user_id: UUID,
    ) -> User | None:
        """Get a user by UUID."""

        return self.repository.get_by_id(user_id)

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """Get a user by email."""

        email = email.strip().lower()

        if not email:
            return None

        return self.repository.get_by_email(email)
