import itertools

from pyramid.config import Configurator
from clld.interfaces import (
    IParameter, IMapMarker, IDomainElement, IValue, ILanguage,
)
from clld.web.adapters.base import adapter_factory
from clld.web.icon import Icon

# we must make sure custom models are known at database initialization!
from sails import models
from sails.interfaces import IConstruction
from sails.util import icon_from_req

_ = lambda s: s
_('Parameters')
_('Parameter')
_('Contributions')


def map_marker(ctx, req):
    """to allow for user-selectable markers, we have to look up a possible custom
    selection from the url params.
    """
    return icon_from_req(ctx, req).url(req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(map_marker, IMapMarker)
    config.register_adapter(adapter_factory(
        'parameter/detail_tab.mako',
        mimetype='application/vnd.clld.tab',
        send_mimetype="text/plain",
        extension='tab',
        name='tab-separated values'), IParameter)
    config.register_resource('construction', models.sailsConstruction, IConstruction, with_index=True)
    return config.make_wsgi_app()
