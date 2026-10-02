{
    "name": "Aurora Storefront - Blog",
    "version": "20.0.1.0.0",
    "category": "Website/Website",
    "summary": "Featured blog posts, Aurora blog cards and a ready-made blog block",
    "description": """
Aurora Storefront - Blog
========================

Installed automatically when both *Aurora Storefront* and *Blog* are
installed, so the theme never depends on the blog app:

* "Featured" flag on blog posts and a *Featured Blog Posts* data source;
* an Aurora card layout for Odoo's *Blog Posts* blocks (grid and carousel),
  with cover, category, date, reading time and teaser;
* a ready-made *Latest Stories* block in the Aurora group.
""",
    "author": "Aurora Theme Contributors",
    "website": "https://github.com/Adityashah1409/Theme-module",
    "license": "LGPL-3",
    "depends": ["website_aurora20", "website_blog"],
    "auto_install": True,
    "data": [
        "data/website_snippet_filter_data.xml",
        "views/blog_post_views.xml",
        "views/snippets.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_aurora20_blog/static/src/scss/blog.scss",
        ],
    },
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": False,
}
