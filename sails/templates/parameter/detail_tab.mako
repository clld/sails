iso-639-3 name value description latitude longitude family
% for vs in sorted(datapoints, key=lambda i: i.language.name):
${vs.language.id}	${vs.language.name|n}	${vs.values[0].domainelement.name}	${vs.values[0].domainelement.description|n}	${vs.language.latitude}	${vs.language.longitude}	${vs.language.family.name|n}
% endfor