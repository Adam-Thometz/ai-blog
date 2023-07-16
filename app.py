import openai
import os
import shutil
from git import Repo
from pathlib import Path
from secret import OPENAI_API_KEY
from bs4 import BeautifulSoup as Soup

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

# random_text_string = "fgrehiuswdjlscoaiehfgfgre"

# with open(PATH_TO_BLOG/"index.html", "w") as f:
#     print('writing')
#     f.write(random_text_string)

# update_blog()

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

with open(PATH_TO_BLOG/"index.html") as index:
    soup = Soup(index.read())

def check_for_duplicate_links(path_to_new_content, links):
    urls = [str(link.get('href')) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls

def write_to_index(path_to_new_content):
    with open(PATH_TO_BLOG/"index.html") as index:
        soup = Soup(index.read())

    links = soup.find_all('a')
    last_link = links[-1]
    if check_for_duplicate_links(path_to_new_content, links):
        raise ValueError("Link already exists")
    
    link_to_new_blog = soup.new_tag('a', href=Path(*path_to_new_content.parts[-2:]))
    link_to_new_blog.string = path_to_new_content.name.split('.')[0]

    last_link.insert_after(link_to_new_blog)

    with open(PATH_TO_BLOG/"index.html", 'w') as f:
        f.write(str(soup.prettify(formatter='html')))

write_to_index(path_to_new_content)
update_blog()