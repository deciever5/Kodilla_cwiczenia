import datetime
from random import randint


class Movie:
    def __init__(self, title, year, genre):
        self.title = title
        self.year = year
        self.genre = genre
        # variables
        self.played = 0

    def __str__(self):
        return f'{self.title} {self.year} '

    def play(self):
        self.played += 1


class Series(Movie):
    def __init__(self, title, year, genre, episode, season):
        super().__init__(title, year, genre)
        self.episode = episode
        self.season = season

    def __str__(self):
        return f'{self.title} S{self.episode:0=2d}E{self.season:0=2d}'

    def number_of_episodes(self):
        return sum(p.title == self.title for p in movie_list)


def get_movies():
    only_movies_list = [movie for movie in movie_list if not isinstance(movie, Series)]
    print(only_movies_list)


def get_series():
    only_series_list = [movie for movie in movie_list if isinstance(movie, Series)]
    print(only_series_list)


def search(title):
    for movie in movie_list:
        if movie.title == title:
            print(f'Znaleziono film {str(movie)}')
            return None
    print(f"Nie znaleziono filmu {title}")


def generate_views(num):
    for m in range(num):
        movie_list[randint(0, len(movie_list) - 1)].played += randint(1, 100)


def add_series(title, year, genre, season, nr_of_episodes):
    movie_list.append(Series(title, year, genre, season, nr_of_episodes))


def print_movies(list_of_movies):
    for x in range(len(list_of_movies)):
        print(f'Tytuł: {list_of_movies[x]} Liczba odtworzeń: {list_of_movies[x].played}')


def top_titles(nr_of_tops=5, movie_or_series=None):
    print(f"Najpopularniejsze filmy i seriale dnia {datetime.datetime.today():%d.%m.%y}")
    top_titles_sorted = [movie for movie in sorted(movie_list, key=lambda x: x.played, reverse=True)]
    if movie_or_series == Series:
        top_series = [movie for movie in top_titles_sorted if isinstance(movie, Series)][:nr_of_tops:]
        print_movies(top_series)
    elif movie_or_series == Movie:
        top_movies = [movie for movie in top_titles_sorted if not isinstance(movie, Series)][:nr_of_tops:]
        print_movies(top_movies)
    else:
        print_movies(top_titles_sorted[:nr_of_tops:])


# Test functions
print("Biblioteka filmów")

movie_list = [Movie("Pulp Fiction", 1994, "Drama"), Movie("Matrix", 1997, "Action"),
              Series("Frasier", 1992, "Commedy", 1, 1), Series("Friends", 1993, "Commedy", 1, 1),
              Movie("Top gun", 1996, "Action"), Movie("Das Boot", 1985, "Action")]

for i in range(1, 11):
    add_series("Dr House", 2001, "Drama", i, i * 2)

generate_views(100)

top_titles(3)
