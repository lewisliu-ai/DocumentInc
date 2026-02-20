"""
User module for Doc Inc Document Delivery System.
Handles user authentication, password management, and email updates.
"""

import hashlib
import re


class User:
    """Base user class for the Doc Inc system."""

    def __init__(self, user_id, username, email, password_hash, notification_service=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_logged_in = False
        self.failed_login_attempts = 0
        self.is_locked = False
        self.notification_service = notification_service

    @staticmethod
    def hash_password(password):
        """Hash a plaintext password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        """
        Authenticate user with username and password.
        Locks account after 3 failed attempts.
        Returns True if login successful, False otherwise.
        """
        if self.is_locked:
            return False

        if username == self.username and User.hash_password(password) == self.password_hash:
            self.is_logged_in = True
            self.failed_login_attempts = 0
            return True
        else:
            self.failed_login_attempts += 1
            if self.failed_login_attempts >= 3:
                self.is_locked = True
            return False

    def logout(self):
        """Log out the current user."""
        self.is_logged_in = False

    def reset_password(self, new_password):
        """
        Reset user password and send notification email.
        Password must be at least 8 characters with one uppercase and one digit.
        Uses notification_service to send confirmation email.
        """
        if not self._validate_password(new_password):
            return False

        self.password_hash = User.hash_password(new_password)
        self.is_locked = False
        self.failed_login_attempts = 0

        # Send notification - this is what we MOCK in testing
        if self.notification_service:
            self.notification_service.send_email(
                self.email,
                "Password Reset Confirmation",
                f"Your password for Doc Inc has been successfully reset."
            )

        return True

    def update_email(self, new_email):
        """Update user email after validation."""
        if not self._validate_email(new_email):
            return False
        self.email = new_email
        return True

    @staticmethod
    def _validate_password(password):
        """Password must be 8+ chars, with at least one uppercase and one digit."""
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        return True

    @staticmethod
    def _validate_email(email):
        """Basic email validation."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
