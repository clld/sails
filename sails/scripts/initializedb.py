import json
import collections

from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType
from csvw.dsv import reader

from sails import models


def typed(r, t):  # pragma: no cover
    if 'version' in r:
        del r['version']
    for k in r:
        if k.endswith('_pk') or k == 'pk' or k.endswith('_int'):
            r[k] = int(r[k]) if r[k] != '' else None
        elif k == 'jsondata':
            r[k] = json.loads(r[k]) if r[k] else None
        elif k in {'latitude', 'longitude'}:
            r[k] = float(r[k]) if r[k] != '' else None

    if t in {'editor.csv', 'contributioncontributor.csv'}:
        r['primary'] = r['primary'] == 't'
        r['ord'] = int(r['ord'])
    elif t == 'contribution.csv':
        r['date'] = None
    elif t in {'value.csv', 'unitvalue.csv'}:
        r['frequency'] = None
    elif t == 'source.csv':
        r['bibtex_type'] = r['bibtex_type'] or 'misc'
        r['bibtex_type'] = EntryType.get(r['bibtex_type'])
    return r


def main(args):  # pragma: no cover
    repos = args.cldf.directory.parent
    def iterrows(core, extended=False):
        res = collections.OrderedDict()
        for row in reader(repos / 'raw' / core, dicts=True):
            res[row['pk']] = row
        if extended:
            for row in reader(repos / 'raw' / extended, dicts=True):
                res[row['pk']].update(row)
        for r in res.values():
            yield typed(r, core)

    for stem, cls in [
        ('dataset', common.Dataset),
        ('contributor', common.Contributor),
        ('editor', common.Editor),
        ('source', common.Source),
        ('family', models.Family),
        ('featuredomain', models.FeatureDomain),
        ('constructionfeaturedomain', models.ConstructionFeatureDomain),
    ]:
        for row in iterrows(stem + '.csv'):
            DBSession.add(cls(**row))
        DBSession.flush()

    for row in iterrows('contribution.csv', extended='designer.csv'):
        DBSession.add(models.Designer(**row))
        DBSession.flush()

    for stem, cls in [
        ('identifier', common.Identifier),
    ]:
        for row in iterrows(stem + '.csv'):
            DBSession.add(cls(**row))
        DBSession.flush()

    for row in iterrows('language.csv', extended='sailslanguage.csv'):
        DBSession.add(models.sailsLanguage(**row))
        DBSession.flush()

    for row in iterrows('parameter.csv', extended='feature.csv'):
        DBSession.add(models.Feature(**row))
        DBSession.flush()

    for stem, cls in [
        ('languageidentifier', common.LanguageIdentifier),
        ('domainelement', common.DomainElement),
        ('valueset', common.ValueSet),
        ('languagesource', common.LanguageSource),
        ('valuesetreference', common.ValueSetReference),
    ]:
        seen = set()
        for row in iterrows(stem + '.csv'):
            if stem == 'valuesetreference':
                key = (row['valueset_pk'], row['source_pk'], row['description'])
                if key in seen:
                    continue
                seen.add(key)
            DBSession.add(cls(**row))
        DBSession.flush()

    for row in iterrows('value.csv', extended='sailsvalue.csv'):
        DBSession.add(models.sailsValue(**row))
        DBSession.flush()

    for row in iterrows('unit.csv', extended='sailsconstruction.csv'):
        DBSession.add(models.sailsConstruction(**row))
        DBSession.flush()

    for row in iterrows('unitparameter.csv', extended='sailsunitparameter.csv'):
        DBSession.add(models.sailsUnitParameter(**row))
        DBSession.flush()

    for row in iterrows('unitvalue.csv', extended='sailsunitvalue.csv'):
        DBSession.add(models.sailsUnitValue(**row))
        DBSession.flush()
