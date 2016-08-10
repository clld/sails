<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "unitparameters" %>

<h2>${_('Construction Feature')} ${ctx.id}: ${ctx.name}</h2>

<dl>
<dt>Feature Possible Values:</dt>
<dd>${ctx.jsondata['vdoc']}</dd>
<dt>Feature Domain:</dt>
<dd>${ctx.constructionfeaturedomain.name}</dd>
<dt>Designer:</dt>
<dd>${ctx.designer.contributor}</dd>
<dt>Number of constructions with a definite datapoint:</dt>
<dd>${ctx.nconstructions}</dd>
<dt>Number of languages with at least one construction with a definite datapoint:</dt>
<dd>${ctx.nlanguages}</dd>
% if ctx.description:
    <dt>Additional Information:</dt>
    <dd>${u.markup_feature_desc(request, ctx.description)|n}</dd>
% endif
% if ctx.dependson:
<dt>Logically depends on:</dt>
<dd>${ctx.dependson}</dd>
% endif

</dl>

<div>
    <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'unitvalues'); dt = dt(request, h.models.UnitValue, unitparameter=ctx) %>
    ${dt.render()}
</div>


