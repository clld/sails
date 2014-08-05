from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.versioned import Versioned
from clld.db.models.common import (
    Language,
    Parameter,
    Contribution,
    Value,
    IdNameDescriptionMixin,
)
from sails import interfaces as sails_interfaces


# ----------------------------------------------------------------------------
# specialized common mapper classes
# ----------------------------------------------------------------------------
@implementer(sails_interfaces.IFamily)
class Family(Base, IdNameDescriptionMixin, Versioned):
    pass


@implementer(interfaces.ILanguage)
class sailsLanguage(Language, CustomModelMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    family_pk = Column(Integer, ForeignKey('family.pk'))
    family = relationship(Family, backref=backref("languages", order_by="Language.name"))
    representation = Column(Integer)


@implementer(interfaces.IValue)
class sailsValue(Value, CustomModelMixin):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    comment = Column(Unicode)
    example = Column(Unicode)
    contributed_datapoint = Column(Unicode)


class FeatureDomain(Base, IdNameDescriptionMixin, Versioned):
    pass


@implementer(interfaces.IContribution)
class Designer(Contribution, CustomModelMixin, Versioned):
    """Contributions in SAILS are designers. These comprise a set of
    features with corresponding values and a descriptive text.
    """
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    domain = Column(Unicode)
    contributor = Column(Unicode)
    pdflink = Column(Unicode)
    citation = Column(Unicode)
    more_information = Column(Unicode)


@implementer(interfaces.IParameter)
class Feature(Parameter, CustomModelMixin, Versioned):
    """Parameters in SAILS are called feature. They are always related to one Designer.
    """
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    vdoc = Column(String)
    representation = Column(Integer)
    featuredomain_pk = Column(Integer, ForeignKey('featuredomain.pk'))
    featuredomain = relationship(FeatureDomain, lazy='joined')
    designer_pk = Column(Integer, ForeignKey('designer.pk'))
    designer = relationship(Designer, lazy='joined', backref="features")
    dependson = Column(String)
    sortkey_str = Column(String)
    sortkey_int = Column(Integer)

    def __solr__(self, req):
        res = Parameter.__solr__(self, req)
        res.update(featuredomain_t=self.featuredomain.name)
        return res
