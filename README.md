# Website Blog Short URL — Odoo 18

## Result

Default Odoo URL:

    https://example.com/blog/our-blog-1/my-first-post-2

New URL:

    https://example.com/blog/my-first-post-2

The numeric suffix is part of Odoo's normal record slug and is intentionally retained.

## Features

- Short blog post route: `/blog/<post-slug>`
- Existing long post URLs redirect with HTTP 301
- Pre-v14 `/blog/<blog>/post/<post>` URLs redirect with HTTP 301
- Standard `blog.post.website_url` uses the short URL
- Existing Odoo post template is reused
- Query-string parameters are retained during redirect
- No Odoo core files are modified

## Installation

1. Extract the ZIP.
2. Copy the `website_blog_short_url` directory into your custom addons path.
3. Restart Odoo.
4. Update Apps List.
5. Search for **Website Blog Short URL**.
6. Install it.
7. Clear browser cache and test using a published post.

## Important testing note

This module is designed primarily for a website using one blog. Odoo supports
multiple blogs and its default URL includes the blog slug to avoid ambiguity.

Test these URLs after installation:

- `/blog`
- `/blog/your-blog-slug`
- `/blog/your-post-slug`
- the old full post URL

If a blog and a post happen to have conflicting record slugs, keep unique names
or use Odoo's default URL structure.

## Uninstall

After uninstalling, Odoo automatically returns to its standard URL structure.
Old short URLs will no longer resolve unless you add redirects.
