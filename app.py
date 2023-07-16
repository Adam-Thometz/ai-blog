import openai
import os
import shutil
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

def create_new_blog(title, content, cover_image="no_image.png"):
    cover_image = Path(cover_image)

    files = len(list(PATH_TO_CONTENT.glob("*.html")))
    new_title = f"{files+1}.html"
    path_to_new_content = PATH_TO_CONTENT/new_title

    shutil.copy(cover_image, PATH_TO_CONTENT)

    if not os.path.exists(path_to_new_content):
        # write a new html file
        with open(path_to_new_content, "w") as f:
            f.write('<!DOCTYPE HTML>\n')
            f.write('<html>\n')
            f.write('<head>\n')
            f.write(f'<title>{title}</title>\n')
            f.write('</head>\n')

            f.write('<body>\n')            
            f.write(f'<img src="{cover_image.name}" alt="Cover image for {title}"> <br />\n')
            f.write(f'<h1>{title}</h1>\n')
            # OpenAI --> ChatCompletion GPT --> "hello\nblog post\n"
            f.write(content.replace('\n', '<br />\n'))
            f.write('</body>\n')            
            f.write('</html>\n')
            print('blog created!')
            return path_to_new_content
    else:
        raise FileExistsError('File already exists, please check your name. Aborting...')
    
path_to_new_content = create_new_blog("Test", "frsbgirwygbrewliuyfrbwiueWBIWRUEVBWIRUY")