import yaml
from jinja2 import FileSystemLoader, Environment
import os
import codecs
import markdown


CWD = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(CWD, 'output')


from base import Engine

e = Engine()

from os.path import join, exists


def index():
    news_f = open('content/news.yaml', 'r')
    news = yaml.load_all(news_f)

    blogs_f = open('content/blogs.yaml', 'r')
    blogs = yaml.load_all(blogs_f)

    temp = e.env.get_template('index.html')
    output_fn = e.get_root_fn('index.html')
    e.render_and_write(temp, dict(news=news, blogs=blogs), output_fn)

    news_f.close()
    blogs_f.close()

def about():
    temp = e.env.get_template('page.html')

    with codecs.open('content/about.md', 'r', encoding='utf-8') as f:
        content = f.read()
        content = markdown.markdown(content)

    output = join(OUTPUT_DIR, 'about.html')
    e.render_and_write(temp, dict(title='About IC3', content=content), output)


def people():
    output = join(OUTPUT_DIR, 'people.html')
    temp = e.env.get_template('people.html')
    html = temp.render()

    page_temp = e.env.get_template('page.html')
    e.render_and_write(page_temp, dict(title='People', content=html), output)

def partners():
    output = os.path.join(OUTPUT_DIR, 'partners.html')
    temp = e.env.get_template('page.html')

    with codecs.open('./content/partners.md', 'r', encoding='utf-8') as f:
        content = f.read()
        content = markdown.markdown(content)

    e.render_and_write(temp, dict(title='Partners', content=content), output)

def projects():
    output = os.path.join(OUTPUT_DIR, 'projects.html')
    with open('./content/projects.yaml', 'r') as c:
        data = yaml.load(c)

    temp = e.env.get_template('projects.html')
    e.render_and_write(temp, dict(
        title='Projects',
        challenges=data['challenges'],
        projects=data['projects']),
        output)

import os
import shutil
import errno

if __name__ == '__main__':
    if exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)

    index()
    about()
    people()
    partners()
    projects()

    try:
        shutil.copytree('static', join(OUTPUT_DIR, 'static'))
        shutil.copytree('images', join(OUTPUT_DIR, 'images'))
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise
