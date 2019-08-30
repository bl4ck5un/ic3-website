import copy
import logging
import os
import re
import shutil
from os.path import exists

from jinja2 import FileSystemLoader, Environment

# filters
def dateformat(value, format='%b %d, %Y'):
    return value.strftime(format)

def prependsiteroot(path, root):
    if path.startswith('http://') or path.startswith('https://'):
        return path
    else:
        return '{}/{}'.format(root, path)


class StaticSiteGenerator(object):
    env = Environment(loader=FileSystemLoader('./templates/'))
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    site_root = '.'

    def __init__(self, deploy=False):
        self.def_cntx = dict(SITE_ROOT=self.site_root)
        print 'deploy: ' + str(deploy)
        if exists(StaticSiteGenerator.output_dir):
            shutil.rmtree(StaticSiteGenerator.output_dir)
        os.mkdir(StaticSiteGenerator.output_dir)

        # register custom filters
        self.env.filters['dateformat'] = dateformat
        self.env.filters['prependsiteroot'] = lambda path: prependsiteroot(path, self.site_root)

    def render(self, temp, cntx):
        x = copy.copy(cntx)
        x.update(self.def_cntx)
        return temp.render(x)

    def write(self, content, filename):
        with open(filename, 'w') as f:
            f.write(content)

    def write_utf8(self, content, filename):
        try:
            out = content.encode('utf-8')
        except Exception as e:
            logging.error(e)
            raise

        logging.debug("writing at {}: {}".format(filename, out))
        self.write(out, filename)

    def render_and_write(self, template, cntx, path):
        self.write_utf8(self.render(template, cntx), path)

    def default_context(self):
        return copy.copy(self.def_cntx)

    def calc_output_fullpath(self, fn):
        return os.path.join(self.output_dir, fn)

    def sanitize_filename(self, fn):
        s = re.sub('\s', '-', fn)
        return re.sub('[^0-9a-zA-Z-]', '', s)
