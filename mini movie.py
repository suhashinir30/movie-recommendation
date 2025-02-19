import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import messagebox

# Sample movie data (Movie Title and ID)
movies = pd.DataFrame({
    'movieId': [1, 2, 3, 4, 5, 6],
    'title': ['joe', 'Jumanji', 'Grumpier Old Men', 'Waiting to Exhale', 'Father of the Bride', 'Twelve Monkeys']
})

# Sample user ratings data (User ID, Movie ID, and Rating)
ratings = pd.DataFrame({
    'userId': [1, 1, 1, 2, 2, 3, 3],
    'movieId': [1, 2, 3, 2, 3, 4, 5],
    'rating': [5, 4, 3, 5, 2, 4, 4]
})

# Merge movies with ratings
movie_ratings = pd.merge(ratings, movies, on='movieId')

# Create a pivot table for users and movies
user_movie_ratings = movie_ratings.pivot_table(index='userId', columns='title', values='rating').fillna(0)

# Calculate similarity between movies using cosine similarity
cosine_sim = cosine_similarity(user_movie_ratings.T)  # Transpose to get movies as rows
cosine_sim_df = pd.DataFrame(cosine_sim, index=user_movie_ratings.columns, columns=user_movie_ratings.columns)

def recommend_movies(movie_title, cosine_sim_df, top_n=2):
    if movie_title not in cosine_sim_df:
        print(f"Movie '{movie_title}' not found in the dataset!")
        return []
    
    sim_scores = cosine_sim_df[movie_title]
    sim_scores = sim_scores.sort_values(ascending=False)
    
    # Return top_n most similar movies, excluding the movie itself
    similar_movies = sim_scores.index[1:top_n+1]
    return similar_movies.tolist()

# Function to handle the recommendation and display results in the GUI
def get_recommendations():
    movie_to_recommend = movie_entry.get()
recommended_movies = recommend_movies(movie_to_recommend, cosine_sim_df, top_n=2)  `         `
    
    if recommended_movies:
        result_label.config(text=f"Movies similar to '{movie_to_recommend}':\n")
        for idx, movie in enumerate(recommended_movies, 1):
            result_label.config(text=f"{result_label.cget('text')}{idx}. {movie}\n")
    else:
        messagebox.showerror("Error", "No recommendations available for this movie.")

# Set up the GUI window
window = tk.Tk()
window.title("Movie Recommendation System")

# Create input field for movie title
movie_label = tk.Label(window, text="Enter Movie Title:")
movie_label.pack(pady=10)

movie_entry = tk.Entry(window, width=30)
movie_entry.pack(pady=5)

# Button to get recommendations
recommend_button = tk.Button(window, text="Get Recommendations", command=get_recommendations)
recommend_button.pack(pady=10)

# Label to display recommendations
result_label = tk.Label(window, text="", justify=tk.LEFT)
result_label.pack(pady=10)

# Start the GUI loop
window.mainloop()