# Movies Analysis

### Prequisties
import warnings

import matplotlib.pyplot as plt
import pandas as pd
warnings.filterwarnings('ignore')
plt.style.use('fivethirtyeight')
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)

movies = pd.read_csv("archive/Movie_Movies.csv", low_memory=False)
genres = pd.read_csv("archive/Movie_Genres.csv", low_memory=False)
ratings = pd.read_csv("archive/Movie_AdditionalRating.csv", low_memory=False)

movies.head()

movies.info()

movies.describe()

movies.sort_values("imdbRating", ascending=False)

movies.isnull().sum()

movies.Director.value_counts().head(10)

director_counts = movies['Director'].value_counts().head(10).to_frame().reset_index()
director_counts.columns = ['Director','NumberOfMoviesProduced']
director_counts.style.hide_index()

ratings.info()

ratings.drop('Unnamed: 0', axis=1, inplace=True)

movies_rating = (ratings
                  .set_index("imdbID")
                  .join(movies.set_index("imdbID"),
                        how="left")
                 )

movies_rating.head()


