# coding: utf8
import re
from itertools import groupby

from clld import RESOURCES
from clld.web.util.helpers import button, icon, JS_CLLD, get_referents, JS, external_link, link
from clld.web.util.multiselect import MultiSelect, CombinationMultiSelect
from clld.web.util.htmllib import HTML
from clld.web.icon import ICON_MAP
from clld.db.models.common import Source

import sails
from sails.maps import CombinedMap


def dataset_detail_html(context=None, request=None, **kw):
    return {
        'stats': context.get_stats([rsc for rsc in RESOURCES if rsc.name in ['language', 'parameter', 'value']]),
        'stats_datapoints': "TODO"
    }


def source_detail_html(context=None, request=None, **kw):
    return {'referents': get_referents(context)}


def parameter_detail_html(context=None, request=None, **kw):
    return dict(select=CombinationMultiSelect(request, selected=[context]))


def combination_detail_html(context=None, request=None, **kw):
    """feature combination view
    """
    return dict(
        select=CombinationMultiSelect(request, combination=context),
        map=CombinedMap(context, request))


def markup_feature_desc(req, desc):
    for pattern, repl in [
        ('WALS feature number:\s*(?P<id>[0-9]+)\s*\[http://wals\.info\]',
         lambda match: external_link(
            'http://wals.info/feature/%sA' % match.group('id'),
            label='WALS feature number %sA' % match.group('id'))),
        ('Constenla feature number:\s*(?P<id>[a-z0-9]+)\s*\[[^\]]+\]',
         lambda match: link(
            req,
            Source.get('hvtypconstenlaintermedia'),
            label='Constenla feature number: ' + match.group('id')))]:
        desc = re.sub(pattern, repl, desc)

    return desc
