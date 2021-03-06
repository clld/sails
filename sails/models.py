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
from clld.db.models.common import (
    Language,
    Parameter,
    Contribution,
    Value,
    Unit,
    UnitValue,
    UnitParameter,
    IdNameDescriptionMixin,
)
from sails import interfaces as sails_interfaces

# ----------------------------------------------------------------------------
# specialized common mapper classes
# ----------------------------------------------------------------------------
@implementer(sails_interfaces.IFamily)
class Family(Base, IdNameDescriptionMixin):
    pass


@implementer(interfaces.ILanguage)
class sailsLanguage(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    family_pk = Column(Integer, ForeignKey('family.pk'))
    family = relationship(Family, backref=backref("languages", order_by="Language.name"))
    representation = Column(Integer)


@implementer(interfaces.IValue)
class sailsValue(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    comment = Column(Unicode)
    example = Column(Unicode)
    contributed_datapoint = Column(Unicode)


class FeatureDomain(Base, IdNameDescriptionMixin):
    pass


class ConstructionFeatureDomain(Base, IdNameDescriptionMixin):
    pass


@implementer(interfaces.IContribution)
class Designer(CustomModelMixin, Contribution):
    """Contributions in SAILS are designers. These comprise a set of
    features with corresponding values and a descriptive text.
    """
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    domain = Column(Unicode)
    contributor = Column(Unicode)
    orientation = Column(Unicode)
    nlanguages = Column(Integer)
    nfeatures = Column(Integer)
    ndatapoints = Column(Integer)   
    pdflink = Column(Unicode)
    citation = Column(Unicode)
    more_information = Column(Unicode)


@implementer(interfaces.IParameter)
class Feature(CustomModelMixin, Parameter):
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


@implementer(interfaces.IUnitParameter)
class sailsUnitParameter(CustomModelMixin, UnitParameter):
    pk = Column(Integer, ForeignKey('unitparameter.pk'), primary_key=True)
    vdoc = Column(String)
    constructionfeaturedomain_pk = Column(Integer, ForeignKey('constructionfeaturedomain.pk'))
    constructionfeaturedomain = relationship(ConstructionFeatureDomain, lazy='joined')
    designer_pk = Column(Integer, ForeignKey('designer.pk'))
    designer = relationship(Designer, lazy='joined', backref="sailsunitparameters")
    dependson = Column(String)
    nconstructions = Column(Integer)
    nlanguages = Column(Integer)
    sortkey_str = Column(String)
    sortkey_int = Column(Integer)


@implementer(sails_interfaces.IConstruction)
class sailsConstruction(CustomModelMixin, Unit):
    pk = Column(Integer, ForeignKey('unit.pk'), primary_key=True)


@implementer(interfaces.IUnitValue)
class sailsUnitValue(CustomModelMixin, UnitValue):
    pk = Column(Integer, ForeignKey('unitvalue.pk'), primary_key=True)
    comment = Column(Unicode)
    source = Column(Unicode)
    provenance = Column(Unicode)
    contributed_datapoint = Column(Unicode)
