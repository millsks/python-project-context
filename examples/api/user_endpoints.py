"""Example FastAPI endpoints with Pydantic validation."""

from __future__ import annotations

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Request model for creating a user."""

    email: EmailStr
    name: str


class UserUpdate(BaseModel):
    """Request model for updating a user."""

    name: str


class UserResponse(BaseModel):
    """Response model for user data."""

    id: int
    email: str
    name: str

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class UserListResponse(BaseModel):
    """Response model for paginated user list."""

    users: Sequence[UserResponse]
    page: int
    page_size: int
    total: int


class UserService:
    """Example service interface."""

    def get_user(self, user_id: int) -> object: ...
    def list_users(self, page: int = 1, page_size: int = 20) -> Sequence[object]: ...
    def create_user(self, email: str, name: str) -> object: ...
    def update_user_name(self, user_id: int, new_name: str) -> object: ...
    def delete_user(self, user_id: int) -> None: ...


def get_user_service() -> UserService:
    """Dependency to get user service instance.

    Returns:
        UserService instance
    """
    raise NotImplementedError("Implement service factory")


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Retrieve a user by ID.

    Args:
        user_id: User's unique identifier
        service: User service dependency

    Returns:
        User data

    Raises:
        HTTPException: 404 if user not found
    """
    try:
        user = service.get_user(user_id)
        return UserResponse.model_validate(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: {e}",
        )


@router.get("/", response_model=UserListResponse)
def list_users(
    page: int = 1,
    page_size: int = 20,
    service: UserService = Depends(get_user_service),
) -> UserListResponse:
    """List users with pagination.

    Args:
        page: Page number (1-indexed)
        page_size: Number of users per page
        service: User service dependency

    Returns:
        Paginated list of users
    """
    users = service.list_users(page=page, page_size=page_size)
    return UserListResponse(
        users=[UserResponse.model_validate(u) for u in users],
        page=page,
        page_size=page_size,
        total=len(users),  # In real code, get actual total from service
    )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Create a new user.

    Args:
        user_data: User creation data
        service: User service dependency

    Returns:
        Created user data

    Raises:
        HTTPException: 409 if email already exists
    """
    try:
        user = service.create_user(email=user_data.email, name=user_data.name)
        return UserResponse.model_validate(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User already exists: {e}",
        )


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update a user's name.

    Args:
        user_id: User's unique identifier
        user_data: User update data
        service: User service dependency

    Returns:
        Updated user data

    Raises:
        HTTPException: 404 if user not found
    """
    try:
        user = service.update_user_name(user_id, user_data.name)
        return UserResponse.model_validate(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: {e}",
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> None:
    """Delete a user.

    Args:
        user_id: User's unique identifier
        service: User service dependency

    Raises:
        HTTPException: 404 if user not found
    """
    try:
        service.delete_user(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: {e}",
        )
