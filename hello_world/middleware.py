



#Global Middleware
class GlobalMiddleware:
    def resolve(self, next, root, info, **kwargs):
        # Log the incoming query or mutation
        print(f"Received query or mutation: {info.field_name}")
        
        # Call the next middleware or resolver in the chain
        return next(root, info, **kwargs)



#Filed Level Middleware
class GlobalMiddleware:
    def resolve(self, next, root, info, **kwargs):
        # Log the incoming query or mutation
        if info.field_name == 'allCategory':
            print(f"Received query or mutation: {info.field_name}")
        
        # Call the next middleware or resolver in the chain
        return next(root, info, **kwargs)
    
    
    

