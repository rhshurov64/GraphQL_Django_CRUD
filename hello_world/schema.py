import graphene
from graphene_django import DjangoObjectType
from work.models import Category, Product, Writer, Post

from graphql_jwt.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

import graphql_jwt

from .middleware import GlobalMiddleware


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username')

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name', 'products')

        
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id','name','category',)
        

class WriterType(DjangoObjectType):
    class Meta:
        model = Writer
        fields = ('id', 'name', 'posts')
        
    
class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'writer')
        
    writer= graphene.Field(WriterType)
    


class Query(graphene.ObjectType):
    all_category =  graphene.List(CategoryType)
    one_product =  graphene.Field(ProductType, id = graphene.Int(required=True))
    
    all_product = graphene.List(ProductType)
    one_product = graphene.Field(ProductType, id = graphene.Int(required=True))
    
    
    nasted_post = graphene.List(PostType, id = graphene.Int(required=True), writer_id = graphene.Int(required=True))
    
    
    
    @login_required
    def resolve_nasted_post(root, info, id, writer_id):
        try:
            writer = Writer.objects.get(id=writer_id)
            post = Post.objects.get(id=id, writer=writer)
            return [post] if post else None
        except (Writer.DoesNotExist, Post.DoesNotExist):
            return None
    
    
    
    @login_required
    def resolve_all_category(root, info):
        return Category.objects.all()
    
    
    
    
    @login_required
    def resolve_all_product(root, info):
        return Product.objects.all()
    
    
    @login_required
    def resolve_one_category(root, info, id):
        return Category.objects.get(id=id)

    @login_required
    def resolve_one_product(root, info, id):
        return Product.objects.get(id=id)


    


class CreateCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
    
    category = graphene.Field(CategoryType)
    
    @staticmethod
    @login_required
    def mutate(root, info, name):
        category = Category(name=name)
        category.save()
        return CreateCategoryMutation(category=category)

class UpdateCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        name = graphene.String(required = True)
        
    category = graphene.Field(CategoryType)
    
    
    @staticmethod
    @login_required
    def mutate(root, info, id, name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return UpdateCategoryMutation(category=category)
    
class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        
    category = graphene.Field(CategoryType)
    
    @staticmethod
    @login_required
    def mutate(root, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return DeleteCategoryMutation(category = category)


class CreateProductMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        category = graphene.Int(required = True)
        
    product = graphene.Field(ProductType)
    
    @staticmethod
    @login_required
    def mutate(root, info, name, category):
        category = Category.objects.get(id = category)
        product = Product(name=name, category=category)
        product.save()
        return CreateProductMutation(product = product)
    

class UpdateProductMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        name = graphene.String(required = True)
        category = graphene.Int(required = True)
        
    product = graphene.Field(ProductType)
    
    @staticmethod
    @login_required
    def mutate(root, info, id, name, category):
        product = Product.objects.get(id=id)
        product.name = name
        product.category = Category.objects.get(id=category)
        product.save()
        return UpdateProductMutation(product = product)

class DeleteProductMutation(graphene.Mutation):
    
    class Arguments:
        id = graphene.Int(required = True)
        
    product = graphene.Field(ProductType)
    
    @staticmethod
    @login_required
    def mutate(root, info, id):
        product = Product.objects.get(id=id)
        product.delete()
        return DeleteProductMutation(product = product)
    
    
class LogoutMutation(graphene.Mutation):
    success = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(cls, info):
        logout(info.context)
        success = True
        return LogoutMutation(success=success)
    


    


class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()
    
    create_product  = CreateProductMutation.Field()
    update_product  = UpdateProductMutation.Field()
    delete_product  = DeleteProductMutation.Field()
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    
    logout = LogoutMutation.Field()
    

    

schema = graphene.Schema(query= Query, mutation= Mutation)

    
