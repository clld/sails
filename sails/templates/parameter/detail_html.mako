<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<% values = request.get_datatable('values', h.models.Value, parameter=ctx) %>

<%block name="title">Feature ${ctx.id}: ${ctx.name}</%block>

<%block name="head">
<link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
<script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
${util.head_coloris()|n}
</%block>

<div class="span4" style="float: right; margin-top: 1em;">
    <%util:well title="Values">
        <table class="table table-condensed">
            % for de in ctx.domain:
            <tr>
                <td>${util.coloris_icon_picker(u.icon_from_req(de, req))|n}</td>
                <td>${de.name}</td>
                <td>${de.description}</td>
                <td class="right">${len(de.values)}</td>
            </tr>
            % endfor
        </table>
        ${util.parameter_map_reloader([u.icon_from_req(de, req) for de in ctx.domain])}
    </%util:well>
</div>

<h2>Feature ${ctx.id}: ${ctx.name}</h2>
<div>${h.alt_representations(req, ctx, doc_position='right', exclude=['snippet.html'])|n}</div>

<dl>
<dt>Feature Domain:</dt>
<dd>${ctx.featuredomain.name}</dd>
<dt>Designer:</dt>
<dd>${ctx.designer.contributor}</dd>
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
<form action="${request.route_url('select_combination')}">
<fieldset>
<p>
You may combine this feature with another one. Start typing the
feature name or number in the field below.
</p>
${select.render()}
<button class="btn" type="submit">Submit</button>
</fieldset>
</form>
</div>

<br style="clear: right"/>

% if request.map:
${request.get_map('parameter', dt=values, col='Family').render()}
% endif

${values.render()}
