<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "units" %>


<h2>${_('Construction')} ${ctx.name} ${_('in')} ${ctx.language.name}</h2>

<h3>${_('Values')}</h3>

<div>
    <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'unitvalues'); dt = dt(request, h.models.UnitValue, unit=ctx) %>
    ${dt.render()}
</div>
