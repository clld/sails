<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">${_('Authors')}</%block>

<h2>${_('Authors/Domains')}</h2>

<p>
SAILS Online is organised by domains. Some domains (NP, ARGEX, TAME, SUB) cover
a certain typological division, while other domains cover a geographical
area (FFQ, AND, IC) or a specific language family (ARW). Typically one
author of the team designed the feature sets for each domain,
but there are deviations. The same author also filled in most datapoints
for his/her domain, but further individuals may have contributed datapoints
and indicated as such at the details page for individual datapoints.
</p>

<div>
${ctx.render()}
</div>

