from clld.web.assets import environment
from clldutils.path import Path

import sails


environment.append_path(
    Path(sails.__file__).parent.joinpath('static').as_posix(), url='/sails:static/')
environment.load_path = list(reversed(environment.load_path))
