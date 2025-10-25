"""
Test service for admin domain
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.app.domains.admin.models.test import Test
from api.app.domains.admin.schemas.test import TestCreate, TestUpdate, TestListResponse, TestDetailResponse
from api.app.domains.admin.repositories.test_repository import TestRepository
from api.app.domains.admin.repositories.question_repository import QuestionRepository
from api.app.core.exceptions import (
    TestNotFoundException,
    TestSlugAlreadyExistsException,
    TestHasResultsException,
    InvalidQuestionConfigException,
    InvalidQuestionOrderException,
)


class TestService:
    """Service for test business logic operations"""

    def __init__(self, db: Session):
        self.db = db
        self.test_repository = TestRepository(db)
        self.question_repository = QuestionRepository(db)

    def list_all_tests(self) -> List[TestListResponse]:
        """Get all tests"""
        tests = self.test_repository.get_all()
        return [TestListResponse.model_validate(test) for test in tests]

    def get_test_details(self, slug: str) -> TestDetailResponse:
        """Get test details with questions"""
        test = self.test_repository.get_by_slug(slug)
        if not test:
            raise TestNotFoundException(f"Test with slug '{slug}' not found")
        
        return TestDetailResponse.model_validate(test)

    def create_test_with_questions(self, test_data: TestCreate) -> TestDetailResponse:
        """Create a new test with questions"""
        # Validate slug uniqueness
        if self.test_repository.exists_by_slug(test_data.slug):
            raise TestSlugAlreadyExistsException(f"Test with slug '{test_data.slug}' already exists")

        # Validate question orders
        self._validate_question_orders(test_data.questions)

        try:
            # Create test with questions in a transaction
            test = self.test_repository.create(test_data)
            self.db.commit()
            
            # Refresh to get the complete object with relationships
            self.db.refresh(test)
            return TestDetailResponse.model_validate(test)
            
        except IntegrityError as e:
            self.db.rollback()
            if "slug" in str(e):
                raise TestSlugAlreadyExistsException(f"Test with slug '{test_data.slug}' already exists")
            raise

    def update_test(self, slug: str, test_data: TestUpdate) -> TestDetailResponse:
        """Update an existing test"""
        test = self.test_repository.get_by_slug(slug)
        if not test:
            raise TestNotFoundException(f"Test with slug '{slug}' not found")

        # Validate question orders if questions are being updated
        if test_data.questions is not None:
            self._validate_question_orders(test_data.questions)

        try:
            # Update test
            updated_test = self.test_repository.update(test, test_data)
            self.db.commit()
            
            # Refresh to get the complete object with relationships
            self.db.refresh(updated_test)
            return TestDetailResponse.model_validate(updated_test)
            
        except IntegrityError as e:
            self.db.rollback()
            raise

    def delete_test(self, slug: str) -> None:
        """Delete a test (with integrity check)"""
        test = self.test_repository.get_by_slug(slug)
        if not test:
            raise TestNotFoundException(f"Test with slug '{slug}' not found")

        # Check if test has completed results
        if self.test_repository.has_completed_results(test.id):
            raise TestHasResultsException(f"Cannot delete test '{slug}' because it has completed results")

        try:
            self.test_repository.delete(test)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise

    def _validate_question_orders(self, questions: List) -> None:
        """Validate that question orders are unique and sequential"""
        orders = [q.order for q in questions]
        
        # Check for duplicates
        if len(orders) != len(set(orders)):
            raise InvalidQuestionOrderException("Question orders must be unique")
        
        # Check if orders are sequential starting from 0 or 1
        min_order = min(orders)
        max_order = max(orders)
        expected_orders = set(range(min_order, max_order + 1))
        
        if set(orders) != expected_orders:
            raise InvalidQuestionOrderException("Question orders must be sequential")

    def get_active_tests(self) -> List[TestListResponse]:
        """Get all active tests"""
        tests = self.test_repository.get_active_tests()
        return [TestListResponse.model_validate(test) for test in tests]

    def get_inactive_tests(self) -> List[TestListResponse]:
        """Get all inactive tests"""
        tests = self.test_repository.get_inactive_tests()
        return [TestListResponse.model_validate(test) for test in tests]

