from sqlalchemy.orm import joinedload, joinedload_all

from clld.db.meta import DBSession
from clld.db.models import common
from clld.web.util.helpers import linked_contributors, linked_references

from clld.web import datatables
from clld.web.datatables.base import (
    DataTable, Col, filter_number, LinkCol, DetailsRowLinkCol, IdCol, LinkToMapCol
)

from sails.models import FeatureDomain, Feature, sailsLanguage, Family, sailsValue, Designer


class FeatureIdCol(IdCol):
    def search(self, qs):
        if self.model_col:
            return self.model_col.contains(qs)

    def order(self):
        return Feature.sortkey_str, Feature.sortkey_int


class _FeatureDomainCol(Col):
    def __init__(self, *args, **kw):
        super(_FeatureDomainCol, self).__init__(*args, **kw)
        self.choices = [a.name for a in DBSession.query(FeatureDomain).order_by(FeatureDomain.name)]

    def order(self):
        return FeatureDomain.name

    def search(self, qs):
        return FeatureDomain.name.__eq__(qs)


class FeatureDomainCol(_FeatureDomainCol):
    def format(self, item):
        return item.featuredomain.name


class FamilyCol(Col):
    def format(self, item):
        return item.family.name

    def order(self):
        return Family.name

    def search(self, qs):
        return Family.name.contains(qs)


class Features(datatables.Parameters):
    def base_query(self, query):
        return query.join(Designer).options(joinedload_all(Feature.designer))\
            .join(FeatureDomain).options(joinedload_all(Feature.featuredomain))

    def col_defs(self):
        return [
            FeatureIdCol(self, 'Id', sClass='left', model_col=Feature.id),
            LinkCol(self, 'Feature', model_col=Feature.name),
            FeatureDomainCol(self, 'Domain'),
            Col(self, 'Designer', model_col=Designer.contributor, get_object=lambda i: i.designer), # get_object=lambda i: i.feature.designer),
            Col(self, 'Languages', model_col=Feature.representation),
            DetailsRowLinkCol(self, 'd', button_text='Values'),
        ]


class Languages(datatables.Languages):
    def base_query(self, query):
        return query.join(Family).options(joinedload_all(sailsLanguage.family)).distinct()

    def col_defs(self):
        return [
            LinkCol(self, 'Name', model_col=sailsLanguage.name),
            IdCol(self, 'ISO-639-3', sClass='left', model_col=sailsLanguage.id),
            #FamilyCol(self, 'Family'),
            Col(self, 'Family', model_col=Family.name, get_object=lambda i: i.family),
            Col(self, 'Features', model_col=sailsLanguage.representation),
            LinkToMapCol(self, 'm'),
        ]


class Designers(datatables.Contributions):
    def col_defs(self):
        return [
            Col(self, 'Designer', model_col=Designer.contributor),
            Col(self, 'Domain of Design', model_col=Designer.domain),
            Col(self, 'Citation', model_col=Designer.citation),
            Col(self, 'More Information', model_col=Designer.pdflink),
        ]


class Datapoints(DataTable):
    __constraints__ = [Feature, sailsLanguage]

    def base_query(self, query):
        query = query.join(sailsValue).options(joinedload_all(sailsValue.language)).join(sailsValue.parameter).options(joinedload_all(sailsValue.parameter)).distinct()
        if self.sailslanguage:
            query = query.filter(sailsValue.language_pk == self.sailslanguage.pk)
        if self.feature:
            query = query.filter(sailsValue.parameter_pk == self.feature.pk)
        return query

    def col_defs(self):
        cols = []
        if not self.sailslanguage:
            cols = cols + [LinkCol(self, 'Name', model_col=sailsLanguage.name, get_object=lambda i: i.language), IdCol(self, 'ISO-639-3', sClass='left', model_col=sailsLanguage.id, get_object=lambda i: i.language)]
        if not self.feature:
            cols = cols + [LinkCol(self, 'Feature', model_col=Feature.name, get_object=lambda i: i.parameter), FeatureIdCol(self, 'Feature Id', sClass='left', model_col=Feature.id, get_object=lambda i: i.parameter)]

        cols = cols + [
            LinkCol(self, 'Value'),
            Col(self, 'Source', model_col=sailsValue.source),
        ]
        return cols

    def get_options(self):
        if self.sailslanguage or self.feature:
            # if the table is restricted to the values for one language, the number of
            # features is an upper bound for the number of values; thus, we do not
            # paginate.
            return {'bLengthChange': False, 'bPaginate': False}


def includeme(config):
    config.register_datatable('contributions', Designers)
    config.register_datatable('values', Datapoints)
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Features)
