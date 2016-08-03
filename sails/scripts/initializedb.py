from __future__ import unicode_literals
import sys
import re
import io

import transaction
from pytz import utc
from datetime import date, datetime

#, glottocodes_by_isocode,
from clld.scripts.util import (
    initializedb, Data, gbs_func, bibtex2source
)
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import compute_language_sources
from clld.lib.bibtex import Record
from clldutils.misc import slug
from clldutils.path import Path

from sails import models
from sails.scripts import issues
from pyglottolog.api import Glottolog
import getpass

DATA_DIR = Path('data')
reline = re.compile("[\\n\\r]")
refield = re.compile("\\t")

GLOTTOLOG_REPOS = Path(grambank.__file__).parent.parent.parent.parent.joinpath(
    'glottolog3', 'glottolog') \
    if getpass.getuser() in ['robert', 'shh\\forkel'] \
    else Path('C:\\Python27\\glottolog\\')  # add your path to the glottolog repos clone here!


def savu(txt, fn):
    with io.open(fn, 'w', encoding="utf-8") as fp:
        fp.write(txt)

def dtab(fn="sails_neele.tab", encoding="utf-8"):
    lines = reline.split(loadunicode(fn, encoding="utf-8"))
    lp = [[x.strip() for x in refield.split(l)] for l in lines if l.strip()]
    topline = lp[0]
    lpd = [dict(zip(topline, l)) for l in lp[1:]]
    return lpd


def ktfbib(s):
    rs = [z.split(":::") for z in s.split("|||")]
    [k, typ] = rs[0]
    return (k, (typ, dict(rs[1:])))


def opv(d, func):
    n = {}
    for (i, v) in d.iteritems():
        n[i] = func(v)
    return n


def setd(ds, k1, k2, v=None):
    if k1 in ds:
        ds[k1][k2] = v
    else:
        ds[k1] = {k2: v}
    return


def grp2(l):
    r = {}
    for (a, b) in l:
        setd(r, a, b)
    return opv(r, lambda x: x.keys())


def paths_to_d(pths):
    if pths == [()] or pths == [[]]:
        return None
    z = grp2([(p[0], p[1:]) for p in pths])
    return opv(z, paths_to_d)


def paths(d):
    if not d:
        return set([])
    if type(d) == type(""):
        print d
    l = set([(k,) for (k, v) in d.iteritems() if not v])
    return l.union([(k,) + p for (k, v) in d.iteritems() if v for p in paths(v)])


def rangify(ranges):
    r = {}
    n = 1
    for (i, x) in enumerate(reversed(ranges)):
        r[i] = n
        n = n * x
    return [r[i] for i in reversed(range(len(r)))]

def sortinfo(fids, redigit = re.compile('([0-9]+)')):
    fidstr = dict([(fid, '--'.join([c for c in redigit.split(fid) if c.strip() and (c != "-") and not c.isdigit()])) for fid in fids])
    fidintdata = dict([(fid, [int(c) for c in redigit.split(fid) if c.isdigit()]) for fid in fids])
    fidintranges = opv(grp2([(i, x) for ii in fidintdata.itervalues() for (i, x) in enumerate(ii)]), max)
    rmul = rangify([fidintranges[i] for i in range(len(fidintranges))])
    fidint = opv(fidintdata, lambda ii, rmul=rmul: sum([a * b for (a, b) in zip(ii, rmul)]))
    return (fidstr, fidint)

def loadunicode(fn, encoding="utf-8"):
    with DATA_DIR.joinpath(fn).open(encoding=encoding) as fp:
        return fp.read()


reisobrack = re.compile("\[([a-z][a-z][a-z]|NOCODE\_[A-Z][^\s\]]+)\]")


def treetxt(txt):
    ls = [l.strip() for l in txt.split("\n") if l.strip()]
    r = {}
    thisclf = None
    for l in ls:
        o = reisobrack.search(l)
        if o:
            r[thisclf + (o.group(0)[1:-1],)] = None
        else:
            thisclf = tuple(l.split(", "))

    return paths_to_d(r.iterkeys())

def main(args):
    # http://clld.readthedocs.org/en/latest/extending.html
    data = Data(
        created=utc.localize(datetime(2013, 11, 15)),
        updated=utc.localize(datetime(2013, 12, 12)))
    icons = issues.Icons()

    languoids = list(Glottolog(GLOTTOLOG_REPOS).languoids())
    iso_to_gcs = grp2([(l.iso, l.id) for l in languoids]) #glottocodes = glottocodes_by_isocode(args.glottolog_dburi)
    iso_to_name = {l.iso: l.name for l in languoids}
    #Languages
    dp = dtab("dp.tab")
    lons = dict([(d['iso-639-3'], d['lon']) for d in dp])
    lats = dict([(d['iso-639-3'], d['lat']) for d in dp])

    tabfns = [fn.name for fn in DATA_DIR.glob('sails_*.tab')]
    print "Sheets found", tabfns
    ldps = [ld for fn in tabfns for ld in dtab(fn)]
    ldps = [dict([(k, v.replace(".", "-") if k in ['feature_alphanumid', 'value'] else v)
                  for (k, v) in ld.iteritems()]) for ld in ldps]
    ldcps = dtab("constructions_data.tab")
    lgs = dict([(ld['language_id'], ld['language_name'] if ld.has_key('language_name') else iso_to_name[ld['language_id']]) for ld in ldps + ldcps])
    nfeatures = opv(grp2([(ld['language_id'], ld['feature_alphanumid'])
                          for ld in ldps + ldcps if ld["value"] != "?"]), len)

    # Families
    fp = treetxt(loadunicode('lff.txt') + loadunicode('lof.txt'))
    ps = paths(fp)
    lg_to_fam = dict([(p[-1], p[0]) for p in ps])
    families = grp2([(lg_to_fam[lg], lg) for lg in lgs.keys()])
    ficons = dict(icons.iconizeall([
        f for (f, sailslgs) in families.iteritems() if len(sailslgs) != 1]).items() +
                  [(f, icons.graytriangle) for (f, sailslgs) in families.iteritems()
                   if len(sailslgs) == 1])
    for family in families.iterkeys():
        data.add(
            models.Family, family,
            id=family, name=family, jsondata={"icon": ficons[family]})

    DBSession.flush()

    # Lgs
    for lgid in lgs.iterkeys():
        lang = data.add(
            models.sailsLanguage, lgid,
            id=lgid,
            name=lgs[lgid],
            family=data["Family"][lg_to_fam[lgid]],
            representation=nfeatures[lgid],
            latitude=float(lats[lgid]),
            longitude=float(lons[lgid]))
        if not lgid.startswith('NOCODE'):
            iso = data.add(
                common.Identifier, lgid,
                id=lgid,
                name=lgid,
                type=common.IdentifierType.iso.value,
                description=lgs[lgid])
            data.add(common.LanguageIdentifier, lgid, language=lang, identifier=iso)
        if lgid in iso_to_gcs:
            gc = iso_to_gcs[lgid]
            gc = data.add(
                common.Identifier, 'gc' + lgid,
                id=gc,
                name=gc,
                type=common.IdentifierType.glottolog.value,
                description=lgs[lgid])
            data.add(common.LanguageIdentifier, lgid, language=lang, identifier=gc)
    DBSession.flush()

    # Domains
    for domain in set(ld['feature_domain'] for ld in ldps):
        data.add(models.FeatureDomain, domain, id=slug(domain), name=domain)
    DBSession.flush()

    # Designers
    designer_info = dict([(dd['designer'], dd) for dd in dtab("sailscontributions.tab")])
    designers = dict([(ld['designer'], ld['feature_domain']) for ld in ldps])
    citation_template = "%s. 2014. %s. In Muysken, Pieter et al. (eds.) "\
    "South American Indian Language Structures (SAILS) Online. Leipzig: Online "\
    "Max Planck Institute of Evolutionary Anthropology. "\
    "(Available at http://sails.clld.org)"
    for (designer_id, (designer, domain)) in enumerate(designers.iteritems()):
        data.add(
            models.Designer, designer,
            id=str(designer_id),
            name=designer_id,
            domain=designer_info[designer]["domain"],
            contributor=designer,
            citation=citation_template % (
                designer,
                designer_info[designer]["domain"]),
            more_information=designer_info[designer]["citation"])
    DBSession.flush()

    # Features
    fs = dict([(ld['feature_alphanumid'], ld) for ld in ldps])
    nameclash_fs = grp2([(ld['feature_name'], ld['feature_alphanumid']) for ld in ldps])
    fnamefix = {}
    for (dfeature, dfsids) in nameclash_fs.iteritems():
        if len(dfsids) != 1:
            print "Feature name clash", dfeature, dfsids
            for dfsid in dfsids:
                fnamefix[dfsid] = dfeature + " [%s]" % dfsid

    nlgs = opv(grp2([(ld['feature_alphanumid'], ld['language_id'])
                     for ld in ldps if ld["value"] != "?"]), len)

    (fidstr, fidint) = sortinfo(fs.keys())
    for (fid, f) in fs.iteritems():
        if nlgs[fid] == 0:
            continue
        data.add(
            models.Feature, fid,
            id=fid,
            name=fnamefix.get(fid, f['feature_name']),
            description=f['feature_information'],
            jsondata=dict(vdoc=f['feature_possible_values']),
            representation=nlgs[fid],
            designer=data["Designer"][f['designer']],
            dependson=f["depends_on"],
            featuredomain=data['FeatureDomain'][f["feature_domain"]],
            sortkey_str=fidstr[fid],
            sortkey_int=fidint[fid])

    DBSession.flush()

    fvs = dict([(ld['feature_alphanumid'], ld['feature_possible_values']) for ld in ldps])
    fvdesc = {}
    for (fid, vs) in fvs.iteritems():
        vdesclist = [veq.split("==") for veq in vs.split("||")]
        try:
            vdesc = dict([(v.replace(".", "-"), desc) for [v, desc] in vdesclist])
        except ValueError:
            print "Faulty value desc", vdesclist, vs
        if not vdesc.has_key("?"):
            vdesc["?"] = "Not known"
        if not vdesc.has_key("N/A") and fs[fid]["depends_on"]:
            vdesc["N/A"] = "Not Applicable"
        vi = dict([(v, i) for (i, v) in enumerate(sorted(vdesc.keys()))])
        vicons = icons.iconize(vi.keys())
        if len(vdesc) == 0:
            print "VDESC missing", vs, fid, v
        for (v, desc) in vdesc.iteritems():
            fvdesc[(fid, v)] = desc
            data.add(
                common.DomainElement, (fid, v),
                id='%s-%s' % (fid, v),
                name=v,
                description=desc,
                jsondata={"icon": vicons[v]},
                number=vi[v],
                parameter=data['Feature'][fid])
    DBSession.flush()

    done = set()
    for ld in ldps:
        parameter = data['Feature'][ld['feature_alphanumid']]
        language = data['sailsLanguage'][ld['language_id']]
        
        id_ = '%s-%s' % (parameter.id, language.id)

        if (ld['feature_alphanumid'], ld['value']) not in data['DomainElement']:
            print ld['feature_alphanumid'], ld['feature_name'], ld['language_id'], ld['value'], "not in the set of legal values"
            continue

        valueset = data.add(
            common.ValueSet,
            id_,
            id=id_,
            language=language,
            parameter=parameter,
            contribution=parameter.designer,
            source=ld["source"].strip() or None,
        )
        data.add(
            models.sailsValue,
            id_,
            id=id_,
            domainelement=data['DomainElement'][(ld['feature_alphanumid'], ld['value'])],
            jsondata={"icon": data['DomainElement'][(ld['feature_alphanumid'], ld['value'])].jsondata},
            description=fvdesc[(ld['feature_alphanumid'], ld['value'])],
            comment=ld["comment"],
            example=ld["example"],
            valueset=valueset,
            contributed_datapoint=ld["contributor"]
        )
        done.add(id_)

    fcstrs = dict([(ld['feature_alphanumid'].replace('.', "-"), ld) for ld in dtab("constructions_features.tab")])
    (fidstr, fidint) = sortinfo(fcstrs.keys())
    for (fid, ld) in fcstrs.iteritems():
        data.add(
            models.sailsUnitParameter, fid,
            id=fid,
            name=ld['feature_name'],
            description=ld['feature_information'],
            jsondata=dict(vdoc=ld['feature_possible_values']),
            designer=data["Designer"][f['designer']],
            dependson=f["depends_on"],
            featuredomain=data['FeatureDomain'][f["feature_domain"]],
            sortkey_str=fidstr[fid],
            sortkey_int=fidint[fid])
    DBSession.flush()

    #ldcps = dtab("constructions_data.tab")
    cs = set([(ld['construction_id'], ld['language_id']) for ld in ldcps])
    for (cid, lid) in cs:
        language = data['sailsLanguage'][lid]
        data.add(
            common.Unit, cid,
            id=cid,
            name=cid,
            language = language) 
    DBSession.flush()
        
    #done = set()
    dedup = opv(grp2([((ld['construction_id'], ld['feature_alphanumid'].replace('.', "-")), (ld["value"],) + tuple(ld.items())) for ld in ldcps]), max)
    #for (idd, lds) in dups.iteritems():
    #    if len(lds) > 1:
    #        print idd, lds
    for dld in dedup.itervalues():
        ld = dict(dld[1:])
        #print fid, ld['language_id'], ld['construction_id'], "HEJ"
        fid = ld['feature_alphanumid'].replace('.', "-")
        language = data['sailsLanguage'][ld['language_id']]
        construction = data['Unit'][ld['construction_id']]
        construction_feature = data['sailsUnitParameter'][fid]
        id_ = '%s-%s' % (construction.id, construction_feature.id)
        data.add(common.UnitValue, id_, id=id_, name=ld['value'], unit=construction, unitparameter=construction_feature, contribution=construction_feature.designer)
        #cstrs + cstr_features + languages?
        #source comment etc

        #done.add(id_)
    DBSession.flush()


        
    # Sources
    sources = [ktfbib(bibsource) for ld in ldps if ld.get('bibsources') for bibsource in ld['bibsources'].split(",,,")]
    for (k, (typ, bibdata)) in sources:
        rec = Record(typ, k, **bibdata)
        if not data["Source"].has_key(k):
            data.add(common.Source, k, _obj=bibtex2source(rec))
    DBSession.flush()

    for ld in ldps:
        sources = [ktfbib(bibsource) for bibsource in ld['bibsources'].split(",,,") if ld.get('bibsources')]
        for (k, (typ, bibdata)) in sources:
            parameter = data['Feature'][ld['feature_alphanumid']]
            language = data['sailsLanguage'][ld['language_id']]
            id_ = '%s-%s' % (parameter.id, language.id)
            data.add(
                common.ValueSetReference,
                "%s-%s" % (id_, k),
                valueset=data["ValueSet"][id_],
                source=data['Source'][k])
    DBSession.flush()

    dataset = common.Dataset(
        id="SAILS",
        name='SAILS Online',
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        description="Dataset on Typological Features for South American Languages, collected 2009-2013 in the Traces of Contact Project (ERC Advanced Grant 230310) awarded to Pieter Muysken, Radboud Universiteit, Nijmegen, the Netherlands.",
        domain='sails.clld.org',
        published=date(2014, 2, 20),
        contact='harald.hammarstroem@mpi.nl',
        license='http://creativecommons.org/licenses/by-nc-nd/2.0/de/deed.en',
        jsondata={
            'license_icon': 'http://wals.info/static/images/cc_by_nc_nd.png',
            'license_name': 'Creative Commons Attribution-NonCommercial-NoDerivs 2.0 Germany'})
    DBSession.add(dataset)
    DBSession.flush()

    editor = data.add(common.Contributor, "Harald Hammarstrom", id="Harald Hammarstrom", name="Harald Hammarstrom", email = "harald.hammarstroem@mpi.nl")
    common.Editor(dataset=dataset, contributor=editor, ord=0)
    DBSession.flush()

    #To CLDF
    cldf = {}
    for ld in ldps:
        parameter = data['Feature'][ld['feature_alphanumid']]
        language = data['sailsLanguage'][ld['language_id']]
        id_ = '%s-%s' % (parameter.id, language.id)
        if not id_ in done:
            continue
        dt = (lgs[ld['language_id']], ld['language_id'], ld['feature_alphanumid'] + ". " + ld['feature_name'], ld["value"], ld["comment"])
        cldf[dt] = None

    tab = lambda rows: u''.join([u'\t'.join(row) + u"\n" for row in rows])
    savu(tab([("Language", "iso-639-3", "Feature", "Value", "Comment")] + cldf.keys()), "sails.cldf")


    
def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    
    compute_language_sources()
    transaction.commit()
    transaction.begin()

    gbs_func('update', args)

if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
