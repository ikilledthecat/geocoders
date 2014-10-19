import urllib
from .utils import simplejson, geocoder_factory

# http://api.yandex.ru/maps/geocoder/doc/desc/concepts/About.xml

def geocode(q, api_key=None, ll=None, spn=None, rspn=None, plng=None):
    args = {
        'geocode': q,
        'results': 1,
        'format': 'json',
        'lang': 'en-US',
    }
    if plng:
        args['plng'] = plng
    if ll and spn:
        ll = hasattr(ll, '__iter__') and ','.join(map(str, ll)) or ll
        args['ll'] = ll
        spn = hasattr(spn, '__iter__') and ','.join(map(str, spn)) or spn
        args['spn'] = spn
    if rspn and ll and spn:
        args['rspn'] = rspn

    url = 'http://geocode-maps.yandex.ru/1.x/?%s&lang=en-US' % urllib.urlencode(args)
    json = simplejson.load(urllib.urlopen(url))

    try:
        member = json['response']['GeoObjectCollection']['featureMember']\
            [0]['GeoObject']
        return (
            member['metaDataProperty']['GeocoderMetaData']['text'],
            tuple(map(float, member['Point']['pos'].split(' ')[::-1]))
        )
    except (KeyError, IndexError):
        return (None, (None, None))

geocoder = geocoder_factory(geocode, takes_api_key=False)
