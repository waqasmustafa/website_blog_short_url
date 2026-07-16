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
        # Call the original method to let Odoo do its native filtering
        response = super().blogs(page=page, **post)
        
        # If Odoo tries to auto-redirect to a single blog (e.g. /blog/our-blog-1)
        if getattr(response, 'status_code', 200) in (301, 302, 303):
            location = getattr(response, 'location', '')
            if location.startswith('/blog/') and 'page/' not in location and 'tag/' not in location:
                # We catch the redirect and extract the blog it wanted to go to
                slug = location.split('/')[-1]
                try:
                    _, blog_id = request.env['ir.http']._unslug(slug)
                    if blog_id:
                        blog = request.env['blog.blog'].browse(blog_id)
                        if blog.exists():
                            # Render the blog inline without changing the URL
                            return self.blog(blog=blog, page=page, **post)
                except Exception:
                    pass
                    
        return response

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
