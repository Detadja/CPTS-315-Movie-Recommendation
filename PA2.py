import pandas as pd

# Read files into variables
movies = pd.read_csv('C:\\Users\\denis\\Desktop\\PA2\\Data\\movies.csv')
ratings = pd.read_csv('C:\\Users\\denis\\Desktop\\PA2\\Data\\ratings.csv')
# tags = pd.read_csv('C:\\Users\\denis\\Desktop\\PA2\\Data\\tags.csv')
# links = pd.read_csv('C:\\Users\\denis\\Desktop\\PA2\\Data\\links.csv')
# print(movies)
# print(ratings)

# Merge ratings and movies dataframes into one profile dataframe, and sorts it to prioritize userId and the ratings for each movie.
profile = pd.merge(ratings, movies, on = 'movieId')
# print(profile.head())
movie_profile = profile.pivot_table(index = 'userId', columns = 'title', values = 'rating')
# print(movie_profile.iloc[0])
movie_corr = movie_profile.corr(method = 'pearson', min_periods = 40) # Finds the movie-movie correlation matrix
# print(movie_corr)
# print(movie_corr.iloc[1].dropna())

# Determines the neighbourhood set N for each movie with the highest similarity score.
recommend = []
for i in range(len(movie_profile)):
    ratings = movie_profile.iloc[i].dropna() # Gets the ratings for user i, ignoring empty ratings
    recc = pd.Series()
    for j in range(len(ratings)):
        similar = movie_corr[ratings.index[j]].dropna() # Gets the line in the correlation matrix corresponding to the movie user i rated (movie j)
        similar = similar.map(lambda x: x * ratings[j]) # Multiplies the correlation matrix values by user i's rating for movie j.
        recc = recc.append(similar)
    # print(recc)

    dict_recc = recc.to_dict() # Turns the values from series to a dictionary
    sorted_dict = dict(sorted(dict_recc.items(), key = lambda item: item[1], reverse = True)) # Sorts the dictionary
    recommend.append(sorted_dict) # Appends the dictionary to a list
# print(recommend)

# Outputs the results into output.txt
with open("C:\\Users\\denis\\Desktop\\PA2\\output.txt", "w") as ofile:
    index = 1
    for i in recommend:
        count = 0
        ofile.write(str(index) + ' ')
        for key in i:
            if count == 5:
                break
            ofile.write(str(movies.loc[movies['title'] == key, 'movieId'].iloc[0]) + ' ')
            count += 1
        ofile.write('\n')
        index += 1
