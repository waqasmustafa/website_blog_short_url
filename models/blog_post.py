from odoo import models
from odoo.addons.http_routing.models.ir_http import slugify


class BlogPost(models.Model):
    _inherit = "blog.post"

    def _compute_website_url(self):
        super()._compute_website_url()
        for blog_post in self:
            if blog_post.id:
                blog_post.website_url = "/blog/%s" % slugify(blog_post.name or '')
