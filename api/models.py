from django.db import models
# Cloudinary is used for cloud-based image storage.
from cloudinary.models import CloudinaryField


# Model for blog posts containing title, category, image, and content.
class Blogmodel(models.Model):
    title=models.CharField(max_length=200)
    category=models.CharField(max_length=100)
    image=CloudinaryField('image')
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# Model to track users who liked a blog post, using their IP address.
class LikeTableBlog(models.Model):
    user_ip = models.CharField(max_length=50)
    liked_blog = models.ForeignKey(Blogmodel, on_delete=models.CASCADE)
    liked_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user_ip', 'liked_blog')

    def __str__(self):
        return f"{self.user_ip} liked {self.liked_blog.title}"

# Model for showcasing portfolio projects with links and tech stack.
class Projectmodel(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    techstack=models.CharField(max_length=200)
    image=CloudinaryField('image')
    livelink=models.URLField(max_length=400,null=True,blank=True)
    githublink=models.URLField(max_length=400,null=True,blank=True)

    def __str__(self):
        return self.title

# Model to track users who liked a project, using their IP address.
class LikeTableProjects(models.Model):
    user_ip = models.CharField(max_length=50)
    liked_project = models.ForeignKey(Projectmodel, on_delete=models.CASCADE)
    liked_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user_ip', 'liked_project')

    def __str__(self):
        return f"{self.user_ip} liked {self.liked_project.title}"

# Model for a gallery item featuring an image and a description.
class Gallerymodel(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    image=CloudinaryField('image')
    link=models.URLField(null=True,blank=True)
    posted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Model to store messages submitted via the contact form.
class ContactForm(models.Model):
    username=models.CharField(max_length=200)
    usermail=models.EmailField(max_length=400)
    message=models.TextField()
    send_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"message from: { self.username}"

# Model for comments on blog posts.
class CommentTable(models.Model):
    blog=models.ForeignKey(Blogmodel,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=200)
    comment=models.TextField()
    posted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} commented :{self.comment}"


    




