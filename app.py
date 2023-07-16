import openai
from git import Repo
from pathlib import Path
from secret import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

PATH_TO_BLOG_REPO = Path('/Users/ant/SE/Learning/python-openai/blog-post-generator/.git')
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG/"content"

PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

def update_blog(commit_message="update blog"):
    # Establish location
    print('updating')
    repo = Repo(PATH_TO_BLOG_REPO)
    # git add .
    repo.git.add(all=True)
    # git commit -m 'update blog'
    repo.index.commit(commit_message)
    # git push
    origin = repo.remote(name="origin")
    origin.push()

random_text_string = "fgrehiuswdjlscoaiehfgfgre"

with open(PATH_TO_BLOG/"index.html", "w") as f:
    print('writing')
    f.write(random_text_string)

update_blog()