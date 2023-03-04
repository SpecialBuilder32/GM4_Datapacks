from beet import Context, TextFile
import re
from pathlib import Path

REPLACEMENT_PATTERNS = {
    r"https:\/\/wiki\.gm4\.co\/wiki\/([\w_]+)": r"https:MY_URL\\\1"
}

def beet_default(ctx: Context):
    """Loads the README.md and modifies:
        - download links for respective download sites
        - pulls credits from beet.yaml and contributors.json
        - pulls YT link from beet.yaml"""
    readme_path = Path(ctx.project_id) / "README.md"
    my_readme = TextFile(source_path=readme_path)
        # this step handled by release plugin? doesnt seem to bind to ctx
    # my_readme = ctx.data.extra["README.md"]
    file_contents = my_readme.text

    # Credits
        # TODO replacement patterns gets added to?
    linked_credits = ctx.meta['linked_credits']
    credits_text = ""
    for title in linked_credits:
        credits_text += f"- {title}: {', '.join(linked_credits[title])}\n"
    REPLACEMENT_PATTERNS[r'<!-- *\$creditsInsert.+>'] = credits_text

    for pattern, repl in REPLACEMENT_PATTERNS.items():
        file_contents = re.sub(pattern, repl, file_contents)
        
    # add file to datapack, sending to release dir
    ctx.meta['MY_FILE'] = TextFile(file_contents) # can throw non output versions to the meta object 
        # to get dumped into the release directory in output.py
    ctx.data.extra["README.md"] = TextFile(file_contents)
