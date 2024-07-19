from beet import Context


def beet_default(ctx: Context):
    print(f"running debug for {ctx.project_id} (before beet.contrib.lantern_load)")
