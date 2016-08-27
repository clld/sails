from sqlalchemy.orm import joinedload, joinedload_all, load_only

from clld.db.meta import DBSession
from clld.db.models import common

from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, DetailsRowLinkCol, IdCol, LinkToMapCol
from clld.web.datatables.value import Values, ValueNameCol, RefsCol
from clld.web.datatables.unitvalue import Unitvalues, UnitValueNameCol
#UnitValues, 

from sails.models import ConstructionFeatureDomain, FeatureDomain, Feature, sailsLanguage, Family, Designer, sailsUnitParameter, sailsConstruction, sailsUnitValue, sailsValue

class ConstructionFeatures(datatables.Unitparameters):
    def base_query(self, query):
        return query.join(ConstructionFeatureDomain).options(joinedload_all(sailsUnitParameter.constructionfeaturedomain))
    
    def col_defs(self):
        return [
            ConstructionFeatureIdCol(self, 'Id', sClass='left', model_col=sailsUnitParameter.id),
            LinkCol(self, 'Feature', model_col=sailsUnitParameter.name),
            ConstructionFeatureDomainCol(self, 'Domain'),
            Col(self, '# Constructions', model_col=sailsUnitParameter.nconstructions),
            Col(self, '# Languages', model_col=sailsUnitParameter.nlanguages),
            #DetailsRowLinkCol(self, 'd', button_text='Values'),
        ]


class FeatureIdCol(IdCol):
    def search(self, qs):
        if self.model_col:
            return self.model_col.contains(qs.upper())

    def order(self):
        return Feature.sortkey_str, Feature.sortkey_int

class ConstructionFeatureIdCol(IdCol):
    def search(self, qs):
        if self.model_col:
            return self.model_col.contains(qs.upper())

    def order(self):
        return sailsUnitParameter.sortkey_str, sailsUnitParameter.sortkey_int

class LanguageIdCol(Col):
    def format(self, item):
        item = self.get_obj(item)
        return '' if item.id.startswith('NOCODE') else item.id


class _FeatureDomainCol(Col):
    def __init__(self, *args, **kw):
        super(_FeatureDomainCol, self).__init__(*args, **kw)
        self.choices = [a.name for a in
                        DBSession.query(FeatureDomain).order_by(FeatureDomain.name)]

    def order(self):
        return FeatureDomain.name

    def search(self, qs):
        return FeatureDomain.name.__eq__(qs)

class _ConstructionFeatureDomainCol(Col):
    def __init__(self, *args, **kw):
        super(_ConstructionFeatureDomainCol, self).__init__(*args, **kw)
        self.choices = [a.name for a in DBSession.query(ConstructionFeatureDomain).order_by(ConstructionFeatureDomain.name)]

    def order(self):
        return ConstructionFeatureDomain.name

    def search(self, qs):
        return ConstructionFeatureDomain.name.__eq__(qs)


class FeatureDomainCol(_FeatureDomainCol):
    def format(self, item):
        return item.featuredomain.name

class ConstructionFeatureDomainCol(_ConstructionFeatureDomainCol):
    def format(self, item):
        return item.constructionfeaturedomain.name

class Features(datatables.Parameters):
    def base_query(self, query):
        return query.join(Designer).options(joinedload_all(Feature.designer))\
            .join(FeatureDomain).options(joinedload_all(Feature.featuredomain))

    def col_defs(self):
        return [
            FeatureIdCol(self, 'Id', sClass='left', model_col=Feature.id),
            LinkCol(self, 'Feature', model_col=Feature.name),
            FeatureDomainCol(self, 'Domain'),
            Col(self, 'Designer',
                model_col=Designer.contributor,
                get_object=lambda i: i.designer),
            Col(self, 'Languages', model_col=Feature.representation),
            DetailsRowLinkCol(self, 'd', button_text='Values'),
        ]


class FamilyCol(Col):
    def __init__(self, *args, **kw):
        kw['choices'] = [
            (f.pk, f.name) for f in DBSession.query(Family).order_by(Family.name)]
        kw['model_col'] = Family.name
        Col.__init__(self, *args, **kw)

    def search(self, qs):
        return Family.pk == int(qs)


class Languages(datatables.Languages):
    def base_query(self, query):
        return query.join(Family).options(joinedload_all(sailsLanguage.family)).distinct()

    def col_defs(self):
        return [
            LinkCol(self, 'Name', model_col=sailsLanguage.name),
            LanguageIdCol(self, 'ISO-639-3', sClass='left', model_col=sailsLanguage.id),
            FamilyCol(self, 'Family', get_object=lambda i: i.family),
            Col(self, 'Features', model_col=sailsLanguage.representation),
            LinkToMapCol(self, 'm'),
        ]


class Designers(datatables.Contributions):
    def __init__(self, dt, name, *args, **kw):
        self.short = kw.get('short')
        super(Designers, self).__init__(dt, name, *args, **kw)

    def base_query(self, query):
        if self.short:
            return datatables.Contributions.base_query(self, query).options(load_only("domain", "contributor", "nfeatures", "nlanguages", "ndatapoints"))
        return datatables.Contributions.base_query(self, query)
   
    def col_defs(self):
        #print "COL DEFS", self.short
        if self.short:
            return [
            Col(self, 'Domain of Design', model_col=Designer.domain),
            Col(self, 'Designer', model_col=Designer.contributor),
            Col(self, 'Features', model_col=Designer.nfeatures),
            Col(self, 'Languages', model_col=Designer.nlanguages),
            Col(self, 'Datapoints', model_col=Designer.ndatapoints),    
        ]
        return [
            Col(self, 'Designer', model_col=Designer.contributor),
            Col(self, 'Domain of Design', model_col=Designer.domain),
            Col(self, 'Citation', model_col=Designer.citation),
            Col(self, 'Features', model_col=Designer.nfeatures),
            Col(self, 'Languages', model_col=Designer.nlanguages),
            Col(self, 'Datapoints', model_col=Designer.ndatapoints),
            Col(self, 'More Information', model_col=Designer.more_information),
            Col(self, 'PDF Link', model_col=Designer.pdflink),
        ]

    def get_options(self):
        if self.short:
            return {'bLengthChange': False, 'bPaginate': False}
    
class Datapoints(Values):
    def base_query(self, query):
        query = Values.base_query(self, query)
        if self.language:
            query = query.options(
                joinedload_all(common.Value.valueset, common.ValueSet.parameter),
                joinedload(common.Value.domainelement),
            )
        elif self.parameter:
            query = query.outerjoin(Family)\
                .options(joinedload_all(
                    common.Value.valueset,
                    common.ValueSet.language,
                    sailsLanguage.family))
        return query

    def col_defs(self):
        name_col = ValueNameCol(self, 'value')
        if self.parameter and self.parameter.domain:
            name_col.choices = [de.name for de in self.parameter.domain]

        cols = []
        if self.parameter:
            cols = [
                LinkCol(
                    self, 'Name',
                    model_col=common.Language.name,
                    get_object=lambda i: i.valueset.language),
                LanguageIdCol(
                    self, 'ISO-639-3',
                    model_col=common.Language.id,
                    get_object=lambda i: i.valueset.language),
                FamilyCol(
                    self, 'Family',
                    get_object=lambda i: i.valueset.language.family)]
        elif self.language:
            cols = [
                FeatureIdCol(
                    self, 'Feature Id',
                    sClass='left', model_col=common.Parameter.id,
                    get_object=lambda i: i.valueset.parameter),
                LinkCol(
                    self, 'Feature',
                    model_col=common.Parameter.name,
                    get_object=lambda i: i.valueset.parameter)]

        cols = cols + [
            name_col,
            Col(self, 'description'),
            #RefsCol(self, 'source'),
            RefsCol(self, 'Source',
                model_col=common.ValueSet.source,
                get_object=lambda i: i.valueset),
            Col(self, 'Comment', model_col=sailsValue.comment)
        ]
        return cols

    def get_options(self):
        if self.language or self.parameter:
            # if the table is restricted to the values for one language, the number ofs
            # features is an upper bound for the number of values; thus, we do not
            # paginate.
            return {'bLengthChange': False, 'bPaginate': False}

class Constructions(datatables.Units):
    #def base_query(self, query):
    #    query = query.join(Language).options(joinedload(Unit.language))

    #    if self.language:
    #        return query.filter(Unit.language == self.language)
    #    return query

    def col_defs(self):
        return [
            LinkCol(
                self, 'language', model_col=common.Language.name, get_obj=lambda i: i.language),
            LinkCol(self, 'construction name'),
            #DescriptionLinkCol(self, 'description'),
        ]


class ConstructionValues(Unitvalues):
    def base_query(self, query):
        query = Unitvalues.base_query(self, query).options(joinedload_all(sailsUnitValue.unitparameter)) #.join(sailsLanguage).options(joinedload(common.UnitValue.unit, sailsConstruction.language))
        #if self.language:
        #    query = query.options(
        #        joinedload_all(common.Value.valueset, common.ValueSet.parameter),
        #        joinedload(common.Value.domainelement),
        #    )
        #elif self.unitparameter:
        #    query = query.outerjoin(Family)\
        #        .options(joinedload_all(
        #            common.Value.valueset,
        #            common.ValueSet.language,
        #            sailsLanguage.family))
        return query

    def col_defs(self):
        name_col = UnitValueNameCol(self, 'value')
        if self.unitparameter and self.unitparameter.domain:
            name_col.choices = sorted([de.name for de in self.unitparameter.domain])
        return [
            #LinkCol(
            #    self, 'language', model_col=sailsLanguage.name, get_obj=lambda i: i.unit.language.name),
            LinkCol(self, 'Construction', get_obj=lambda i: i.unit, model_col=common.Unit.name),
            ConstructionFeatureIdCol(self, 'Feature Id', sClass='left', model_col=sailsUnitParameter.id, get_obj=lambda i: i.unitparameter),
            LinkCol(self, 'Feature', get_obj=lambda i: i.unitparameter, model_col=common.UnitParameter.name),
            name_col,
            Col(self, 'Source', model_col=sailsUnitValue.source),
            Col(self, 'Comment', model_col=sailsUnitValue.comment)
        ]
        
def includeme(config):
    config.register_datatable('contributions', Designers)
    config.register_datatable('values', Datapoints)
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Features)
    
    config.register_datatable('unitparameters', ConstructionFeatures)
    config.register_datatable('constructions', Constructions)
    config.register_datatable('units', Constructions)
    config.register_datatable('unitvalues', ConstructionValues)
