import re
import unicodedata
from odoo import models


def custom_slugify(s):
    if not s:
        return ''
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[-\s]+', '-', s).strip('-')
    return s


class BlogPost(models.Model):
    _inherit = "blog.post"

    def _compute_website_url(self):
        super()._compute_website_url()
        for blog_post in self:
            if blog_post.id:
                # Use custom slugify to avoid Odoo 18 import errors
                slug_name = custom_slugify(blog_post.name)
                blog_post.website_url = "/blog/%s" % slug_name
