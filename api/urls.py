from django.urls import path
from .views import (
    BlogListView, 
    BlogDetailView, 
    CommentCreateView,
    Likeblog,
    ProjectListView,
    ProjectLike,
    GalleryListView,
    ContactFormView
)

urlpatterns = [
    # Endpoint to retrieve a list of all blog posts.
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    
    # Endpoint to retrieve details of a specific blog post by ID.
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    # Endpoint for submitting a comment on a blog post.
    path('comment/create/',CommentCreateView.as_view(),name='comment-create'),
    # Endpoint to like or unlike a blog post.
    path('blog/<int:pk>/like/',Likeblog.as_view(),name='like-blog'),
    # Endpoint to retrieve a list of all portfolio projects.
    path('project/',ProjectListView.as_view(),name='project-view'),
    # Endpoint to like or unlike a project.
    path('project/<int:pk>/like/',ProjectLike.as_view(),name='like-project'),
    # Endpoint for the paginated gallery view.
    path('gallery/',GalleryListView.as_view(),name='gallery-view'),
    # Endpoint for contact form submissions.
    path('contact/',ContactFormView.as_view(),name='contact-form')
]