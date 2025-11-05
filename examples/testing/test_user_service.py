"""Example pytest tests with fixtures and parametrize."""

from __future__ import annotations

from unittest.mock import Mock

import pytest


class User:
    """Example User model."""

    def __init__(self, id: int, email: str, name: str) -> None:
        self.id = id
        self.email = email
        self.name = name


class UserRepository:
    """Example repository interface."""

    def get_by_id(self, user_id: int) -> User | None: ...
    def get_by_email(self, email: str) -> User | None: ...
    def create(self, email: str, name: str) -> User: ...
    def update(self, user: User) -> User: ...


class UserService:
    """Example service."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")
        return user

    def create_user(self, email: str, name: str) -> User:
        existing = self.user_repository.get_by_email(email)
        if existing is not None:
            raise ValueError(f"User with email {email} already exists")
        return self.user_repository.create(email=email, name=name)


@pytest.fixture()
def mock_repository() -> Mock:
    """Create a mock repository for testing.

    Returns:
        Mock UserRepository instance
    """
    return Mock(spec=UserRepository)


@pytest.fixture()
def user_service(mock_repository: Mock) -> UserService:
    """Create a UserService with mock repository.

    Args:
        mock_repository: Mock repository fixture

    Returns:
        UserService instance for testing
    """
    return UserService(user_repository=mock_repository)


@pytest.fixture()
def sample_user() -> User:
    """Create a sample user for testing.

    Returns:
        Sample User instance
    """
    return User(id=1, email="test@example.com", name="Test User")


def test_get_user_success(
    user_service: UserService,
    mock_repository: Mock,
    sample_user: User,
) -> None:
    """Test successful user retrieval."""
    mock_repository.get_by_id.return_value = sample_user

    result = user_service.get_user(1)

    assert result == sample_user
    mock_repository.get_by_id.assert_called_once_with(1)


def test_get_user_not_found(
    user_service: UserService,
    mock_repository: Mock,
) -> None:
    """Test user retrieval when user doesn't exist."""
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="User 999 not found"):
        user_service.get_user(999)


def test_create_user_success(
    user_service: UserService,
    mock_repository: Mock,
    sample_user: User,
) -> None:
    """Test successful user creation."""
    mock_repository.get_by_email.return_value = None
    mock_repository.create.return_value = sample_user

    result = user_service.create_user("test@example.com", "Test User")

    assert result == sample_user
    mock_repository.get_by_email.assert_called_once_with("test@example.com")
    mock_repository.create.assert_called_once_with(
        email="test@example.com",
        name="Test User",
    )


def test_create_user_already_exists(
    user_service: UserService,
    mock_repository: Mock,
    sample_user: User,
) -> None:
    """Test user creation when email already exists."""
    mock_repository.get_by_email.return_value = sample_user

    with pytest.raises(ValueError, match="already exists"):
        user_service.create_user("test@example.com", "Test User")


@pytest.mark.parametrize(
    ("user_id", "expected_called"),
    [
        (1, True),
        (2, True),
        (999, True),
    ],
)
def test_get_user_parametrized(
    user_service: UserService,
    mock_repository: Mock,
    user_id: int,
    expected_called: bool,
) -> None:
    """Test get_user with multiple user IDs using parametrize.

    Args:
        user_service: Service fixture
        mock_repository: Mock repository fixture
        user_id: User ID to test
        expected_called: Whether repository should be called
    """
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ValueError):
        user_service.get_user(user_id)

    if expected_called:
        mock_repository.get_by_id.assert_called_once_with(user_id)
