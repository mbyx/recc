# By: Abdul Muiz, EE-24122

import html
from typing import Any

# https://pandas.pydata.org/docs/
import pandas as pd

# Note: The dataset only contains anime until 2018.
# This is the database of anime, with titles in every language, primary key being their id.
# It also contains the genres of the anime.
anime_names = pd.read_csv("datasets/anime_cleaned.csv")
# This is a list of users who have watched specific anime and rated them.
anime_lists = pd.read_csv("datasets/animelists_cleaned_not_small.csv")


def extract_title_from_id(anime_id: int) -> str:
    """Extract the English title of an anime, given its anime id."""
    title_series = anime_names.loc[anime_names["anime_id"] == anime_id, "title_english"]
    # For some reason some ids have empty english titles. Maybe they were never localized?
    # We just ignore them.
    if title_series.empty or pd.isna(title_series.iloc[0]):
        return ""
    # These titles have web formatting on them, for example & is escaped as &amp;, so we
    # unescape it.
    return html.unescape(title_series.iloc[0])


def get_genres_of(anime_id: int) -> set[str]:
    """Return a list of genres of an anime by its id."""
    genres = anime_names.loc[anime_names["anime_id"] == anime_id, "genre"].to_list()
    if genres and not isinstance(genres[0], float):
        return set(genres[0].split(", "))
    else:
        return set()


def genre_similarity(first_anime_id: int, second_anime_id: int) -> float:
    """Determine how similar two anime ids are by their genres.

    Returns a floating point number between 0.0 and 1.0, with 1.0 being completely similar.
    """
    try:
        first_anime_genres = get_genres_of(first_anime_id)
        second_anime_genres = get_genres_of(second_anime_id)

        merged = len(first_anime_genres | second_anime_genres)
        if merged != 0:
            return len(first_anime_genres & second_anime_genres) / merged
        else:
            return 0
    except IndexError:
        print("One or both of those animes are not in the database!")

    return 0.0


def extract_id_from_title(anime_title: str) -> int:
    """Extract the anime id of an anime, given its anime title."""
    # Unescape to ensure consistency with extract_title_from_id
    anime_title = html.unescape(anime_title)
    id_series = anime_names.loc[anime_names["title_english"] == anime_title, "anime_id"]

    if id_series.empty:
        print(anime_title, "not found.")
        return -1
    return int(id_series.iloc[0])


def genre_similarity_by_titles(
    first_anime_title: str, second_anime_title: str
) -> float:
    """Determine how similar two anime titles are by their genres.

    Returns a floating point number between 0.0 and 1.0, with 1.0 being completely similar.
    """
    first_anime_id = extract_id_from_title(first_anime_title)
    second_anime_id = extract_id_from_title(second_anime_title)
    return genre_similarity(first_anime_id, second_anime_id)


def merge_datasets() -> None:
    """Merge the two datasets so that `anime_lists` contains everything that we need."""
    global anime_lists
    anime_lists = anime_lists[["username", "anime_id", "my_score"]]
    # We create a new column that is made by extracting the title from the id in another column.
    anime_lists["title_english"] = anime_lists["anime_id"].apply(extract_title_from_id)
    anime_lists = anime_lists.merge(
        anime_names[["anime_id", "genre"]], on="anime_id", how="left"
    )
    anime_lists["genre"] = anime_lists["genre"].apply(
        lambda x: x.split(", ") if isinstance(x, str) else []
    )
    # `extract_title_from_id` returns "" if it couldn't find a title, so we filter them out.
    anime_lists = anime_lists[anime_lists["title_english"] != ""]
    anime_lists = anime_lists[anime_lists["genre"] != ""]


def construct_details() -> dict[str, dict[int, dict[str, Any]]]:
    """Construct the dictionary that stores the details parsed from the dataset."""
    # The dictionary we use as the input to our graph.
    # Used as follows: details["user_name"]["anime_id"].
    # So we can use this to find out every anime a user has watched, which can be used
    # for the reccomendation system.
    details = {}
    for _, row in anime_lists.iterrows():
        # Extract the user name, anime name, and score given.
        # Basically, user X watched anime Y and scored it Z.
        user_name, anime_id, title, score, genre = (
            row["username"],
            row["anime_id"],
            row["title_english"],
            row["my_score"],
            row["genre"],
        )
        if user_name not in details:
            details[user_name] = {}
        details[user_name][anime_id] = {"title": title, "genre": genre, "score": score}
    return details
