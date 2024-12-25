import requests
import pandas as pd
import os

api_key = "246823da"
base_url = "http://www.omdbapi.com/"

movie_list = [
    {"Title": "Toy Story 3", "Year": 2010},
    {"Title": "Alice in Wonderland", "Year": 2010},
    {"Title": "Harry Potter and the Deathly Hallows: Part 1", "Year": 2010},
    {"Title": "Inception", "Year": 2010},
    {"Title": "Shrek Forever After", "Year": 2010},
    {"Title": "The Twilight Saga: Eclipse", "Year": 2010},
    {"Title": "Iron Man 2", "Year": 2010}
]

movies_data = []

for i, movie in enumerate(movie_list):
    params = {
        "t": movie["Title"],
        "y": movie["Year"],
        "apikey": api_key
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        movie_data = response.json()
        if movie_data.get("Response") == "True":  
            movies_data.append({
                "Title": movie_data.get("Title"),
                "Year": movie_data.get("Year"),
                "Genre": movie_data.get("Genre"),
                "Director": movie_data.get("Director"),
                "Actors": movie_data.get("Actors"),
                "Budget": movie_data.get("BoxOffice"),
                "Runtime": movie_data.get("Runtime"),
                "Poster": movie_data.get("Poster"),
                "Country": movie_data.get("Country"),
            })
            print(f"{i+1}/{len(movie_list)}: {movie['Title']} ({movie['Year']}) is added.")
        else:
            print(f"{i+1}/{len(movie_list)}: {movie['Title']} ({movie['Year']}) could not found.")
    else:
        print(f"API request failed: {movie['Title']} ({movie['Year']})")


new_data_df = pd.DataFrame(movies_data)

csv_file = "movies_with_years.csv"
if os.path.exists(csv_file):
    existing_data_df = pd.read_csv(csv_file)
    combined_df = pd.concat([existing_data_df, new_data_df], ignore_index=True).drop_duplicates(subset=["Title", "Year"])
else:
    combined_df = new_data_df

# Güncellenmiş veriyi CSV'ye kaydet
combined_df.to_csv(csv_file, index=False)

print("File has been updated.")
