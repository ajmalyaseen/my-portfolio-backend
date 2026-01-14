from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from .models import (
    Blogmodel, CommentTable, LikeTableBlog, 
    LikeTableProjects, Projectmodel, Gallerymodel, ContactForm
)
from .serializer import (
    BlogListSerializer, BlogDetailSerializer, CommentsSerilizer, 
    ProjectSerializer, GallerySerializer, ContactSerializer
)
from .utils import BlogUtils
from .mixins import BaseLikeToggleView
from .task import send_mail_users

# --- BLOG SECTION ---

# Returns a list of all blog posts, sorted by newest first.
class BlogListView(generics.ListAPIView):
    queryset = Blogmodel.objects.all().order_by('-created_at')
    serializer_class = BlogListSerializer
    permission_classes = [permissions.AllowAny]

# Returns detailed information for a single blog post (content, comments, likes).
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blogmodel.objects.all()
    serializer_class = BlogDetailSerializer
    permission_classes = [permissions.AllowAny]

# Allows users to post a comment on a specific blog post.
class CommentCreateView(generics.CreateAPIView):
    queryset = CommentTable.objects.all()
    serializer_class = CommentsSerilizer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Automatically attach the comment to the blog post identified by the ID in the URL.
        blog_id = self.kwargs.get('pk')
        try:
            serializer.save(blog_id=blog_id)
        except IntegrityError:
            # If the blog ID doesn't exist in the database, return a clear error.
            raise ValidationError("Invalid blog ID. The blog post does not exist.")

# Toggles 'like' status for a blog post based on current user's ID/IP.
class Likeblog(BaseLikeToggleView):
    model_class = LikeTableBlog
    foreign_key_field = 'liked_blog_id'


# --- PROJECTS SECTION ---

# Returns a list of all portfolio projects.
class ProjectListView(generics.ListAPIView):
    queryset = Projectmodel.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

# Toggles 'like' status for a project.
class ProjectLike(BaseLikeToggleView):
    model_class = LikeTableProjects
    foreign_key_field = 'liked_project_id'


# --- GALLERY SECTION ---

# Handles displaying gallery images with manual pagination (12 items per page).
class GalleryListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Determine the current page; default is 1.
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1

        items_per_page = 12
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        # Fetch enough data to check if there is a next page.
        data = Gallerymodel.objects.all()[start_index : end_index + 1]
        
        # If we got 13 items, it means a next page exists.
        if len(data) > items_per_page:
            has_next_page = True
            response_data = data[:items_per_page]
        else:
            has_next_page = False
            response_data = data

        serializer = GallerySerializer(response_data, many=True)

        return Response({
            'data': serializer.data,
            'has_next_page': has_next_page
        }, status=status.HTTP_200_OK)


# --- CONTACT SECTION ---

# Handles contact form submissions and triggers an asynchronous email via Celery.
class ContactFormView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Save the contact message to the database.
            serializer.save()
            
            # Send an email notification in the background using Celery.
            usermail = serializer.validated_data.get('usermail')
            username = serializer.validated_data.get('username')
            send_mail_users.delay(usermail, username)
            
            return Response({
                "message": "Message sent successfully! We will contact you soon."
            }, status=status.HTTP_201_CREATED)

        # If data is invalid (e.g., bad email format), return the errors.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)