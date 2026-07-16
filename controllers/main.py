import re
import unicodedata
from odoo import http
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from odoo.http import request


def custom_slugify(s):
    if not s:
        return ''
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[-\s]+', '-', s).strip('-')
    return s


class WebsiteBlogShortURL(WebsiteBlog):

    @http.route([
        '/blog',
        '/blog/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=True)
    def blogs(self, page=1, **post):
        # Override to prevent redirect to /blog/our-blog-1 if there is only 1 blog
        blogs = request.env['blog.blog'].search([('website_id', 'in', (False, request.website.id))])
        if len(blogs) == 1:
            return self.blog(blog=blogs[0], page=page, **post)
        return super().blogs(page=page, **post)

    @http.route(
        ['/blog/<string:post_slug>'],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def short_blog_post(
        self,
        post_slug,
        tag_id=None,
        page=1,
        enable_editor=None,
        **post
    ):
        # Find the blog post by checking its slugified name instead of its ID
        all_posts = request.env['blog.post'].search([])
        blog_post = all_posts.filtered(lambda p: custom_slugify(p.name) == post_slug)
        
        if not blog_post:
            # Fallback for old links that might still have the ID in them
            try:
                _, post_id = request.env['ir.http']._unslug(post_slug)
                if post_id:
                    blog_post = request.env['blog.post'].browse(post_id)
            except Exception:
                pass

        if not blog_post or not blog_post.exists():
            raise request.not_found()
            
        blog_post = blog_post[0]

        return super().blog_post(
            blog=blog_post.blog_id,
            blog_post=blog_post,
            tag_id=tag_id,
            page=page,
            enable_editor=enable_editor,
            **post
        )

    @http.route(
        ['/blog/<model("blog.blog"):blog>/<model("blog.post", "[(\'blog_id\',\'=\',blog.id)]"):blog_post>'],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def blog_post(
        self,
        blog,
        blog_post,
        tag_id=None,
        page=1,
        enable_editor=None,
        **post
    ):
        query_string = request.httprequest.query_string.decode("utf-8")
        target = blog_post.website_url
        if query_string:
            target = "%s?%s" % (target, query_string)
        return request.redirect(target, code=301)

    @http.route(
        ['/blog/<model("blog.blog"):blog>/post/<model("blog.post"):blog_post>'],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def old_blog_post(self, blog, blog_post, **post):
        return request.redirect(blog_post.website_url, code=301)
