from functools import wraps
def restrict_args_type (required_type):
    def decorator (func):
        @wraps (func)
        def wrapper ( * args):
            if not all ( isinstance (arg, required_type) for arg in args):
                raise ValueError ( f'All arguments must be { required_type . __name__ } ' )
            return func ( * args)
        return wrapper
    return decorator

if __name__ == '__main__':
    @restrict_args_type(int)
    def add_num (*arg):
        i= 0
        for element in arg:
            i+=element
        print (f'sum of elments {arg} is {i}')
    add_num(1,2,3,4)
