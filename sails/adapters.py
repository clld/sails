from __future__ import unicode_literals

from sqlalchemy.orm import joinedload, joinedload_all
from clld.interfaces import ILanguage, IParameter, IIndex, IValue, ICldfConfig
from clld.web.adapters.base import Index
from clld.web.adapters.geojson import GeoJsonParameter
from clld.web.adapters.cldf import CldfConfig
from clld.web.maps import SelectedLanguagesMap
from clld.db.meta import DBSession
from clld.db.models.common import Value, ValueSet, DomainElement


class SAILSCldfConfig(CldfConfig):
    module = 'StructureDataset'

    def convert(self, model, item, req):
        res = CldfConfig.convert(self, model, item, req)

        if model == DomainElement:
            res['ID'] = res['ID'].replace('N/A', 'NA').replace('?', 'NN')

        if model == Value:
            res['Code_ID'] = res['Code_ID'].replace('N/A', 'NA').replace('?', 'NN')

        return res


class GeoJsonFeature(GeoJsonParameter):
    def feature_iterator(self, ctx, req):
        return DBSession.query(Value).join(DomainElement)\
            .filter(DomainElement.id == req.params.get('domainelement'))\
            .options(
                joinedload_all(Value.valueset, ValueSet.language),
                joinedload(Value.domainelement),
            )

    def get_language(self, ctx, req, value):
        return value.valueset.language

    def feature_properties(self, ctx, req, value):
        return {
            'values': list(value.valueset.values),
            'value_numeric': value.domainelement.number,
            'value_name': value.domainelement.name}


class MapView(Index):
    extension = str('map.html')
    mimetype = str('text/vnd.clld.map+html')
    send_mimetype = str('text/html')
    template = 'language/map_html.mako'

    def get_languages(self, ctx, req):
        return list(ctx.get_query(limit=8000))

    def template_context(self, ctx, req):
        languages = self.get_languages(ctx, req)
        return {
            'map': SelectedLanguagesMap(
                ctx, req, languages, geojson_impl=getattr(self, 'geojson_impl', None)),
            'languages': languages}


class GeoJsonSelectedValues(GeoJsonFeature):
    def feature_iterator(self, ctx, req):
        return ctx.get_query(limit=8000)


class ValueMapView(MapView):
    geojson_impl = GeoJsonSelectedValues

    def get_languages(self, ctx, req):
        return [v.valueset.language for v in ctx.get_query(limit=8000)]


def includeme(config):
    config.registry.registerUtility(SAILSCldfConfig(), ICldfConfig)
    config.register_adapter(GeoJsonFeature, IParameter)
    config.register_adapter(MapView, ILanguage, IIndex)
    config.register_adapter(ValueMapView, IValue, IIndex)
