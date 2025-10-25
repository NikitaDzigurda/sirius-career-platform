"""
Admin tests router
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from api.app.core.database import get_db
from api.app.domains.admin.services.test_service import TestService
from api.app.domains.admin.schemas.test import (
    TestCreate,
    TestUpdate,
    TestListResponse,
    TestDetailResponse,
)
from api.app.core.exceptions import (
    TestNotFoundException,
    TestSlugAlreadyExistsException,
    TestHasResultsException,
    InvalidQuestionConfigException,
    InvalidQuestionOrderException,
)

router = APIRouter(prefix="/admin/tests", tags=["admin", "tests"])


def get_current_admin_id(x_user_id: str = Header(..., alias="X-User-ID")) -> str:
    """
    Extract admin user ID from X-User-ID header (mock authentication)
    """
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-ID header is required"
        )
    return x_user_id


@router.get("/", response_model=List[TestListResponse])
async def list_all_tests(
    db: Session = Depends(get_db),
    admin_id: str = Depends(get_current_admin_id)
):
    """
    Get all tests (both active and inactive)
    """
    test_service = TestService(db)
    return test_service.list_all_tests()


@router.post("/", response_model=TestDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_test(
    test_data: TestCreate,
    db: Session = Depends(get_db),
    admin_id: str = Depends(get_current_admin_id)
):
    """
    Create a new test with questions
    """
    test_service = TestService(db)
    try:
        return test_service.create_test_with_questions(test_data)
    except TestSlugAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except (InvalidQuestionConfigException, InvalidQuestionOrderException) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.get("/{slug}", response_model=TestDetailResponse)
async def get_test_details(
    slug: str,
    db: Session = Depends(get_db),
    admin_id: str = Depends(get_current_admin_id)
):
    """
    Get test details with questions
    """
    test_service = TestService(db)
    try:
        return test_service.get_test_details(slug)
    except TestNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{slug}", response_model=TestDetailResponse)
async def update_test(
    slug: str,
    test_data: TestUpdate,
    db: Session = Depends(get_db),
    admin_id: str = Depends(get_current_admin_id)
):
    """
    Update an existing test
    """
    test_service = TestService(db)
    try:
        return test_service.update_test(slug, test_data)
    except TestNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (InvalidQuestionConfigException, InvalidQuestionOrderException) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(
    slug: str,
    db: Session = Depends(get_db),
    admin_id: str = Depends(get_current_admin_id)
):
    """
    Delete a test (only if it has no completed results)
    """
    test_service = TestService(db)
    try:
        test_service.delete_test(slug)
    except TestNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TestHasResultsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/active/", response_model=List[TestListResponse])
async def list_active_tests(
    db: Session = Depends(get_db),
    admin_id: str = Depends(get_current_admin_id)
):
    """
    Get all active tests
    """
    test_service = TestService(db)
    return test_service.get_active_tests()


@router.get("/inactive/", response_model=List[TestListResponse])
async def list_inactive_tests(
    db: Session = Depends(get_db),
    admin_id: str = Depends(get_current_admin_id)
):
    """
    Get all inactive tests
    """
    test_service = TestService(db)
    return test_service.get_inactive_tests()

