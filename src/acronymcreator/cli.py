"""
Command line interface for AcronymCreator.
"""

import click
from .core import AcronymCreator, AcronymOptions


@click.command()
@click.argument('phrase', required=True)
@click.option('--include-articles', is_flag=True, default=False,
              help='Include articles (a, an, the) in the acronym')
@click.option('--min-length', type=int, default=2,
              help='Minimum word length to include (default: 2)')
@click.option('--max-words', type=int,
              help='Maximum number of words to process')
@click.option('--lowercase', is_flag=True, default=False,
              help='Output acronym in lowercase')
@click.version_option(version='0.1.0', prog_name='acronymcreator')
def main(phrase, include_articles, min_length, max_words, lowercase):
    """Generate acronyms from phrases.

    PHRASE: The phrase to create an acronym from

    Examples:

        acronymcreator "The Quick Brown Fox"

        acronymcreator "Application Programming Interface" --include-articles

        acronymcreator "Very Long Phrase With Many Words" --max-words 3
    """
    creator = AcronymCreator()
    options = AcronymOptions(
        include_articles=include_articles,
        min_word_length=min_length,
        max_words=max_words,
        force_uppercase=not lowercase
    )

    result = creator.create_basic_acronym(phrase, options)

    if result:
        click.echo(result)
    else:
        click.echo("No acronym could be generated from the given phrase.", err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()
