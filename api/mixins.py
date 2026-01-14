from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import BlogUtils

# Base mixin to handle liking and unliking logic for different models (Blogs, Projects).
class BaseLikeToggleView(APIView):
    model_class=None
    foreign_key_field = ''
    def get(self, request, pk):
        ip = BlogUtils.get_user_ip(request)
        data = {
            'user_ip': ip,
            self.foreign_key_field: pk
        }
        # Check if this IP has already liked this item
        is_liked = self.model_class.objects.filter(**data).exists()
        return Response({'is_liked': is_liked})

    def post(self,request,pk):
        ip=BlogUtils.get_user_ip(request)
        data={
            'user_ip':ip,
            self.foreign_key_field:pk
        }

        is_liked=self.model_class.objects.filter(**data).exists()
        status_msg=''

        if is_liked:
            self.model_class.objects.filter(**data).delete()
            status_msg='unliked'
        else:
            self.model_class.objects.create(**data)
            status_msg='liked'
        
        count_data={self.foreign_key_field:pk}
        like_count=self.model_class.objects.filter(**count_data).count()
        return Response({
            'message':status_msg,
            'total_like':like_count
            })
    