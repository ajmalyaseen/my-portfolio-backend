from django.http import HttpRequest
import hashlib

# Utility class for blog-related helper functions.
class BlogUtils:
    @staticmethod
    def get_user_ip(request:HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip=x_forwarded_for.split(',')[0]
        else:
            ip=request.META.get('REMOTE_ADDR')
        
        if not ip:
            return None
        
        hashed_ip=hashlib.sha256(ip.encode('utf-8')).hexdigest()
        return hashed_ip
    
