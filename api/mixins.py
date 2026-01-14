from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import BlogUtils

# This Base Mixin provides a reusable logic for liking and unliking different models (like Blogs or Projects).
# It handles both checking the like status (GET) and toggling the like (POST).
class BaseLikeToggleView(APIView):
    # These must be defined in the child classes (e.g., LikeTableBlog, LikeTableProjects)
    model_class = None
    foreign_key_field = ''

    def get(self, request, pk):
        """
        Checks if the current user/visitor has already liked a specific item.
        """
        # 1. Try to get the unique 'visitor_id' from the frontend query parameters.
        visitor_id = request.query_params.get('visitor_id')
        
        # 2. If no visitor_id is provided, fallback to using the user's IP address.
        if not visitor_id:
            visitor_id = BlogUtils.get_user_ip(request)
            
        # Prepare search criteria (identifying the user by ID/IP and the specific item by its primary key).
        data = {
            'user_ip': visitor_id, # We store the unique visitor ID in the 'user_ip' database field.
            self.foreign_key_field: pk
        }
        
        # Check if a record exists in the database for this user and item.
        is_liked = self.model_class.objects.filter(**data).exists()
        
        return Response({'is_liked': is_liked})

    def post(self, request, pk):
        """
        Toggles the like status: if already liked, it removes it (unlike); if not, it adds it (like).
        """
        # 1. Get the 'visitor_id' from the request body.
        visitor_id = request.data.get('visitor_id')
        
        # 2. Fallback to IP address if visitor_id is missing.
        if not visitor_id:
            visitor_id = BlogUtils.get_user_ip(request)
            
        data = {
            'user_ip': visitor_id,
            self.foreign_key_field: pk
        }
        
        # Check if the user has already liked this item.
        is_liked = self.model_class.objects.filter(**data).exists()
        status_msg = ''

        if is_liked:
            # If already liked, delete the record (Unlike logic).
            self.model_class.objects.filter(**data).delete()
            status_msg = 'unliked'
        else:
            # If not liked yet, create a new record (Like logic).
            self.model_class.objects.create(**data)
            status_msg = 'liked'
        
        # Calculate the updated total like count for this specific item.
        count_data = {self.foreign_key_field: pk}
        like_count = self.model_class.objects.filter(**count_data).count()
        
        return Response({
            'message': status_msg,
            'total_like': like_count
        })