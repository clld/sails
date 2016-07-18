import re

from pyramid.config import Configurator
from clld.interfaces import (
    IParameter, IMapMarker, IDomainElement, IValue, ILanguage, IIconList,
)
from clld.web.adapters.base import adapter_factory
from clld.web.icon import Icon
from clldutils.path import Path


# we must make sure custom models are known at database initialization!
from sails import models


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
    convert = lambda spec: ''.join(c if i == 0 else c + c for i, c in enumerate(spec))
    filename_pattern = re.compile('(?P<spec>(c|d|s|f|t)[0-9a-f]{3})\.png')
    icons = []
    for name in sorted(
            [fn.name for fn in
             Path(__file__).parent.joinpath('static', 'icons').glob('*.png')]):
        m = filename_pattern.match(name)
        if m:
            icons.append(Icon(convert(m.group('spec'))))

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

    return config.make_wsgi_app()
