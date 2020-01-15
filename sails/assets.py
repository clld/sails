import pathlib

from clld.web.assets import environment

import sails


environment.append_path(
    str(pathlib.Path(sails.__file__).parent.joinpath('static')), url='/sails:static/')
environment.load_path = list(reversed(environment.load_path))
