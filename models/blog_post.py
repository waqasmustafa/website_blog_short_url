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


class BlogBlog(models.Model):
    _inherit = "blog.blog"

    def _compute_website_url(self):
        super()._compute_website_url()
        for blog in self:
            if blog.id:
                # If there's only 1 blog for this website, its URL is just /blog
                domain = [('website_id', 'in', (False, blog.website_id.id))] if blog.website_id else []
                blogs_count = self.env['blog.blog'].search_count(domain)
                
                if blogs_count == 1:
                    blog.website_url = "/blog"
                else:
                    blog.website_url = "/blog/%s" % custom_slugify(blog.name)


class BlogPost(models.Model):
    _inherit = "blog.post"

    def _compute_website_url(self):
        super()._compute_website_url()
        for blog_post in self:
            if blog_post.id:
                # Use custom slugify to avoid Odoo 18 import errors
                slug_name = custom_slugify(blog_post.name)
                blog_post.website_url = "/blog/%s" % slug_name
