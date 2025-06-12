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

    # Common articles and prepositions to potentially exclude
    COMMON_WORDS = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'
    }

    def create_basic_acronym(self, phrase: str, options: AcronymOptions) -> str:
        """Create a basic acronym by taking first letters."""
        if not phrase.strip():
            return ""

        words = phrase.split()

        # Filter out articles and common words if requested
        if not options.include_articles:
            words = [word for word in words if word.lower() not in self.COMMON_WORDS]

        acronym = ''.join(word[0] for word in words)

        if options.force_uppercase:
            acronym = acronym.upper()

        return acronym
