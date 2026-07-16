{
    "name": "Website Blog Short URL",
    "version": "18.0.1.0.0",
    "summary": "Use /blog/post-title instead of /blog/blog-name/post-title",
    "description": """
Website Blog Short URL
======================

Changes blog post URLs from:

    /blog/our-blog-1/my-post-2

to:

    /blog/my-post-2

The original Odoo URL is permanently redirected (301) to the short URL.
The module also changes blog post website_url values so standard Odoo links,
search results, sharing links and canonical URLs use the short URL.
    """,
    "category": "Website/Website",
    "author": "Waqas Mustafa",
    "website": "https://apps.odoo.com/apps/modules/browse?search=waqas+mustafa",
    "license": "LGPL-3",
    "depends": ["website_blog"],
    "data": [],
    "installable": True,
    "application": False,
    "auto_install": False
}
