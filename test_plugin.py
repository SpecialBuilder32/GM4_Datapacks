from beet import Context

def say_hello(ctx: Context):
    print("Hello Action World")

def print_data(ctx):
    print(f"retrieved project {ctx.name}, {ctx.description}")
