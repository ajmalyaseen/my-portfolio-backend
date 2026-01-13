from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Blogmodel,CommentTable,LikeTableBlog,LikeTableProjects,Projectmodel,Gallerymodel,ContactForm
from .serializer import BlogListSerializer,BlogDetailSerializer,CommentsSerilizer,ProjectSerializer,GallerySerializer,ContactSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import BlogUtils
from .mixins import BaseLikeToggleView
from .task import send_mail_users
from rest_framework import status

# View to list all blog posts, ordered by the most recent first.
class BlogListView(generics.ListAPIView):
    queryset=Blogmodel.objects.all().order_by('-created_at')
    serializer_class=BlogListSerializer
    permission_classes=[permissions.AllowAny]

# View to retrieve details of a single blog post, including its comments.
class BlogDetailView(generics.RetrieveAPIView):
    queryset=Blogmodel.objects.all()
    serializer_class=BlogDetailSerializer
    permission_classes=[permissions.AllowAny]


# Section for creating new comments on blogs.
class CommentCreateView(generics.CreateAPIView):
    queryset=CommentTable.objects.all()
    serializer_class=CommentsSerilizer
    permission_classes=[permissions.AllowAny]

# Endpoint for liking/unliking a blog post.
class Likeblog(BaseLikeToggleView):
    model_class=LikeTableBlog
    foreign_key_field = 'liked_blog_id'



# View to list all projects in the portfolio.
class ProjectListView(generics.ListAPIView):
    queryset=Projectmodel.objects.all()
    serializer_class=ProjectSerializer

# Endpoint for liking/unliking a project.
class ProjectLike(BaseLikeToggleView):
    model_class=LikeTableProjects
    foreign_key_field = 'liked_project_id'

# View for the gallery with simple pagination (12 items per page).
class GalleryListView(APIView):
    def get(self,request):
        page = request.GET.get('page', 1)
        start_index=(page-1)*12
        end_index=start_index+12
        data=Gallerymodel.objects.all()[start_index:end_index+1]
        if len(data)>12:
            has_next_page=True
            response_data=data[:12]
        else:
            has_next_page=False
            response_data=data

        serializer=GallerySerializer(response_data,many=True)

        return Response(
            {'data':serializer.data,
             'has_next_page':has_next_page},
             status=status.HTTP_200_OK)

# Endpoint to handle contact form submissions and send confirmation emails.
class ContactFormView(APIView):
    def post(self,request):
        serializer=ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            usermail = serializer.validated_data.get('usermail')
            username = serializer.validated_data.get('username')
            send_mail_users.delay(usermail,username)
            return Response({
                "message": "Message sent successfully! We will contact you soon."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
        


    
        

       