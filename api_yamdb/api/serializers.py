from rest_framework import serializers
from reviews.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'review', 'created')
        read_only_fields = ('author', 'review')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        read_only_fields = ('author', 'title')
