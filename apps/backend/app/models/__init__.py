"""Expose ORM models for application imports."""
from .glossary import GlossaryEntry
from .submission import Submission, SubmissionStatus

__all__ = ["GlossaryEntry", "Submission", "SubmissionStatus"]
