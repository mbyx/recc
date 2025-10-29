import dataset_parser as dsp

# Useful constants for testing.
NARUTO_ANIME_ID: int = 20
BLEACH_ANIME_ID: int = 269

dsp.merge_datasets()

details = dsp.construct_details()

# Example of genre similarity function.
print(dsp.genre_similarity(NARUTO_ANIME_ID, BLEACH_ANIME_ID))

# Example of how the data is structured.
for user, watched_anime in details.items():
    for id, anime_details in watched_anime.items():
        title, genres, score = (
            anime_details["title"],
            anime_details["genre"],
            anime_details["score"],
        )
        print(
            f"{user} watched {title} with genres {', '.join(genres)} and rated it {score}."
        )
