<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>

<h2>${_('Datapoint')} ${h.link(request, ctx.unit.language)} / ${h.link(request, ctx.unit)} / ${h.link(request, ctx.unitparameter)}</h2>

<dl>
<dt>Language:</dt>
<dd>${h.link(request, ctx.unit.language)}</dd>
<dt>Construction:</dt>
<dd>${h.link(request, ctx.unit)}</dd>
<dt>Construction Feature:</dt>
<dd>${h.link(request, ctx.unitparameter)} designed by ${ctx.unitparameter.designer.contributor}</dd>
<dt>Value:</dt>
<dd>${ctx.name}</dd>
<dt>Comment:</dt>
<dd>${ctx.comment}</dd>
<dt>Datapoint contributed by:</dt>
<dd>${ctx.contributed_datapoint}</dd>
<dt>Legal Values and Meanings:</dt>
<dd>${ctx.unitparameter.jsondata['vdoc']}</dd>
% if ctx.source:
<dt>Source:</dt>
<dd>${ctx.source}</dd>
% endif
<dt>Provenance:</dt>
<dd>${ctx.provenance}</dd>
</dl>
