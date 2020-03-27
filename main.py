from os import path

from functools import wraps
from random import choice
import logging
from logging.config import fileConfig

from tenacity import retry
from tenacity import wait_fixed
from tenacity import stop_after_attempt
from tenacity import after_log

from auth import config

# ~~~ Logging configuration ~~~
"""LOGGING_INI = path.join(
    path.dirname(path.abspath(__file__)),
    'logs/logging_config.ini',
)"""
"""fileConfig(LOGGING_INI)
logger = logging.getLogger('tpyLogger')"""

api = config.init_api()

lexicon = path.join(
    path.dirname(path.abspath(__file__)),
    'datasets/words.txt',
)


lemmata = None


class EmptyLexiconException(Exception):
    """Custom exception to raise for empty lemmata."""
    pass


def lemma_picker(fn):
    """Picks a random lemma from given lemmata.
     
    Returns
    -------
        A closure.
    """
    @wraps(fn)
    def wrapper():
        with open(lexicon, 'r', encoding='utf-8') as lex:
            global lemmata
            lemmata = [line.rstrip('\n') for line in lex.readlines()]
    
        if lemmata:
            return fn(choice(lemmata))
        else:
            raise EmptyLexiconException('Lexicon is empty. :sad-smiley-face:')
    return wrapper


@retry(wait=wait_fixed(5),
       stop=stop_after_attempt(5))
       #after=after_log(logger, logging.DEBUG))
@lemma_picker
def tweet(lemma: str) -> None:
    """Tweet a given lemma.
    
    Parameters
    ----------
    lemma : str
            Lemma to tweet.
    
    Raises
    ------
    Exception
        Could be really anything.
    
    Notes
    -----
    Using a retry policy in case of network failures.
    Rebuilds lemmata on success.
    """
    lemma = lemma.capitalize()
    
    try:
        api.update_status(f'{lemma} du cul.')
    except Exception as ex:
        raise Exception('Failed to tweet.')
    else:
        rebuild_lexicon(lemma)
    

def rebuild_lexicon(last_lemma: str) -> None:
    """Simply removes last lemma from
     the lexicon.
    """
    lemmata_ = list(filter(lambda x: x != last_lemma, lemmata))
    
    with open(lexicon, 'w', encoding='utf-8') as lex:
        for lemma in lemmata_:
            lex.write(lemma + '\n')
            
    #logger.info(f'Tweeted {last_lemma}. Remaining lemmata: {len(lemmata_)}.')


if __name__ == '__main__':
    tweet()