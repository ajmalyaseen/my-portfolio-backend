from rest_framework import serializers
from .models import Blogmodel,Projectmodel,Gallerymodel,ContactForm,LikeTableBlog,LikeTableProjects,CommentTable

# Serializer for listing blog posts with basic info (id, title, image, date).
class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogmodel
        fields = ['id','title','image','created_at']
        read_only_fields=['created_at']

# Serializer for individual blog comments.
class CommentsSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CommentTable
        fields = '__all__'
        read_only_fields = ['posted_at', 'blog']


# Serializer for retrieving full blog details, including comments and total likes.
class BlogDetailSerializer(serializers.ModelSerializer):
    comments=CommentsSerilizer(many=True, read_only=True)
    total_like=serializers.SerializerMethodField()
    class Meta:
        model = Blogmodel
        fields = ['id','title','image','content','created_at','comments','total_like']
        read_only_fields=['created_at','total_like']
    def get_total_like(self,obj):
        total_like=LikeTableBlog.objects.filter(liked_blog=obj).count()
        return total_like
    

# Serializer for projects, including the total number of likes.
class ProjectSerializer(serializers.ModelSerializer):
    total_like=serializers.SerializerMethodField()
    class Meta:
        model = Projectmodel
        fields = '__all__'
    def get_total_like(self,obj):
        total_like=LikeTableProjects.objects.filter(liked_project_id=obj.id)
        return total_like

# Serializer for gallery items.
class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallerymodel
        fields = '__all__'
        read_only_fields=['posted_at']

# Serializer for contact form data.
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'
        read_only_fields=['send_at']

# Serializers to handle like data for blogs and projects.
class LikeTableBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeTableBlog
        fields = '__all__'
        read_only_fields=['liked_at']

class LikeTableProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeTableProjects
        fields = '__all__'