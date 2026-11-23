from modeltranslation.translator import TranslationOptions,register
from .models import Category, Genre, Country, Director, Actor, Movie, MovieLanguage

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('genre_name',)

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)

@register(Director)
class DirectorTranslationOptions(TranslationOptions):
    fields = ('director_name','bio')

@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('actor_name','bio')

@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('movie_name','slogan','status_movie')

@register(MovieLanguage)
class MovieLanguageTranslationOptions(TranslationOptions):
    fields = ('language',)