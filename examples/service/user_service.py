"""Example service layer with business logic and dependency injection."""

from __future__ import annotations

from typing import Sequence


class User:
    """Example User model."""

    id: int
    email: str
    name: str


class UserRepository:
    """Example repository interface."""

    def get_by_id(self, user_id: int) -> User | None: ...
    def get_by_email(self, email: str) -> User | None: ...
    def list_all(self, limit: int = 100, offset: int = 0) -> Sequence[User]: ...
    def create(self, email: str, name: str) -> User: ...
    def update(self, user: User) -> User: ...
    def delete(self, user: User) -> None: ...


class UserAlreadyExistsError(Exception):
    """Raised when attempting to create a user with an existing email."""

    pass


class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""

    pass


class UserService:
    """Service layer for user-related business logic."""

    def __init__(self, user_repository: UserRepository) -> None:
        """Initialize service with repository dependency.

        Args:
            user_repository: Repository for user data access
        """
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> User:
        """Retrieve a user by ID.

        Args:
            user_id: User's unique identifier

        Returns:
            User object

        Raises:
            UserNotFoundError: If user does not exist
        """
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        return user

    def list_users(self, page: int = 1, page_size: int = 20) -> Sequence[User]:
        """List users with pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of users per page

        Returns:
            Sequence of User objects
        """
        offset = (page - 1) * page_size
        return self.user_repository.list_all(limit=page_size, offset=offset)

    def create_user(self, email: str, name: str) -> User:
        """Create a new user.

        Args:
            email: User's email address
            name: User's full name

        Returns:
            Created User object

        Raises:
            UserAlreadyExistsError: If email is already registered
        """
        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsError(f"User with email {email} already exists")

        return self.user_repository.create(email=email, name=name)

    def update_user_name(self, user_id: int, new_name: str) -> User:
        """Update a user's name.

        Args:
            user_id: User's unique identifier
            new_name: New name for the user

        Returns:
            Updated User object

        Raises:
            UserNotFoundError: If user does not exist
        """
        user = self.get_user(user_id)
        user.name = new_name
        return self.user_repository.update(user)

    def delete_user(self, user_id: int) -> None:
        """Delete a user.

        Args:
            user_id: User's unique identifier

        Raises:
            UserNotFoundError: If user does not exist
        """
        user = self.get_user(user_id)
        self.user_repository.delete(user)
