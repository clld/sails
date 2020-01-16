import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get', '/parameters/AND2.tab'),
        ('get_html', '/parameters/NP740'),
        ('get_html', '/parameters/NP740?z=5&lat=0.5&lng=0.5'),
        ('get_html', '/parameters/NP740?z=ff&lat=pp&lng=yy'),
        ('get_json', '/parameters/NP740.geojson?domainelement=NP740-1'),
        ('get_html', '/combinations/AND3_AND4?v1=cff4400'),
        ('get_html', '/sources/sdricharabela'),
        ('get_html', '/languages'),
        ('get_dt', '/values?parameter=AND1'),
        ('get_html', '/languages.map.html?sEcho=1&sSearch_2=araw'),
        ('get_dt', '/parameters?sSearch_0=AND&iSortingCols=1&iSortCol_0=0'),
        ('get_dt', '/parameters?sSearch_2=And&iSortingCols=1&iSortCol_0=2'),
        ('get_html', '/contributions'),
        ('get_dt', '/values?language=qux'),
        ('get_html', '/values.map.html?parameter=AND1&sEcho=1'),
        ('get_html', '/valuesets/ARGEX2-12-xwa'),
        ('get_html', '/values/NP221-cub'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
