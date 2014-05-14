from clld.web.maps import ParameterMap, Map, CombinationMap

from sails.adapters import GeoJsonCDE


class FeatureMap(ParameterMap):
    def get_options(self):
        return {
            'center': {"lon": 289.564764, "lat": 1.745725},
            'icon_size': 20,
            'max_zoom': 9,
            'worldCopyJump': True,
            'info_query': {'parameter': self.ctx.pk}}


class LanguageMap(Map):
    def get_options(self):
        return {'center': {"lon": -70.564764, "lat": 1.745725}}


class CombinedMap(CombinationMap):
    __geojson__ = GeoJsonCDE

    def get_options(self):
        return {'icon_size': 20, 'hash': True, 'center': {"lon": 289.564764, "lat": 1.745725}}


def includeme(config):
    config.register_map('languages', LanguageMap)
    config.register_map('parameter', FeatureMap)
