from clld.web.maps import ParameterMap, Map, CombinationMap, Layer
from clld.web.util.helpers import JS, map_marker_img

from sails.adapters import GeoJsonLects, GeoJsonCDE

def map_params(req):
    res = {}
    try:
        if 'lat' in req.params and 'lng' in req.params:
            res['center'] = map(float, [req.params['lat'], req.params['lng']])
        if 'z' in req.params:
            res['zoom'] = int(req.params['z'])
    except (ValueError, TypeError):
        #print req.params
        pass
    return res

class FeatureMap(ParameterMap):
    def get_options(self):
        res = {
            'center': {"lon": 289.564764, "lat": 1.745725},
            'icon_size': 20,
            'max_zoom': 9,
            'worldCopyJump': True,
            'info_query': {'parameter': self.ctx.pk}}
        #print "Hello"
        res.update(map_params(self.req))
        return res

class LanguageMap(Map):
    def get_options(self):
        res = {'center': {"lon": -70.564764, "lat": 1.745725}}
        #print "Hello"
        res.update(map_params(self.req))
        return res


class FamilyMap(Map):
    def get_options(self):
        print "familymap"
        return {
            'icons': 'sailslettericons',
        }
    def get_layers(self):
        geojson = GeoJsonLects(self.ctx)
        for genus in self.ctx.genera:
            yield Layer(
                Family.name,
                geojson.render(family, self.req, dump=False),
                marker=map_marker_img(self.req, family))



class CombinedMap(CombinationMap):
    __geojson__ = GeoJsonCDE

    def get_options(self):
        res = {'icon_size': 20, 'hash': True, 'center': {"lon": 289.564764, "lat": 1.745725}}
        res.update(map_params(self.req))
        return res


def includeme(config):
    config.register_map('languages', LanguageMap)
    config.register_map('parameter', FeatureMap)
    config.register_map('family', FamilyMap)

