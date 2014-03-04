from clld.tests.util import TestWithSelenium

import sails


class Tests(TestWithSelenium):
    app = sails.main({}, **{'sqlalchemy.url': 'postgres://robert@/sails'})
