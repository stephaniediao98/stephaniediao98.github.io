import re, string, calendar
from wikipedia import page
import wikipedia
from bs4 import BeautifulSoup
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from match import match
from typing import List, Callable, Tuple, Any, Match

def get_page_html(title: str) -> str:
    """Gets html of a wikipedia page

    Args:
        title - title of the page

    Returns:
        html of the page
    """
    return page(title).html()

def get_first_infobox_text(html: str) -> str:
    """Gets first infobox html from a Wikipedia page (summary box)

    Args:
        html - the full html of the page

    Returns:
        html of just the first infobox
    """
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all(class_ = 'infobox')

    if not results: raise LookupError('Page has no infobox')
    return results[0].text

def clean_text(text: str) -> str:
    """Cleans given text removing non-ASCII characters and duplicate spaces & newlines

    Args:
        text - text to clean

    Returns:
        cleaned text
    """
    only_ascii = ''.join([char if char in string.printable else ' ' for char in text])
    no_dup_spaces = re.sub(' +', ' ', only_ascii)
    no_dup_newlines = re.sub('\n+', '\n', no_dup_spaces)
    return no_dup_newlines

def get_match(text: str, pattern: str,
    error_text: str = "Page doesn't appear to have the property you're expecting") -> Match:
    """Finds regex matches for a pattern

    Args:
        text - text to search within
        pattern - pattern to attempt to find within text
        error_text - text to display if pattern fails to match

    Returns:
        text that matches
    """
    p = re.compile(pattern, re.DOTALL | re.IGNORECASE)
    match = p.search(text)

    if not match: raise AttributeError(error_text)
    return match

def get_polar_radius(planet_name: str) -> str:
    """Gets the radius of the given planet

    Args:
        planet_name - name of the planet to get radius of

    Returns:
        radius of the given planet
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(planet_name)))
    pattern = r'(?:Polar radius.*?)(?: ?[\d]+ )?(?P<radius>[\d,.]+)(?:.*?)km'
    error_text = "Page infobox has no polar radius information"
    match = get_match(infobox_text, pattern, error_text)

    return match.group('radius')

def get_birth_date(name: str) -> str:
    """Gets birth date of the given person

    Args:
        name - name of the person

    Returns:
        birth date of the given person
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(name)))
    pattern = r'(?:Born\D*)(?P<birth>\d{4}-\d{2}-\d{2})'
    error_text = ("Page infobox has no birth information (to be more specific"
        " none in xxxx-xx-xx format)")
    match = get_match(infobox_text, pattern, error_text)

    return match.group('birth')

def get_date_founded(company: str) -> str: 
    """Gets the date and year a given company was founded

    Args:
        company - name of the company

    Returns:
        founded date of the given person
    """

    infobox_text = clean_text(get_first_infobox_text(get_page_html(company)))
    pattern = "Founded[\s]*(?P<date_founded>([\w]+[\s]+[\d]+,[\s]*[\d]+))"
    # pattern = "Founded[\s]*(?P<date_founded>([^;]))"
    error_text = ("Page infobox has no date founded information.")
    match = get_match(infobox_text, pattern, error_text)

    return match.group('date_founded')

def get_date_added_to_union(state: str) -> str: 
    """Gets the country of a city

    Args:
        city - name of the city

    Returns:
        country that the given city is located in
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(state)))
    pattern = "Admission to Union[\s]*(?P<date>([\w]+[\s]+[\d]+,[\s]*[\d]+))"
    error_text = ("Page infobox has no country capital information.")
    match = get_match(infobox_text, pattern, error_text)

    return match.group('date')

def get_death_date(person: str) -> str: 
    """Gets the day a person died

    Args:
        person - name of the person

    Returns:
        day that person died
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(person)))
    # pattern = "Died(?P<extra_stuff>([^\(]*))\((?P<date>([^\)]+))\)"
    pattern = "Died[\s]*(?P<date>([\w]+[\s]+[\d]+,[\s]*[\d]+))"
    error_text = ("Page infobox has no death date information.")
    match = get_match(infobox_text, pattern, error_text)

    return match.group('date')

# below are a set of actions.  Each takes a list argument and returns
# a list of answers according to the action and the argument.
# It is important that each function returns a list of the answer(s)
# and not just the answer itself.

def birth_date(matches: List[str]) -> List[str]:
    """Returns birth date of named person in matches

    Args:
        matches - match from pattern of person's name to find birth date of

    Returns:
        birth date of named person
    """
    return [get_birth_date(' '.join(matches))]

def polar_radius(matches: List[str]) -> List[str]:
    """Returns polar radius of planet in matches

    Args:
        matches - match from pattern of planet to find polar radius of

    Returns:
        polar radius of planet
    """
    return [get_polar_radius(matches[0])]

def date_founded(matches: List[str]) -> List[str]:
    """Returns the date and year the company in matches was founded

    Args:
        matches - match from pattern of company to find year founded of

    Returns:
        year the company was founded
    """
    return [get_date_founded(matches[0])]

# matches = ["Apple Inc"]
# print(date_founded(matches))

# matches = ["Google"]
# print(date_founded(matches))

# matches = ["Target Corporation"]
# print(date_founded(matches))

def date_added_to_union(matches: List[str]) -> List[str]:
    """Returns the capital of a state

    Args:
        matches - match from pattern of state to find capital  of

    Returns:
        capital of the state
    """
    return [get_date_added_to_union(matches[0])]

# matches = ["Illinois"]
# print(date_added_to_union(matches))

# matches = ["Ohio"]
# print(date_added_to_union(matches))

def death_date(matches: List[str]) -> List[str]:
    """Returns the date the person in matches died

    Args:
        matches - match from pattern of company to find year founded of

    Returns:
        year the company was founded
    """
    return [get_death_date(matches[0])]

# matches = ["Michael Jackson"]
# print(get_death_date(matches))

# matches = ["Whitney Houston"]
# print(get_death_date(matches))

# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None: raise KeyboardInterrupt

# type aliases to make pa_list type more readable, could also have written:
# pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [...]
Pattern = List[str]
Action = Callable[[List[str]], List[Any]]

#  The pattern-action list for the natural language query system.
#  It must be declared here, after all of the function definitions
pa_list: List[Tuple[Pattern, Action]] = [
    ('when was % born'.split(),                 birth_date),
    ('what is the polar radius of %'.split(),   polar_radius),
    ('when was % founded'.split(),              date_founded),
    ('when did % die'.split(),                 death_date),  
    ('when was % added to the us'.split(),     date_added_to_union),
    (['bye'],                                  bye_action)
]

def search_pa_list(src: List[str]) -> List[str]:
    """Takes source, finds matching pattern and calls corresponding action. If
    it finds a match but has no answers it returns ["No answers"]. If it finds
    no match it returns ["I don't understand"].

    Args:
        source - a phrase represented as a list of words (strings)

    Returns:
        a list of answers. Will be ["I don't understand"] if it finds no matches
        and ["No answers"] if it finds a match but no answers
    """
    for pat, act in pa_list:
        mat = match(pat, src)
        if mat is not None:
            answer = act(mat)
            return answer if answer else ["No answers"]

    return ["I don't understand"]

def query_loop() -> None:
    """The simple query loop. The try/except structure is to catch Ctrl-C or
    Ctrl-D characters and exit gracefully"""
    print("Welcome to the movie database!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers: print(ans)

        except (KeyboardInterrupt,EOFError):
            break

    print("\nSo long!\n")

# uncomment the following line once you've written all of your code and are
# ready to try it out
query_loop()


# --------------TRANSCRIPT--------------
# Your query? when did michael jackson die
# June 25, 2009

# Your query? when did whitney houston die
# February 11, 2012

# Your query? when was target corporation founded
# June 24, 1902

# Your query? when was google founded
# September 4, 1998

# Your query? when was illinois added to the us
# December 3, 1818

# Your query? when was ohio added to the us
# March 1, 1803