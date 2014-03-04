<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">${_('Authors')}</%block>

<h2>${_('Authors')}</h2>
<div>
${ctx.render()}
</div>