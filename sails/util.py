import re

from sqlalchemy.orm import joinedload

from clld import RESOURCES
from clld.db.meta import DBSession
from clld.db.models.common import ValueSet
from clld.web.util.helpers import get_referents, external_link, link
from clld.web.util.multiselect import CombinationMultiSelect
from clld.web.icon import Icon
from clld.db.models.common import Source
from clld.interfaces import ILanguage

from sails.maps import LanguageMap
from sails.models import sailsValue, sailsLanguage


def icon_spec_factory(ctx, req):
    if ILanguage.providedBy(ctx):
        return ctx.family.jsondata['icon']

def icon_from_req(ctx, req):
    return Icon.from_req(ctx, req, icon_spec_factory=icon_spec_factory)


def language_index_html(context=None, request=None, **kw):
    return dict(map_=LanguageMap(context, request, col='Family', dt=context))


def dataset_detail_html(context=None, request=None, **kw):
    return {
        'stats': context.get_stats([
            rsc for rsc in RESOURCES if rsc.name in ['language', 'parameter', 'value']]),
        'stats_datapoints': "TODO"
    }


def source_detail_html(context=None, request=None, **kw):
    return {'referents': get_referents(context)}


def _valuesets(parameter):
    return DBSession.query(ValueSet)\
        .filter(ValueSet.parameter_pk == parameter.pk)\
        .options(
            joinedload(ValueSet.language),
            joinedload(ValueSet.values).joinedload(sailsValue.domainelement))


def parameter_detail_html(context=None, request=None, **kw):
    return dict(select=CombinationMultiSelect(request, selected=[context]))


def parameter_detail_tab(context=None, request=None, **kw):
    query = _valuesets(context).options(
        joinedload(ValueSet.language).joinedload(sailsLanguage.family))
    return dict(datapoints=query)


def combination_detail_html(context=None, request=None, **kw):
    """feature combination view"""
    return dict(iconselect=True)


def markup_feature_desc(req, desc):
    for pattern, repl in [
        (r'WALS feature number:\s*(?P<id>[0-9]+)\s*\[http://wals\.info\]',
         lambda match: external_link(
            'http://wals.info/feature/%sA' % match.group('id'),
            label='WALS feature number %sA' % match.group('id'))),
        (r'Constenla feature number:\s*(?P<id>[a-z0-9]+)\s*\[[^\]]+\]',
         lambda match: link(
            req,
            Source.get('hvtypconstenlaintermedia'),
            label='Constenla feature number: ' + match.group('id')))]:
        desc = re.sub(pattern, repl, desc)

    return desc
