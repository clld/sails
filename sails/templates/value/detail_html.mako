<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>


<h2>${_('Datapoint')} ${h.link(request, ctx.valueset.language)} / ${h.link(request, ctx.valueset.parameter)}</h2>

<dl>
<dt>Language:</dt>
<dd>${h.link(request, ctx.valueset.language)}</dd>
<dt>Feature:</dt>
<dd>${h.link(request, ctx.valueset.parameter)} designed by ${ctx.valueset.parameter.designer.contributor}</dd>
<dt>Value:</dt>
<dd>${ctx.domainelement.name}</dd>
<dt>Datapoint contributed by:</dt>
<dd>${ctx.contributed_datapoint}</dd>
<dt>Comment:</dt>
<dd>${ctx.comment}</dd>
% if ctx.valueset.source:
<dt>Source:</dt>
<dd>${ctx.valueset.source}</dd>
% endif
<dt>Legal Values and Meanings:</dt>
<dd>

<table class="table table-hover table-condensed domain" style="width: auto;">
<thead>
<tr>
<th>Value</th><th>Meaning</th>
</tr>
</thead>
<tbody>
        % for de in ctx.valueset.parameter.domain:
<tr>
<td>${de.name}</td>
<td>${de.description}</td>
</tr>
        % endfor
</tbody>
</table>

</dd>

</dl>
