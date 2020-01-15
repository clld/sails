import itertools

from pyramid.config import Configurator
from clld.interfaces import (
    IParameter, IMapMarker, IDomainElement, IValue, ILanguage, IIconList,
)
from clld.web.adapters.base import adapter_factory
from clld.web.icon import Icon

# we must make sure custom models are known at database initialization!
from sails import models
from sails.interfaces import IConstruction

COLORS = [
    '0000dd', '000000', '66ff33', '99ffff', '009900', '9999ff', '990099', 'aa0000', 'cccccc',
    'dd0000', 'ff66ff', 'ff4400', 'ff6600', 'ffcc00', 'ffff00', 'ffffcc', 'ffffff']
SHAPES = list('cdfst')


_ = lambda s: s
_('Parameters')
_('Parameter')
_('Contributions')


def map_marker(ctx, req):
    """to allow for user-selectable markers, we have to look up a possible custom
    selection from the url params.
    """
    icon_map = {i.name: i for i in req.registry.getUtility(IIconList)}
    icon = None
    if IValue.providedBy(ctx):
        icon = req.params.get(
            'v%s' % ctx.domainelement.number,
            ctx.domainelement.jsondata['icon'])
    elif IDomainElement.providedBy(ctx):
        icon = req.params.get('v' + str(ctx.number), ctx.jsondata['icon'])
    elif ILanguage.providedBy(ctx):
        icon = ctx.family.jsondata['icon']
    if icon and icon in icon_map:
        return icon_map[icon].url(req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    icons = [Icon(s + c) for s, c in itertools.product(SHAPES, COLORS)]

    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(map_marker, IMapMarker)
    config.registry.registerUtility(icons, IIconList)
    config.register_adapter(adapter_factory(
        'parameter/detail_tab.mako',
        mimetype='application/vnd.clld.tab',
        send_mimetype="text/plain",
        extension='tab',
        name='tab-separated values'), IParameter)
    config.register_resource('construction', models.sailsConstruction, IConstruction, with_index=True)
    return config.make_wsgi_app()
