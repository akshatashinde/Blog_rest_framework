from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)

from comments.api.serializers import CommentSerializer
from comments.models import Comment
from posts.models import Post

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
		view_name = 'posts-api:detail',
		lookup_field='slug'
		)


class PostDetailSerializer(ModelSerializer):
	url = post_detail_url
	user = SerializerMethodField()
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
			'publish',
			'image',
			'html',
			'comments',
		]	

	def get_html(self,obj):
		return obj.get_markdown()

	def get_user(self, obj):
		return str(obj.user.username)

	def get_image(self, obj):
		try:
			image = obj.image.path
		except:
			image = None
		return image 	

	def get_comments(self, obj):
		content_type = obj.get_content_type
		object_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj)				
		comments = CommentSerializer(c_qs, many=True).data
		return comments


class PostListSerializer(ModelSerializer):
	url = post_detail_url
	user = SerializerMethodField()
	# delete_url = HyperlinkedIdentityField(
	# 	view_name = 'posts-api:delete',
	# 	lookup_field='slug'
	# 	)
	class Meta:
		model = Post
		fields = [
			'url',
			'user',
			'title',
			'slug',
			'content',
			'publish',
			# 'delete_url',
		]

	def get_user(self, obj):
		return str(obj.user.username )	


""""

data = {
		"id": 3,
        "title": "Ak",
        "slug": "ak",
        "content": "hello..",
        "publish": "2016-07-22"

}

new_item = PostSerializer(data=data)
if new_item.is_valid():
	new_item.save()


	print(new_item.errors)


"""
