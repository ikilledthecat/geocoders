import urllib
from utils import make_nsfind, ET, geocoder_factory

# http://api.yandex.ru/maps/geocoder/doc/desc/concepts/About.xml

def geocode(q, api_key):
    find = make_nsfind({
        'ns0': 'http://www.opengis.net/gml',
        'ns1': 'http://maps.yandex.ru/geocoder/1.x',
        'ns2': 'http://www.opengis.net/gml',
    })
    args = {
        'geocode': q,
        'key': api_key,
        'results': 1,
    }
    url = 'http://geocode-maps.yandex.ru/1.x/?%s' % urllib.urlencode(args)
    et = ET.parse(urllib.urlopen(url))

    result = find(et, '//ns0:featureMember')
    if result:
        name = find(et, '//ns1:text').text
        lon, lat = map(float, find(et, '//ns2:pos').text.split(' '))

        return (name, (lat, lon))

    return (None, (None, None))

geocoder = geocoder_factory(geocode)
