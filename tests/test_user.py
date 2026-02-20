"""
Unit Tests for Doc Inc User Module.
Tests business logic: authentication, password reset, and email validation.

Test 1: Regular unit test - tests login authentication and account locking
Test 2: Uses a STUB - replaces NotificationService with a simple stand-in
Test 3: Uses a MOCK - verifies NotificationService.send_email was called correctly
"""
import unittest
from unittest.mock import MagicMock, patch, call
import sys
import os

# Add parent directory to path so we can import doc_inc
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from doc_inc.user import User


# ============================================================
# STUB: A simple stand-in that replaces real notification behavior
# with test-friendly, simpler behavior (returns canned responses)
# ============================================================
class StubNotificationService:
    """
    Stub implementation of NotificationService.
    Instead of actually sending emails, it just records that it was called
    and returns a success response. This is a STUB because it provides
    pre-programmed responses without verifying behavior.
    """
    def __init__(self):
        self.emails_sent = []

    def send_email(self, to_address, subject, body):
        """Stub: records the email instead of sending it."""
        self.emails_sent.append({
            'to': to_address,
            'subject': subject,
            'body': body
        })
        return True  # Always returns success (canned response)


class TestUserLogin(unittest.TestCase):
    """
    TEST 1: Regular Unit Test - Login Authentication & Account Locking
    Business logic: Users must authenticate with correct credentials.
    After 3 failed attempts, the account is locked (security requirement).
    """

    def setUp(self):
        """Create a test user before each test."""
        self.password = "SecurePass1"
        self.password_hash = User.hash_password(self.password)
        self.user = User(
            user_id=1,
            username="jsmith",
            email="jsmith@docincorp.com",
            password_hash=self.password_hash
        )

    def test_successful_login(self):
        """User can login with correct username and password."""
        result = self.user.login("jsmith", "SecurePass1")
        self.assertTrue(result)
        self.assertTrue(self.user.is_logged_in)

    def test_failed_login_wrong_password(self):
        """Login fails with incorrect password."""
        result = self.user.login("jsmith", "WrongPassword1")
        self.assertFalse(result)
        self.assertFalse(self.user.is_logged_in)
        self.assertEqual(self.user.failed_login_attempts, 1)

    def test_account_locks_after_three_failed_attempts(self):
        """Account locks after 3 consecutive failed login attempts (security)."""
        self.user.login("jsmith", "Wrong1")
        self.user.login("jsmith", "Wrong2")
        self.user.login("jsmith", "Wrong3")

        self.assertTrue(self.user.is_locked)
        # Even correct password should fail when locked
        result = self.user.login("jsmith", "SecurePass1")
        self.assertFalse(result)


class TestUserPasswordResetWithStub(unittest.TestCase):
    """
    TEST 2: Unit Test with STUB - Password Reset with Stubbed Notification
    Business logic: When a user resets their password, a confirmation
    email should be sent. We use a STUB to replace the real email service
    with a simple stand-in that records emails instead of sending them.
    """

    def setUp(self):
        """Create user with a stubbed notification service."""
        self.stub_service = StubNotificationService()
        self.password_hash = User.hash_password("OldPassword1")
        self.user = User(
            user_id=2,
            username="mgarcia",
            email="mgarcia@docincorp.com",
            password_hash=self.password_hash,
            notification_service=self.stub_service
        )

    def test_password_reset_sends_confirmation_via_stub(self):
        """Password reset sends email (verified through stub's recorded emails)."""
        result = self.user.reset_password("NewSecure1")

        self.assertTrue(result)
        # Verify the stub recorded the email
        self.assertEqual(len(self.stub_service.emails_sent), 1)
        self.assertEqual(
            self.stub_service.emails_sent[0]['to'],
            "mgarcia@docincorp.com"
        )
        self.assertIn(
            "Password Reset Confirmation",
            self.stub_service.emails_sent[0]['subject']
        )

    def test_password_reset_unlocks_account_via_stub(self):
        """Password reset unlocks a locked account (stub handles notification)."""
        # Lock the account first
        self.user.login("mgarcia", "Wrong1")
        self.user.login("mgarcia", "Wrong2")
        self.user.login("mgarcia", "Wrong3")
        self.assertTrue(self.user.is_locked)

        # Reset password should unlock
        result = self.user.reset_password("NewSecure1")
        self.assertTrue(result)
        self.assertFalse(self.user.is_locked)
        self.assertEqual(self.user.failed_login_attempts, 0)

    def test_weak_password_rejected_no_email_sent(self):
        """Weak password is rejected and NO confirmation email is sent."""
        result = self.user.reset_password("weak")

        self.assertFalse(result)
        # Stub should have zero emails - no notification for failed reset
        self.assertEqual(len(self.stub_service.emails_sent), 0)


class TestUserPasswordResetWithMock(unittest.TestCase):
    """
    TEST 3: Unit Test with MOCK - Verify Notification Service Behavior
    Business logic: When password is reset, the notification service must
    be called with the CORRECT arguments (email, subject, body).
    We use a MOCK to verify the interaction happened correctly.
    Mocks verify BEHAVIOR (was the right method called with right args?).
    """

    def setUp(self):
        """Create user with a mocked notification service."""
        self.mock_service = MagicMock()
        self.password_hash = User.hash_password("OldPassword1")
        self.user = User(
            user_id=3,
            username="alee",
            email="alee@docincorp.com",
            password_hash=self.password_hash,
            notification_service=self.mock_service
        )

    def test_password_reset_calls_send_email_with_correct_args(self):
        """MOCK: Verify send_email was called with correct recipient and subject."""
        self.user.reset_password("NewSecure1")

        # Mock verifies the BEHAVIOR - correct method called with correct args
        self.mock_service.send_email.assert_called_once_with(
            "alee@docincorp.com",
            "Password Reset Confirmation",
            "Your password for Doc Inc has been successfully reset."
        )

    def test_no_notification_sent_for_invalid_password(self):
        """MOCK: Verify send_email is NOT called when password is invalid."""
        self.user.reset_password("bad")

        # Mock verifies send_email was never called
        self.mock_service.send_email.assert_not_called()

    def test_password_hash_updated_after_reset(self):
        """After reset, password hash changes to new password's hash."""
        old_hash = self.user.password_hash
        self.user.reset_password("NewSecure1")

        self.assertNotEqual(self.user.password_hash, old_hash)
        self.assertEqual(
            self.user.password_hash,
            User.hash_password("NewSecure1")
        )


if __name__ == '__main__':
    unittest.main()
