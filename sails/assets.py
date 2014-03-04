from clld.web.assets import environment
from path import path

import sails


environment.append_path(
    path(sails.__file__).dirname().joinpath('static'), url='/sails:static/')
environment.load_path = list(reversed(environment.load_path))
