from rest_framework import serializers

from .models import Category, Product, Comment, Pictures, Reply, Variation
from users.serializer import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = ["comment", "author", "content", "rate", "creation_date"]

    def create(self, validate_data):
        author = validate_data.pop("author")
        reply = Reply.objects.create(author=author, **validate_data)
        return reply

    def update(self, instance, validated_data):

        instance.rate = validated_data.get("rate", instance.rate)
        instance.content = validated_data.get("content", instance.content)
        instance.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, source="reply_set", read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "product",
            "author",
            "rate",
            "content",
            "creation_date",
            "replies",
        ]

    def create(self, validated_data):

        author = validated_data.pop("author")
        comment = Comment.objects.create(author=author, **validated_data)
        return comment

    def update(self, instance, validated_data):

        instance.rate = validated_data.get("rate", instance.rate)
        instance.content = validated_data.get("content", instance.content)
        instance.save()

        return instance


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = ["image_url"]


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ["id", "title", "price", "discount", "creation_date"]


class ProductSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, source="pictures_set")
    comments = CommentSerializer(many=True, source="comment_set", read_only=True)
    supplier = UserSerializer(read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "creation_date",
            "pictures",
            "price",
            "discount",
            "supplier",
            "category",
            "comments",
        ]

    def create(self, validated_data):
        user = validated_data.pop("user")
        images_data = validated_data.pop("pictures_set")
        category = validated_data.pop("category")
        category = Category.objects.get(name=category["name"])
        product = Product.objects.create(
            supplier=user, category=category, **validated_data
        )

        for image in images_data:
            Pictures.objects.create(product=product, **image)

        Variation.objects.create(
            product=product,
            title=product.title,
            price=product.price,
            discount=product.discount,
        )
        return product

    def update(self, instance, validated_data):

        pictures_data = validated_data.pop("pictures_set")
        pictures = (instance.pictures_set).all()
        pictures = list(pictures)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.discount = validated_data.get("discount", instance.discount)
        instance.supplier = validated_data.get("supplier", instance.supplier)
        instance.category = validated_data.get("category", instance.category)
        instance.save()

        Variation.objects.create(
            product=instance,
            title=instance.title,
            price=instance.price,
            discount=instance.discount,
        )

        for picture_data in pictures_data:
            picture = pictures.pop(0)
            picture.image_url = picture_data.get("image_url", picture.image_url)
            picture.save()

        return instance
