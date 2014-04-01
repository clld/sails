from sqlalchemy.orm import joinedload, joinedload_all

from clld.db.meta import DBSession
from clld.db.models import common
from clld.web.util.helpers import linked_contributors, linked_references, external_link
from clld.web.util.htmllib import HTML

from clld.web import datatables
from clld.web.datatables.base import (
    DataTable, Col, filter_number, LinkCol, DetailsRowLinkCol, IdCol, LinkToMapCol
)
from clld.web.datatables.value import Values, ValueNameCol

from sails.models import FeatureDomain, Feature, sailsLanguage, Family, sailsValue, Designer


class FeatureIdCol(IdCol):
    def search(self, qs):
        if self.model_col:
            return self.model_col.contains(qs)

    def order(self):
        return Feature.sortkey_str, Feature.sortkey_int


class LanguageIdCol(Col):
    def format(self, item):
        item = self.get_obj(item)
        return '' if item.id.startswith('NOCODE') else item.id


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
            LanguageIdCol(self, 'ISO-639-3', sClass='left', model_col=sailsLanguage.id),
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
            Col(self, 'More Information', model_col=Designer.more_information),
        ]


class Datapoints(Values):
    def base_query(self, query):
        query = Values.base_query(self, query)
        if self.language:
            query = query.options(
                joinedload_all(common.Value.valueset, common.ValueSet.parameter),
                joinedload(common.Value.domainelement),
            )
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
                    get_object=lambda i: i.valueset.language)]
        elif self.language:
            cols = [
                LinkCol(
                    self, 'Feature',
                    model_col=common.Parameter.name,
                    get_object=lambda i: i.valueset.parameter),
                FeatureIdCol(
                    self, 'Feature Id',
                    sClass='left', model_col=common.Parameter.id,
                    get_object=lambda i: i.valueset.parameter)]

        cols = cols + [
            name_col,
            Col(self, 'description'),
            #RefsCol(self, 'source'),
            Col(self, 'Source',
                model_col=common.ValueSet.source,
                get_object=lambda i: i.valueset),
        ]
        return cols

    def get_options(self):
        if self.language or self.parameter:
            # if the table is restricted to the values for one language, the number of
            # features is an upper bound for the number of values; thus, we do not
            # paginate.
            return {'bLengthChange': False, 'bPaginate': False}


def includeme(config):
    config.register_datatable('contributions', Designers)
    config.register_datatable('values', Datapoints)
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Features)
