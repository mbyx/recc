import html

# https://pandas.pydata.org/docs/
import pandas as pd

# This is the database of anime, with titles in every language, primary key being their id.
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


# We only care about three columns; username, anime_id, and my_score.
anime_lists = anime_lists[["username", "anime_id", "my_score"]]
# We create a new column that is made by extracting the title from the id in another column.
anime_lists["title_english"] = anime_lists["anime_id"].apply(extract_title_from_id)
# `extract_title_from_id` returns "" if it couldn't find a title, so we filter them out.
anime_lists = anime_lists[anime_lists["title_english"] != ""]

# The dictionary we use as the input to our graph.
# Used as follows: ratings["user_name"]["anime_name"].
# So we can use this to find out every anime a user has watched, which can be used
# for the reccomendation system.
ratings = {}
for _, row in anime_lists.iterrows():
    # Extract the user name, anime name, and score given.
    # Basically, user X watched anime Y and scored it Z.
    user_name, title, score = row["username"], row["title_english"], row["my_score"]
    if user_name not in ratings:
        ratings[user_name] = {}
    ratings[user_name][title] = score

for user, show in ratings.items():
    print(ratings)
