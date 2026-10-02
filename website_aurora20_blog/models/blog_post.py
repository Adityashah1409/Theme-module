import math

from odoo import api, fields, models

from odoo.addons.website.tools import text_from_html

WORDS_PER_MINUTE = 200


class BlogPost(models.Model):
    _inherit = "blog.post"

    aurora_is_featured = fields.Boolean(
        string="Featured",
        help="Listed by the 'Featured Blog Posts' data source of the blog blocks.",
    )
    aurora_reading_time = fields.Integer(
        string="Reading Time (minutes)", compute="_compute_aurora_reading_time",
    )

    @api.depends("content")
    def _compute_aurora_reading_time(self):
        for post in self:
            words = len(text_from_html(post.content or "", True).split())
            post.aurora_reading_time = max(1, math.ceil(words / WORDS_PER_MINUTE)) if words else 0
