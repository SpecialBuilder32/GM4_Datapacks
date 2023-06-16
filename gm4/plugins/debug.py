from beet import Context

def beet_default(ctx: Context):
    print("DEBUG CALLED!")
    print(ctx.directory)
    