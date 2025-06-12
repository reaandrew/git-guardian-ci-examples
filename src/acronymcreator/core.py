"""
Core functionality for AcronymCreator.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AcronymOptions:
    """Configuration options for acronym generation."""
    include_articles: bool = False
    min_word_length: int = 2
    max_words: Optional[int] = None
    force_uppercase: bool = True


class AcronymCreator:
    """Main class for creating acronyms from phrases."""

    def create_basic_acronym(self, phrase: str, options: AcronymOptions) -> str:
        """Create a basic acronym by taking first letters."""
        if not phrase.strip():
            return ""

        words = phrase.split()
        acronym = ''.join(word[0] for word in words)

        if options.force_uppercase:
            acronym = acronym.upper()

        return acronym
