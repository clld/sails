from itertools import groupby

from clld import RESOURCES
from clld.web.util.helpers import button, icon, JS_CLLD, get_referents, JS
from clld.web.util.multiselect import MultiSelect, CombinationMultiSelect
from clld.web.util.htmllib import HTML
from clld.web.icon import ICON_MAP

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
