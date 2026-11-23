from django.contrib import admin
from .models import (UserProfile, Category, Country, Director,Actor,
                     Genre, Movie, MovieLanguage, Moment, Rating, Review,
                     ReviewLike,Favorite, FavoriteItem, History)
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin

class GenreInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Genre
    extra = 1

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    inlines = [GenreInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class MovieLanguageInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = MovieLanguage
    extra = 1

class MomentInline(admin.TabularInline ):
    model = Moment
    extra = 1

@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    inlines = [MovieLanguageInline, MomentInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Country, Director, Actor)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(UserProfile)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(ReviewLike)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
admin.site.register(History)


