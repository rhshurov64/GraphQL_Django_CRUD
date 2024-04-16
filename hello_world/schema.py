import graphene
from graphene_django import DjangoObjectType
from work.models import Category, Product



class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name', 'products')

        
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id','name','category',)
        


class Query(graphene.ObjectType):
    all_category =  graphene.List(CategoryType)
    one_product =  graphene.Field(ProductType, id = graphene.Int(required=True))
    
    all_product = graphene.List(ProductType)
    one_product = graphene.Field(ProductType, id = graphene.Int(required=True))
    
        
    def resolve_all_category(root, info):
        return Category.objects.all()
        
    def resolve_all_product(root, info):
        return Product.objects.all()
    
    
    def resolve_one_category(root, info, id):
        return Category.objects.get(id=id)

    def resolve_one_product(root, info, id):
        return Product.objects.get(id=id)



class CreateCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
    
    category = graphene.Field(CategoryType)
    
    @staticmethod
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
    def mutate(root, info, name, category):
        category = Category.objects.get(id = category)
        product = Product(name=name, category=category)
        product.save()
        return CreateProductMutation(product = product)
    

        
    


class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()
    
    create_product  = CreateProductMutation.Field()
    

schema = graphene.Schema(query= Query, mutation= Mutation)
    
