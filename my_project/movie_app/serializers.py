from rest_framework import serializers
from .models import (UserProfile, Category, Country, Director,Actor, Genre,
                     Movie, MovieLanguage, Moment, Rating, Review, ReviewLike,
                     Favorite, FavoriteItem, History)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','first_name','avatar']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','first_name','last_name','avatar']


class CountryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre_name']


class MovieDetailSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format='%d-%m-%Y')
    country = CountryNameSerializer(many=True)
    genre = GenreListSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['movie_name','year','slogan','country','director','actor',
                  'genre','types','movie_time','average_rating',
                  'movie_trailer','descriptions','movie_image','status_movie']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    category_genre = GenreListSerializer(many=True)
    class Meta:
        model = Category
        fields = ['category_name', 'category_genre']


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id','director_name','director_image']


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id','actor_name','actor_image']


class MovieLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguage
        fields = ['id','language','video']


class MomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moment
        fields = ['id','movie_moment']


class MovieListSerializer(serializers.ModelSerializer):
    country = CountryNameSerializer(many=True)
    genre = GenreListSerializer(many=True)
    director = DirectorListSerializer(many=True)
    actor = ActorListSerializer(many=True)
    movie_language = MovieLanguageSerializer(many=True, read_only=True)
    movie_moment = MomentSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id','movie_name','year','genre','director',
                  'actor','movie_image','status_movie','country', 'movie_language','movie_moment']


class MovieNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id','movie_name']




class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']

class CountryDetailSerializer(serializers.ModelSerializer):
    country_movie = MovieListSerializer(read_only=True, many=True)
    class Meta:
        model = Country
        fields = ['country_name', 'country_movie']


class DirectorDetailSerializer(serializers.ModelSerializer):
    director_movie = MovieListSerializer(many=True, read_only=True)
    class Meta:
        model = Director
        fields = ['director_name','bio','age','director_image','director_movie']


class ActorDetailSerializer(serializers.ModelSerializer):
    actor_movie = MovieListSerializer(many=True, read_only=True)
    class Meta:
        model = Actor
        fields = ['actor_name','bio','age','actor_image', 'actor_movie']


class GenreDetailSerializer(serializers.ModelSerializer):
    genre_movie = MovieListSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ['genre_name','genre_movie']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user  = UserProfileNameSerializer()
    created_date = serializers.DateField(format='%d-%m-%Y')
    total_like = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['id','user','created_date', 'comment','parent', 'total_like']

    def get_total_like(self, obj):
        return obj.get_total_like()


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
       model = Review
       fields = '__all__'


class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    viewed_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    movie = MovieNameSerializer()
    class Meta:
        model = History
        fields = ['id','movie','viewed_at']