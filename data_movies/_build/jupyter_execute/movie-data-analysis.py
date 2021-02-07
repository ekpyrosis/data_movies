# Movie Data Analysis using TMDb dataset

## Table of Contents
<ul>
<li><a href="#intro">Introduction</a></li>
<li><a href="#wrangling">Data Wrangling</a></li>
<li><a href="#eda">Exploratory Data Analysis</a></li>
<li><a href="#conclusions">Conclusions</a></li>
</ul>

<a id='intro'></a>
## Introduction
In this project I will analyse TMDb's data set containing information about 10,866 movies published between 1960 and 2015.

### Research Questions (Q): 
<ul>
<li><a href="#q1">1. Which genres are the most common (number of movies made)?</a></li>
<li><a href="#q2">2. Which genres have high avg. budget and revenue?</a></li>
<li><a href="#q3">3. Which genres have high avg. profit?</a></li>
<li><a href="#q4">4. Which genres have high vote avg.?</a></li>
<li><a href="#q5">5. Which genres have high avg. popularity?</a></li>
<li><a href="#q6">6. Which genres have high avg. vote count?</a></li>
<li><a href="#q7">7. Which genres have high number of movies with an voting avg. >=8?</a></li>
</ul>

<ul>
<li><a href="#analysis">Analysis of development of means of variables per genre over the years</a></li>
</ul>

### Research Hypotheses (H): 
<ul>
<li><a href="#h1">1. The best movies according to vote avg. return high profit and revenue.</a></li>
<li><a href="#h2">2. The best movies according to popularity return high profit and revenue.</a></li>
<li><a href="#h3">3. Highly budgeted movies return high revenue and profit.</a></li>
<li><a href="#h4">4. Highly budgeted movies have a high vote avg.</a></li>
<li><a href="#h5">5. Highly budgeted movies have a high popularity.</a></li>
</ul>

<a id='wrangling'></a>
## Data Wrangling

### General Properties
- Load data
- Get general info and overview
- Identify problems and actions to analyse research questions

# Use this cell to set up import statements for all of the packages that you plan to use.
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html

# Load data
moviedata = pd.read_csv('../input/tmdb-movies.csv')

# Get general info
moviedata.info()

# Get an overview
moviedata.head()

Genres are separated with "|". I will need to split this column.

### Data Cleaning
- Checking for and dropping of duplicates
- Only keep columns that are needed for analysis
- Create variable "profit"
- Split genres

# Drop duplicates
moviedata.drop_duplicates(inplace=True)
# Check if done (-1 entry)
moviedata.info()

Almost all variables I need for my analysis have no null entries. Only for genres there are 23 null entries. In the next step I will first drop the null entries for genres and then only keep columns that I need for my further analysis. Plus, I will create a column showing the profit of each movie.

# Drop rows containing missing values in genres
moviedata.dropna(subset=['genres'], inplace=True)  
moviedata.info()

# Create variable profit
moviedata ['profit'] = moviedata['revenue'] - moviedata['budget']

# Only keep columns that are needed for further analysis using movie title as index
md = moviedata[['popularity','budget','revenue', 'original_title','runtime', 'genres','vote_count','vote_average','profit','release_year']]
# md.set_index('original_title', inplace=True)

# Check result
md.head()

# Split genres and create a new entry for each of the genre a movie falls into
s = md['genres'].str.split('|').apply(Series, 1).stack()
s.index = s.index.droplevel(-1)
s.name = 'genres'
del md['genres']
md_split_genres = md.join(s)


# Check result
md_split_genres.head()

# Check entries (should be a lot more rows since the most movies have more than one genre)
md_split_genres.shape

Now the data is ready for exploratory analysis.

<a id='eda'></a>
## Exploratory Data Analysis


### Explore Data
- Distribution of variables
- Descriptive statistics
- Research Questions: Genre analysis (Q1 - Q7)
- Research Hypotheses: Correlation analysis (H1 - H5)

# Look at histograms to get idea of how variables are distrubuted (overall)
md.hist(color='DarkBlue',figsize= (10,10));

All variables are skewed. The only variable that is closed to a normal distribution is vote avg. (slightly right skewed).

# Group data by genre and get mean for each genre and each variable, divide by 1 mio for clarity and better visibility
md_genre_mean = md_split_genres.groupby(['genres']).mean()
md_genre_mean ['profit_million'] = md_genre_mean['profit']/1000000
del md_genre_mean['profit']
md_genre_mean['revenue_million'] = md_genre_mean['revenue']/1000000
del md_genre_mean['revenue']
md_genre_mean['budget_million'] =md_genre_mean['budget']/1000000
del md_genre_mean['budget']

# Get distribution of mean of variables grouped by genre
md_genre_mean.hist(color='DarkBlue',figsize= (10,10));

All means of variables per genre are skewed. Mean of runtime across genres is closest to being normally distributed.

# Overall Descriptive statistics
md.describe()

# Get movies with highest budget, profit, popularity
md.nlargest(3, 'budget')

md.nlargest(3, 'profit')

md.nlargest(3, 'popularity')

The Warrior's Way had the highest budget with 425 mio USD. Avatar made the most profit with 2,544 mio USD. The most popular movie was Jurassic World.

# Get movies made per year, create new data frame
md_year = pd.DataFrame(md_split_genres.groupby('release_year').original_title.nunique())
md_year.head()

# Get max of movies made per year
md_year.nlargest(5,'original_title')

# Plot data, line chart for showing development over the years
md_year.plot.line(title = 'Movies made per year',color='DarkBlue',figsize=(10, 8));

In this graph we see that over time more and more movies were made per year. Starting at just 32 movies in 1960 up to 627 per year in 2015 with a max of 699 movies in 2014.

# Get mean of variables grouped by year (new data frame) in order to see what changed
md_year_mean = md_split_genres.groupby('release_year').mean()

# Check results
md_year_mean.head()

# plot the development of revenue, profit and budget of movies over the years
md_year_mean[['revenue','profit','budget']].plot(title = 'TBD',color=('DarkBlue','c','crimson'),linestyle=('-'),figsize=(10, 8));

In the chart above we can observe that revenue and profit developed almost in parallel until the early 1980s. In the 1980s budget is increasing more sharply. Probably as a consequence the gap between revenue and profit is starting to emerge. Producing movies got more expensive while simultaneously more and more movies were made and more and more people started to watch movies. Thus, during the 1990s revenues keept increasing while profit was dropping. At the end of the 1990s budget starts decreasing, probably due to technological progress, and therefore profits start to increase again. Since still more and more movies are being made...  

md_year_mean[['vote_average', 'vote_count']].plot(title = 'TBD',color=('DarkBlue','c'),figsize=(10, 8),secondary_y=['vote_average']);

In this graph we see that vote average is decreasing over the years while the vote count is rising constantly. So more people vote but in general movies are getting worse?! Or people seem to like movies less...

# Lets turn to genres, reminder of what the split looked like
md_split_genres.head()

# How many different genres do we have?
md_split_genres['genres'].unique()

len(md_split_genres['genres'].unique())

Overall, we have movies from 20 unique genres.

### Research Questions

<a id='q1'></a>
#### Q1. Which genres are the most common (number of movies made)?

# Group movies by genre using title as unique identifier and display all genres.
md_genre = (pd.DataFrame(md_split_genres.groupby('genres').original_title.nunique())).sort_values('original_title', ascending=True)
md_genre.head(20)

md_genre['original_title'].plot.pie(title= 'Movies per Genre in %', figsize=(10,10), autopct='%1.1f%%',fontsize=15);

# Display in bar chart
md_genre['original_title'].plot.barh(title = 'Movies per Genre',color='DarkBlue', figsize=(10, 9));


The most common genres are Drama (4672 movies, 17.6%) , Comedy (3750 movies, 14.2%) and Thriller (2841 movies, 10.7%).

<a id='q2'></a>
#### Q2. Which genres have high avg. budget and revenue?

# Check results
md_genre_mean.head()

# Sort data in acending order 
md_genre_mean.sort_values('budget_million', ascending=True, inplace = True )

# Create bar chart with revenue and budget
md_genre_mean[['revenue_million', 'budget_million']].plot.barh(stacked=False, title = 'Budget and Revenue by Genre (US$ million)',color=('DarkBlue','c'), figsize=(15, 10));

In the graph above we clearly see that the genre Adventure has both the highest avg. budget and revenue. Fantasy comes second in budget and revenue. Interestingly, Animation has the third highest revenue but only the sixth highest budget. Meaning Animation movies are on avg. more profitable. Lets look at profitability of the genres.

<a id='q3'></a>
#### Q3. Which genres have high avg. profit?

md_genre_mean.sort_values('profit_million', ascending=True, inplace = True )
md_genre_mean['profit_million'].plot.barh(stacked=False, title = 'Profit by Genre (US$ million)',color='DarkBlue', figsize=(10, 9));

The top 5 genres in terms of avg. profit are Adventure, Fantasy, Animation, Family and Science Fiction.

<a id='q4'></a>
#### Q4. Which genres have high vote avg.?

md_genre_mean.sort_values('vote_average', ascending=True, inplace = True)
md_genre_mean[['vote_average']].plot.barh(stacked=True, title = 'Voting Avg by Genre',color='DarkBlue', figsize=(10, 9));

Documentaries, Music and History have the hightest voting avg. Then comes Animation.

<a id='q5'></a>
#### Q5. Which genres have high avg. popularity?

md_genre_mean.sort_values('popularity', ascending=True, inplace = True)
md_genre_mean[['popularity']].plot.barh(stacked=True, title = 'Genres by Avg Popularity',color='DarkBlue', figsize=(10, 9));


The most popular genres are Adventure, Science Fiction, Fantasy, Action and again Animation.

<aid='q6'></a>
#### Q6. Which genres have high avg. vote count?

md_genre_mean.sort_values('vote_count', ascending=True, inplace = True)
md_genre_mean[['vote_count']].plot.barh(stacked=True, title = 'Genres by Avg Vote Count',color='DarkBlue',figsize=(10, 9));

However, Documentary, Music and History have a relatively low number of votes. Compared to Adventure, Science Fiction and Fantasy. Then comes Action and again Animation.

<a id='q7'></a>
#### Q7. Which genres have high number of movies with an voting avg. >=8?

md_8 = md_split_genres[md_split_genres['vote_average']>=8]
md_8 = (pd.DataFrame(md_split_genres.groupby('genres').original_title.nunique())).sort_values('original_title', ascending=True )
md_8[['original_title']].plot.barh(stacked=True, title = 'Genres with >= 8 ratings', figsize=(10, 9),color='DarkBlue');


The genre drama has the most movies with a rating of at least 8.

<a id='analysis'></a>
#### Analysis of development of means of variables per genre over the years

# Reminder of how the data frame looked like, when we splitted for genres
md_split_genres.head()

# Create data frame grouped by genres AND release year, get means of variables of interest
md_year_genre_mean = pd.DataFrame(md_split_genres.groupby(['release_year','genres'])['revenue', 'budget','profit','vote_average','vote_count','popularity'].mean())
md_year_genre_mean.head()

#### Profit per genre per year

# Create data frame for average profit per genre per year
md_year_genre_profit = pd.DataFrame(md_split_genres.groupby(['release_year','genres'])['profit'].mean())
md_year_genre_profit.head()

# pivot data to get the shape that is necessary for a heatmap that displays genres, years and avg. profit per genre per year
md_heat_profit_pivot = pd.pivot_table(md_year_genre_profit, values='profit', index=['genres'], columns=['release_year'])
md_heat_profit_pivot.head()

# display heatmap
sns.set(rc={'figure.figsize':(15,10)})
sns.heatmap(md_heat_profit_pivot, linewidths=.5, cmap='YlGnBu');

This heatmap displays the average profit per genre per year from 1960 to 2015. The darker blue fields show higher profit, the brighter green into yellow fields show lower profit. In general, profits are increasing over time for especially for the genres Action, Adventure Animation, Family, Fantasy and Science Fiction.
Animation movies had a very profitable year in 1961. History in 1991 and Western in 1998. Adventure in 2012.

#### Revenue per genre per year

md_year_genre_revenue = pd.DataFrame(md_split_genres.groupby(['release_year','genres'])['revenue'].mean())
md_heat_revenue_pivot = pd.pivot_table(md_year_genre_revenue, values='revenue', index=['genres'], columns=['release_year'])
sns.set(rc={'figure.figsize':(15,10)})
sns.heatmap(md_heat_revenue_pivot, linewidths=.5, cmap='YlGnBu');

In terms of revenue the heatmap is of course closely related to the heatmap of profit showing a strong increase for Action, Adventure, Animation, Family, Fantasy and Science Fiction over the years. Nevertheless, the increases of revenue are more visible in the heatmap since revenues increased more sharply over the years than profit. The outliers for Animation movies in 1961 and History in 1991, Western in 1998 and Adventure in 2012 are also visible in the revenue heatmap. Outliers could be due to a view outperformers and very successful movies.

#### Budget per genre per year

md_year_genre_budget = pd.DataFrame(md_split_genres.groupby(['release_year','genres'])['budget'].mean())
md_heat_budget_pivot = pd.pivot_table(md_year_genre_budget, values='budget', index=['genres'], columns=['release_year'])
sns.set(rc={'figure.figsize':(15,10)})
sns.heatmap(md_heat_budget_pivot, linewidths=.5, cmap='YlGnBu');

The heatmap shows that in particular the movies of the genres Action, Adventure, Family, Fantasy and Science Fiction had an increasing budget over the years. The heatmap also shows that Western movies had an extremely high budget in 1998 and 2011. This could mean that a costly movie is produced in 1998 (maybe even the successful one) and 2011 which has great influence on the average. This outlier could be removed for a later analysis to get a better overview of the distribution of the rest of the movies.

#### Vote Average per genre per year

md_year_genre_vote_avg = pd.DataFrame(md_split_genres.groupby(['release_year','genres'])['vote_average'].mean())
md_heat_vote_avg_pivot = pd.pivot_table(md_year_genre_vote_avg, values='vote_average', index=['genres'], columns=['release_year'])
sns.set(rc={'figure.figsize':(15,10)})
sns.heatmap(md_heat_vote_avg_pivot, linewidths=.5, cmap='YlGnBu');

This heatmap is way more blue than the previous ones. It seems that movies across genres got a better rating from ~1975 to 1985. Most of the genres seem to be getting somewhere around a 6 to 6.4 out of 10 score, though. Especially notable is the fact that there are very few green or yellow colored cells, which could mean that most movies are on average just a not so bad.

#### Vote Count per genre per year

md_year_genre_vote_count = pd.DataFrame(md_split_genres.groupby(['release_year','genres'])['vote_count'].mean())
md_heat_vote_count_pivot = pd.pivot_table(md_year_genre_vote_count, values='vote_count', index=['genres'], columns=['release_year'])
sns.set(rc={'figure.figsize':(15,10)})
sns.heatmap(md_heat_vote_count_pivot, linewidths=.5, cmap='YlGnBu');

The heatmap shows that in particular the movies of the genres Action, Adventure, Fantasy and Science Fiction as well as Western had an increasing vote count over the years. Especially, Western movies had a extremely high avg. vote count in 2012.

#### Popularity per genre per year

md_year_genre_pop = pd.DataFrame(md_split_genres.groupby(['release_year','genres'])['popularity'].mean())
md_heat_pop_pivot = pd.pivot_table(md_year_genre_pop, values='popularity', index=['genres'], columns=['release_year'])
sns.set(rc={'figure.figsize':(15,10)})
sns.heatmap(md_heat_pop_pivot, linewidths=.5, cmap='YlGnBu');

The heatmap shows that in particular the movies of the genres Action, Adventure, Fantasy and Science Fiction as well as Western had an increasing popularity over the years. Especially, Western movies had a extremely high avg. populartiy in 2012 (same as vote count). Moreover, Animation had a very high popularity in 1961 (maybe the high revenue/ profit movie). 

### Research Hypotheses

<a id='h1'></a>
#### H1. The best movies according to vote avg. return high profit and revenue.

md.corr(method='pearson')

To see if there is a linear relationship b/w profit (revenue) and vote avg. I used the correlation coefficient of pearson and displayed the results in a table. With a coefficient of ~0.184 there is no evidence of a strong postive linear relationship b/w profit and vote avg. The same holds true for revenue with a coefficient of ~0.173. So movies with a higher avg. voting do not necessarily bring in high profits and revenues. There is no strong evidence in the data for hypothesis 1.

I displayed the correlation in a scatterplot for visualization.

md.plot.scatter(x='vote_average', y='profit',title='Profit vs Vote Avg',color='DarkBlue',figsize=(6,5));

md.plot.scatter(x='vote_average', y='revenue',title='Revenue vs Vote Avg',color='DarkBlue',figsize=(6,5));

Here, we see that there is no clear positve linear relationship since a lot of movies have a high voting avg. but only moderatly profit and revenue. Both scatterplots are similar since profit is derived from revenue. 

#### Additonal FInding
However, the strongest linear relationship is evident b/w profit (revenue) and vote count ~0.756 and ~0.791, respectievly. It turns out that there is a strong linear relationship b/w proft (revenue) and the number of votes. Movies with a high number of votes seem to return high profit and revenue.


md.plot.scatter(x='vote_count', y='profit',title='Profit vs Vote Count', color='DarkBlue', figsize=(6,5));

md.plot.scatter(x='vote_count', y='revenue',title='Revenue vs Vote Count', color='DarkBlue', figsize=(6,5));

<a id='h2'></a>
#### H2. The best movies according to popularity return high profit and revenue.

md.plot.scatter(x='popularity', y='profit',title='Profit vs Popularity', color='DarkBlue', figsize=(6,5));

md.plot.scatter(x='popularity', y='revenue',title='Revenue vs Popularity', color='DarkBlue', figsize=(6,5));

If we look at the relationship of avg. profit (revenue) with popularity we find that the correlation is more evident in the data. We get a correlation coefficient of ~0.629 for profit and popularity which demonstrates a moderate linear postive relationship. For revenue (which is closely related to profit since profit is calculated based on revenue) we get an even stronger linear relationship with a coefficient of ~0.663. This means that movies with a high avg. popularity rating did bring in on avg. more profit and revenue. There is moderate evidence in the data for hypothesis 2. OUTLIERS???

<a id='h3'></a>
#### H3. Highly budgeted movies return high revenue and profit.

md.plot.scatter(x='revenue', y='budget',title='Budget vs Revenue', color='DarkBlue', figsize=(6,5));

md.plot.scatter(x='profit', y='budget',title='Budget vs Profit', color='DarkBlue', figsize=(6,5));

The correlation coefficient b/w budget and revenue is ~0.735. Here we have a strong linear relationship. We find strong evidence in the data that support hypothesis 3: Higly budgeted movies return in general higher revenue.

For budget and profit we find evidence for a moderate linear relationship with a coefficient of ~0.570.

<a id='h4'></a>
#### H4. Highly budgeted movies have a high vote avg.

md.plot.scatter(x='vote_average', y='budget',title='Budget vs Vote Avg', color='DarkBlue', figsize=(6,5));

There is no linear relationship b/w budget and vote avg (coefficient of ~0.082). We can reject hypothesis 4. Only because a movie has a high budget does not mean that it will receive a high voting avg.

<a id='h5'></a>
#### H5. Highly budgeted movies have a high popularity.

md.plot.scatter(x='popularity', y='budget',title='Budget vs Popularity', color='DarkBlue', figsize=(6,5));

We find a moderate linear relationship b/w budget and popularity with a correlation coefficient of ~0.545 and with that moderate evidence for hypothesis 5: Movies with a high budget seem to have moderately higher popularity.

<a id='conclusions'></a>
## Conclusions

So which genre should you pick if you want to produce a movie?

- If you want profit you should go for Adventure, Fantasy or Animation (Top 3 in terms of profit).
- If you want high rating go for Documentary, Music or History. (Taking into account that you will not have very much viewers and therefore revenue)
- If you want high popularity go for Adventure, Science Fiction or Fantasy.
- In general, profits (revenues) are increasing over time especially for the genres Action, Adventure, Animation, Family, Fantasy and Science Fiction. Animation movies had a very profitable year in 1961. History in 1991 and Western in 1998. Adventure in 2012.
- Also, movies of the genres Action, Adventure, Family, Fantasy and Science Fiction had an increasing budget over the years. The heatmap also shows that Western movies had an extremely high budget in 1998 and 2011.

Let's again look at the research hypotheses:

- Movies with a high avg. voting do not necessarily bring in high profits and revenues.
- However, movies with a high avg. popularity rating seem to bring in on avg. more profit and revenue.
- Higly budgeted movies return in general higher revenue, but not necessarily high profit (moderate linear relationship)
- Only because a movie has a high budget, does not mean that it becomes a great movie with a very high avg. rating.

However, these relations are merely correlations and do not imply causation.

### Limitations

The hypothesis questions were analyzed using the correlation coefficient. They all assume values in the range from −1 to +1, where +1 indicates the strongest possible agreement and −1 the strongest possible disagreement, in terms of linear relationship. As tools of analysis, correlation coefficients present certain problems, including the propensity of some types to be distorted by outliers and the possibility of incorrectly being used to infer a causal relationship between the variables.
Therefore, these relations are merely correlations and do not imply causation. No statistical tests have been made to determine the robustness of relationships.

The hypotheses should be investigated further. 

### Resources
https://seaborn.pydata.org/generated/seaborn.heatmap.html
https://stackoverflow.com/questions/37790429/seaborn-heatmap-using-pandas-dataframe
https://stackoverflow.com/questions/31594549/how-do-i-change-the-figure-size-for-a-seaborn-plot
https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.pivot.html
https://pandas.pydata.org/pandas-docs/stable/reshaping.html
https://github.com/pandas-dev/pandas/issues/11076
https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html
https://pandas.pydata.org/pandas-docs/stable/visualization.html
https://stackoverflow.com/questions/38337918/plot-pie-chart-and-table-of-pandas-dataframe
https://www.kaggle.com/rdrubbel/tmdb-analysis
https://github.com/AjaSharma93/TMDB-Data-Analysis/blob/master/TMDB_Report.ipynb
https://github.com/nirupamaprv/Investigate_Dataset/blob/master/Investigate_a_Dataset_TMDb.ipynb
https://github.com/abhishekchhibber/IMDB_Dataset_Analysis/blob/master/imdb_db_analysis_abhishek_chhibber.ipynb


