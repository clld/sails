"""

"""
import json
import pathlib
import contextlib
import collections

import transaction
from clldutils import db
from clldutils import clilib
from clld.scripts.util import SessionContext, ExistingConfig, get_env_and_settings
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType
from csvw.dsv import reader

import sails
from sails import models

PKG_DIR = pathlib.Path(sails.__file__).parent
PROJECT_DIR = PKG_DIR.parent

# FIXME:
# - source.bib - we should import source data from the bib file, because this can be easier
#   maintained.


def register(parser):  # pragma: no cover
    parser.add_argument(
        "--config-uri",
        action=ExistingConfig,
        help="ini file providing app config",
        default=str(PROJECT_DIR / 'development.ini'))
    parser.add_argument(
        '--doi',
        default=None,
    )
    parser.add_argument(
        '--repos',
        default=pathlib.Path(PROJECT_DIR.parent / 'sails-cldf'),
        help='Clone of cldf-datasets/sails',
        type=clilib.PathType(type='dir'),
    )


def run(args):  # pragma: no cover
    args.env, settings = get_env_and_settings(args.config_uri)

    with contextlib.ExitStack() as stack:
        stack.enter_context(db.FreshDB.from_settings(settings, log=args.log))
        stack.enter_context(SessionContext(settings))

        with transaction.manager:
            load(args.repos)


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


def load(repos):  # pragma: no cover
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
