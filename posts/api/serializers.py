from rest_framework.serializers import (
	ModelSerializer, 
	HyperlinkedIdentityField, 
	SerializerMethodField
	)

from comments.api.serializers import CommentSerializer
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer
from posts.models import Post
from django.contrib.auth import get_user_model


User = get_user_model()
class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			# 'id',
			'title', 
			# 'slug', 
			'content', 
			'publish',
		]

post_detail_url = HyperlinkedIdentityField(
		view_name='posts-api:detail',
		lookup_field='slug'
		)


class PostDetailSerializer(ModelSerializer):
	url = post_detail_url
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()

	class Meta:
		model = Post
		fields = [
			'url', 
			'id', 
			'user', 
			'title', 
			'slug', 
			'content', 
			'html', 
			'publish', 
			'image',
			'comments' 
		]

	def get_html(self, obj):
		return obj.get_markdown()

	# def get_user(self, obj): # Define UserDetailSerializer(read_only=True)
	# 	return str(obj.user.username)

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image

	def get_comments(self, obj):
		# content_type = obj.get_content_type
		# object_id =obj.id
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentSerializer(c_qs, many=True).data
		return comments 


class PostListSerializer(ModelSerializer):
	url = post_detail_url
	user = UserDetailSerializer(read_only=True)

	class Meta:
		model = Post
		fields = [
			'url', 'user', 'title', 'content', 'publish',
		]

	# def get_user(self, obj):  # Define UserDetailSerializer(read_only=True)
	# 	return str(obj.user.username)
