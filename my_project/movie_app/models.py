from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


STATUS_CHOICES = (
    ('simple', 'simple'),
    ('pro', 'pro'),
)
class UserProfile(AbstractUser):
    phone_number = PhoneNumberField()
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(15), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    avatar = models.ImageField(
        upload_to='profile_image',
        null=True,
        blank=True
    )
    user_status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default='simple'
    )
    data_register = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}- {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=45)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    director_image = models.ImageField( upload_to='photo_director', null=True, blank=True)

    def __str__(self):
        return self.director_name

class Actor(models.Model):
    actor_name = models.CharField(max_length=45)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)],
                                         null=True, blank=True)
    actor_image = models.ImageField(upload_to='photo_actor', null=True, blank=True)

    def __str__(self):
        return self.actor_name

class Genre(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_genre')
    genre_name = models.CharField(max_length=32)

    def __str__(self):
        return self.genre_name

class Movie(models.Model):
    TYPES_CHOICES = (
        ('144p', '144p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    )
    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    slogan = models.CharField(max_length=100)
    country = models.ManyToManyField(Country, related_name='country_movie')
    director = models.ManyToManyField(Director, related_name='director_movie')
    actor = models.ManyToManyField(Actor, related_name='actor_movie')
    genre = models.ManyToManyField(Genre, related_name='genre_movie')
    types = models.CharField(choices=TYPES_CHOICES, default='720p')
    movie_time = models.PositiveSmallIntegerField()
    movie_trailer = models.URLField()
    descriptions = models.TextField()
    movie_image = models.ImageField(upload_to='movie_photo')
    status_movie = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return self.movie_name

    def get_average_rating(self):
        ratings = self.movie_rating.all()
        if ratings.exists():
            return round(sum(i.star for i in ratings) / ratings.count(), 2)
        return 0


class MovieLanguage(models.Model):
    language = models.CharField(max_length=64)
    video = models.FileField(upload_to='movie_language')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name = 'movie_language')

    def __str__(self):
        return self.language

class Moment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name = 'movie_moment')
    movie_moment = models.ImageField(upload_to='movie_moment', null=True, blank=True)

    def __str__(self):
        return f'{self.movie.movie_name}'

class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name = 'movie_rating')
    star = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)],
                                           null=True, blank=True)

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class History(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)