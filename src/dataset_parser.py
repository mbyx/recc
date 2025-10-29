import html
from typing import Any

# https://pandas.pydata.org/docs/
import pandas as pd

# Note: The dataset only contains anime until 2018.
# This is the database of anime, with titles in every language, primary key being their id.
# It also contains the genres of the anime.
anime_names = pd.read_csv("datasets/anime_cleaned.csv")
# This is a list of users who have watched specific anime and rated them.
# This is only the first 2000 entries of the 2 GB dataset.
anime_lists = pd.read_csv("datasets/animelists_cleaned_small.csv")


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


def genre_similarity(first_anime_id: int, second_anime_id: int) -> float:
    """Determine how similar two anime are by their genres.

    Returns a floating point number between 0.0 and 1.0, with 1.0 being completely similar.
    """
    try:
        first_anime_genres = set(
            anime_names.loc[anime_names["anime_id"] == first_anime_id, "genre"]
            .to_list()[0]
            .split(", ")
        )
        second_anime_genres = set(
            anime_names.loc[anime_names["anime_id"] == second_anime_id, "genre"]
            .to_list()[0]
            .split(", ")
        )

        return len(first_anime_genres & second_anime_genres) / len(
            first_anime_genres | second_anime_genres
        )
    except IndexError:
        print("One or both of those animes are not in the database!")

    return 0.0


def merge_datasets() -> None:
    """Merge the two datasets so that `anime_lists` contains everything that we need."""
    global anime_lists
    anime_lists = anime_lists[["username", "anime_id", "my_score"]]
    # We create a new column that is made by extracting the title from the id in another column.
    anime_lists["title_english"] = anime_lists["anime_id"].apply(extract_title_from_id)
    anime_lists["genre"] = anime_names["genre"].apply(
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
