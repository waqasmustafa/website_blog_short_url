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
        domain = request.website.website_domain()
        blogs_list = request.env['blog.blog'].search(domain)
        
        if len(blogs_list) == 1:
            # 100% FOOLPROOF WAY: We bypass all Odoo methods (which cause redirects) 
            # and render the blog page template manually!
            blog = blogs_list[0]
            posts_domain = [('blog_id', '=', blog.id)]
            post_count = request.env['blog.post'].search_count(posts_domain)
            
            pager = request.website.pager(
                url='/blog',
                total=post_count,
                page=page,
                step=12,
            )
            posts = request.env['blog.post'].search(posts_domain, limit=12, offset=pager['offset'])
            
            values = {
                'blog': blog,
                'main_object': blog,
                'posts': posts,
                'pager': pager,
                'is_main_page': True,
                'active_tag_ids': [],
            }
            return request.render("website_blog.blog_post_short", values)

        # If there are 0 or >1 blogs, let Odoo handle it
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
        all_posts = request.env['blog.post'].search([])
        blog_post = all_posts.filtered(lambda p: custom_slugify(p.name) == post_slug)
        
        if not blog_post:
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
