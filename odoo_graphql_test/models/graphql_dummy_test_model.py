import json
import logging

from odoo import models, fields, tools


_logger = logging.getLogger(__name__)


class GraphQLDummyDefaultTestModel(models.Model):
    _name = "graphql.dummy.default.test.model"

    date = fields.Date()
    datetime = fields.Datetime()
