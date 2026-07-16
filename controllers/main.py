from odoo import http
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from odoo.http import request


class WebsiteBlogShortURL(WebsiteBlog):

    @http.route(
        ['/blog/<model("blog.post"):blog_post>'],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def short_blog_post(
        self,
        blog_post,
        tag_id=None,
        page=1,
        enable_editor=None,
        **post
    ):
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
