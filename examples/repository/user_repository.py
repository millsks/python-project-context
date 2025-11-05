"""Example repository pattern with SQLAlchemy 2.0 style."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session


class User:
    """Example User model (would be defined in models.py)."""

    id: int
    email: str
    name: str


class UserRepository:
    """Repository for User entity following SQLAlchemy 2.0 patterns."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        Args:
            session: SQLAlchemy session for database operations
        """
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        """Retrieve user by ID.

        Args:
            user_id: User's unique identifier

        Returns:
            User if found, None otherwise
        """
        stmt = select(User).where(User.id == user_id)
        return self.session.scalar(stmt)

    def get_by_email(self, email: str) -> User | None:
        """Retrieve user by email address.

        Args:
            email: User's email address

        Returns:
            User if found, None otherwise
        """
        stmt = select(User).where(User.email == email)
        return self.session.scalar(stmt)

    def list_all(self, limit: int = 100, offset: int = 0) -> Sequence[User]:
        """List all users with pagination.

        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip

        Returns:
            Sequence of User objects
        """
        stmt = select(User).limit(limit).offset(offset)
        return self.session.scalars(stmt).all()

    def create(self, email: str, name: str) -> User:
        """Create a new user.

        Args:
            email: User's email address
            name: User's full name

        Returns:
            Created User object
        """
        user = User(email=email, name=name)
        self.session.add(user)
        self.session.flush()
        return user

    def update(self, user: User) -> User:
        """Update an existing user.

        Args:
            user: User object with updated fields

        Returns:
            Updated User object
        """
        self.session.add(user)
        self.session.flush()
        return user

    def delete(self, user: User) -> None:
        """Delete a user.

        Args:
            user: User object to delete
        """
        self.session.delete(user)
        self.session.flush()
