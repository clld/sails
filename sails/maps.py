from clld.web.maps import ParameterMap, Map, CombinationMap, FilterLegend

from sails.adapters import GeoJsonCDE


class FeatureMap(ParameterMap):
    def __init__(self, ctx, req, eid='map', col=None, dt=None):
        self.col, self.dt = col, dt
        ParameterMap.__init__(self, ctx, req, eid=eid)

    def get_options(self):
        return {
            'center': {"lon": 289.564764, "lat": 1.745725},
            'icon_size': 20,
            'max_zoom': 9,
            'worldCopyJump': True,
            'info_query': {'parameter': self.ctx.pk}}

    def get_legends(self):
        for legend in ParameterMap.get_legends(self):
            yield legend

        yield FilterLegend(self, 'SAILS.getFamily', col=self.col, dt=self.dt)


class LanguageMap(Map):
    def __init__(self, ctx, req, eid='map', col=None, dt=None):
        self.col, self.dt = col, dt
        Map.__init__(self, ctx, req, eid=eid)

    def get_options(self):
        return {'center': {"lon": -70.564764, "lat": 1.745725}}

    def get_legends(self):
        for legend in Map.get_legends(self):
            yield legend

        yield FilterLegend(self, 'SAILS.getFamily', col=self.col, dt=self.dt)


class CombinedMap(CombinationMap):
    __geojson__ = GeoJsonCDE

    def get_options(self):
        return {'icon_size': 20, 'hash': True, 'center': {"lon": 289.564764, "lat": 1.745725}}


def includeme(config):
    config.register_map('languages', LanguageMap)
    config.register_map('parameter', FeatureMap)
    config.register_map('combination', CombinedMap)
