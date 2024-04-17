from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name='products')
    
    def __str__(self):
        return self.name + '-' + str(self.category)
    
    
    
    


class Writer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title
