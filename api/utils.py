from django.http import HttpRequest

# This class contains utility/helper functions for the application.
class BlogUtils:
    
    @staticmethod
    def get_user_ip(request: HttpRequest):
        """
        Retrieves the client's IP address from the request.
        It first checks for 'HTTP_X_FORWARDED_FOR' (often used with proxies/load balancers)
        and then falls back to 'REMOTE_ADDR'.
        """
        # Check if the request was forwarded through a proxy.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            # If multiple IPs exist, the first one is usually the original client IP.
            ip = x_forwarded_for.split(',')[0]
        else:
            # Otherwise, use the standard remote address.
            ip = request.META.get('REMOTE_ADDR')
        
        # Return the extracted IP or None if it couldn't be found.
        return ip if ip else None
