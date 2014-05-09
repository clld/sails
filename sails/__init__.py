import re
from functools import partial

from path import path
from clld.interfaces import IParameter, IMapMarker, IDomainElement, IValue, ILanguage
from clld.web.adapters.base import adapter_factory
from clld.web.app import get_configurator, menu_item


# we must make sure custom models are known at database initialization!
from sails import models


def map_marker(ctx, req):
    """to allow for user-selectable markers, we have to look up a possible custom
    selection from the url params.
    """
    icon_map = req.registry.settings['icons']
    icon = None
    if IValue.providedBy(ctx):
        icon = ctx.domainelement.jsondata['icon']
    elif IDomainElement.providedBy(ctx):
        icon = ctx.jsondata['icon']
    elif ILanguage.providedBy(ctx):
        icon = ctx.family.jsondata['icon']
    if icon:
        return req.static_url('clld:web/static/icons/' + icon + '.png')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['sitemaps'] = 'contribution parameter source valueset'.split()
    convert = lambda spec: ''.join(c if i == 0 else c + c for i, c in enumerate(spec))
    filename_pattern = re.compile('(?P<spec>(c|d|s|f|t)[0-9a-f]{3})\.png')
    icons = {}
    for name in sorted(
        path(__file__).dirname().joinpath('static', 'icons').files()
    ):
        m = filename_pattern.match(name.splitall()[-1])
        if m:
            icons[m.group('spec')] = convert(m.group('spec'))
    settings['icons'] = icons

    utilities = [(map_marker, IMapMarker)]
    config = get_configurator('sails', *utilities, **dict(settings=settings))
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('parameters', partial(menu_item, 'parameters', label='Features')),
        ('languages', partial(menu_item, 'languages')),
        ('sources', partial(menu_item, 'sources')),
        ('contributions', partial(menu_item, 'contributions', label="Designers")),
    )
    config.include('clldmpg')
    config.include('sails.adapters')
    config.include('sails.datatables')
    config.include('sails.maps')

    config.register_adapter(adapter_factory(
        'parameter/detail_tab.mako',
        mimetype='application/vnd.clld.tab',
        send_mimetype="text/plain",
        extension='tab',
        name='tab-separated values'), IParameter)

    return config.make_wsgi_app()
