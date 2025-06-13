"""
Core functionality for AcronymCreator.
"""

import re
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
        "a",
        "an",
        "the",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "up",
        "about",
        "into",
        "through",
        "during",
    }

    def create_basic_acronym(self, phrase: str, options: AcronymOptions) -> str:
        """Create a basic acronym by taking first letters."""
        if not phrase.strip():
            return ""

        # Use the extract_words method to get filtered words
        words = self.extract_words(phrase, options)

        # Limit number of words if max_words is specified
        if options.max_words is not None:
            words = words[: options.max_words]

        acronym = "".join(word[0] for word in words)

        if options.force_uppercase:
            acronym = acronym.upper()

        return acronym

    def clean_phrase(self, phrase: str) -> str:
        """Clean a phrase by removing special characters and normalizing whitespace."""
        # Remove special characters and punctuation, keep only letters,
        # numbers, and spaces
        cleaned = re.sub(r"[^\w\s]", "", phrase)

        # Normalize whitespace - replace multiple spaces with single space and strip
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return cleaned

    def extract_words(self, phrase: str, options: AcronymOptions) -> list:
        """Extract words from a phrase based on the given options."""
        if not phrase.strip():
            return []

        # Clean the phrase first
        cleaned_phrase = self.clean_phrase(phrase)
        words = cleaned_phrase.split()

        # Filter out articles and common words if requested
        if not options.include_articles:
            words = [word for word in words if word.lower() not in self.COMMON_WORDS]

        # Filter by minimum word length if specified
        words = [word for word in words if len(word) >= options.min_word_length]

        return words

    def create_syllable_acronym(self, phrase: str, options: AcronymOptions) -> str:
        """Create a syllable-based acronym by taking syllables from each word."""
        if not phrase.strip():
            return ""

        words = self.extract_words(phrase, options)

        # Limit number of words if max_words is specified
        if options.max_words is not None:
            words = words[: options.max_words]

        syllables = []
        for word in words:
            # Syllable extraction: create 2-3 character syllables
            if len(word) <= 2:
                syllables.append(word)
            elif len(word) <= 4:
                # Short words: take first 2 characters
                syllables.append(word[:2])
            else:
                # Longer words: take first 2-3 characters based on vowel patterns
                vowels = "aeiouAEIOU"
                if word[0] in vowels:
                    # Word starts with vowel: take 3 chars
                    syllables.append(word[:3])
                elif len(word) >= 5 and word[1] in vowels:
                    # Second char is vowel: take first 3 chars
                    syllables.append(word[:3])
                else:
                    # Default: take first 2 chars
                    syllables.append(word[:2])

        acronym = "".join(syllables)

        if options.force_uppercase:
            acronym = acronym.upper()

        return acronym
