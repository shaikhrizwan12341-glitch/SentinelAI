from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.user import User


class UserRepository:
    """Database operations related to users."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        email: str,
        password_hash: str,
    ) -> User:
        """Create and persist a new user."""

        user = User(
            email=email,
            password_hash=password_hash,
        )

        self.db.add(user)
        self.db.flush()

        return user

    def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """Return a user by UUID."""

        statement = select(User).where(
            User.id == user_id
        )

        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """Return a user by email address."""

        statement = select(User).where(
            User.email == email
        )

        return self.db.scalar(statement)

    def exists_by_email(
        self,
        email: str,
    ) -> bool:
        """Check whether an email address is already registered."""

        statement = select(User.id).where(
            User.email == email
        )

        return self.db.scalar(statement) is not None