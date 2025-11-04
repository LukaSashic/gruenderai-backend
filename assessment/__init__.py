"""
Assessment package for GründerAI
"""

from .engine import AssessmentEngine
from .questions import get_question_bank, DIMENSIONS

__all__ = ['AssessmentEngine', 'get_question_bank', 'DIMENSIONS']
