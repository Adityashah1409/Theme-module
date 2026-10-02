from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestAuroraBlog(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("base.default_website")
        blog = cls.env["blog.blog"].create({"name": "Aurora Journal"})
        Post = cls.env["blog.post"]
        cls.featured = Post.create({
            "name": "Aurora Featured Story",
            "blog_id": blog.id,
            "is_published": True,
            "aurora_is_featured": True,
            "content": "<p>%s</p>" % ("word " * 450),
        })
        cls.regular = Post.create({
            "name": "Aurora Regular Story",
            "blog_id": blog.id,
            "is_published": True,
            "content": "<p>Short.</p>",
        })
        cls.featured_draft = Post.create({
            "name": "Aurora Featured Draft",
            "blog_id": blog.id,
            "is_published": False,
            "aurora_is_featured": True,
        })

    def _render(self, filter_xmlid, template_key):
        return self.make_jsonrpc_request("/website/snippet/filters", {
            "filter_id": self.env.ref(filter_xmlid).id,
            "template_key": template_key,
            "limit": 16,
        })

    def test_reading_time(self):
        self.assertEqual(self.featured.aurora_reading_time, 3)
        self.assertEqual(self.regular.aurora_reading_time, 1)

    def test_featured_filter_lists_published_featured_posts_only(self):
        html = "".join(self._render(
            "website_aurora20_blog.dynamic_filter_featured_blog_posts",
            "website_blog.dynamic_filter_template_blog_post_card",
        ))
        self.assertIn("Aurora Featured Story", html)
        self.assertNotIn("Aurora Regular Story", html)
        self.assertNotIn("Aurora Featured Draft", html)

    def test_aurora_card_template(self):
        html = "".join(self._render(
            "website_blog.dynamic_filter_latest_blog_posts",
            "website_aurora20_blog.dynamic_filter_template_blog_post_aurora_card",
        ))
        self.assertIn("o_aurora_blog_card", html)
        self.assertIn("Aurora Featured Story", html)
        self.assertIn("Aurora Journal", html)
        self.assertIn("3 min read", " ".join(html.split()))

    def test_card_template_listed_for_blog_posts(self):
        templates = self.make_jsonrpc_request("/website/snippet/filter_templates", {"filter_name": "blog_post"})
        self.assertIn(
            "website_aurora20_blog.dynamic_filter_template_blog_post_aurora_card",
            [t["key"] for t in templates],
        )

    def test_block_renders(self):
        html = str(self.website.with_context(inherit_branding=False)._render_template(
            "website_aurora20_blog.s_aurora_blog_posts"))
        latest = self.env.ref("website_blog.dynamic_filter_latest_blog_posts")
        self.assertIn('data-filter-id="%s"' % latest.id, html)
        self.assertIn("dynamic_filter_template_blog_post_aurora_card", html)
        registration = self.env.ref("website_aurora20_blog.snippets")
        self.assertTrue(registration.active)
        self.assertIn("website_aurora20_blog.s_aurora_blog_posts", registration.arch)
