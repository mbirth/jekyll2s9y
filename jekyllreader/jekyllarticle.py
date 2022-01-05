from functools import partial
from os.path import basename
import re
import frontmatter


class JekyllArticle():
    RE_IMG = r'!\[(.*?)\]\((.+?)( [\'"].+[\'"])?\)'
    RE_HTML_IMG = r'<img src="(.*?)"'
    RE_SITE_URL = r'\{\{ ?site\.url ?\}\}'

    def __init__(self, md_file: str, base_dir: str = "."):
        self.file_path = md_file
        self.base_dir = base_dir
        self.body = ""
        self.metadata = {}
        self.images = []
        self.replace_image_newpath = ""
        self.parse_file()
        self.collect_images()

    def parse_file(self):
        article = frontmatter.load(self.file_path)
        self.metadata = article.metadata
        self.body = article.content

        # Convert Twig highlights to Markdown Extra highlights
        self.body = re.sub(r'\{% highlight( (\S+)) %\}', r'```\2', self.body)
        self.body = re.sub(r'\{% endhighlight %\}', r'```', self.body)

    def collect_images(self):
        matches = re.findall(self.RE_IMG, self.body)   # Returns a tuple
        for match in matches:
            imgfile = match[1]
            imgfile = re.sub(self.RE_SITE_URL, self.base_dir, imgfile)
            self.images.append(imgfile)
        matches = re.findall(self.RE_HTML_IMG, self.body)   # Returns plain matches
        for match in matches:
            imgfile = match
            imgfile = re.sub(self.RE_SITE_URL, self.base_dir, imgfile)
            self.images.append(imgfile)
        self.images = list(set(self.images))

    def _replace_single_imagepath(self, match, new_base_url: str = ""):
        old_imgfile = match.group(2)
        old_imgfile = re.sub(self.RE_SITE_URL, self.base_dir, old_imgfile)
        img_name = basename(old_imgfile)
        new_imgfile = "{}{}".format(new_base_url, img_name)
        # print("Copying image {} to {} ...".format(old_imgfile, new_imgfile))
        # shutil.copyfile(old_imgfile, new_imgfile)
        img_title = ""
        if match.group(3):
            img_title = match.group(3)
        new_string = "![{}]({}{})".format(match.group(1), new_imgfile, img_title)
        return new_string

    def _replace_single_htmlimagepath(self, match, new_base_url: str = ""):
        old_imgfile = match.group(1)
        old_imgfile = re.sub(self.RE_SITE_URL, self.base_dir, old_imgfile)
        img_name = basename(old_imgfile)
        new_imgfile = "{}{}".format(new_base_url, img_name)
        new_string = "<img src=\"" + new_imgfile + "\""
        return new_string

    def replace_imagepaths(self, new_base_url: str = ""):
        # Images OLD: ![alt text]({{ site.url }}/assets/blah.jpg "title")
        # Images NEW: ![alt text](blah.jpg "title")
        self.body = re.sub(self.RE_IMG, partial(self._replace_single_imagepath, new_base_url=new_base_url), self.body)
        self.body = re.sub(self.RE_HTML_IMG, partial(self._replace_single_htmlimagepath, new_base_url=new_base_url), self.body)
