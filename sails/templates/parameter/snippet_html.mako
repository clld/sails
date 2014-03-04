<%namespace name="util" file="../util.mako"/>

% if ctx.description:
<p>
${ctx.description}
</p>
% endif

% if ctx.domain:
<% total = 0 %>
<table class="table table-hover table-condensed domain" style="width: auto;">
<thead>
<tr>
<th>&nbsp;</th><th>Value</th><th>Representation</th><th>Description</th>
</tr>
</thead>
<tbody>
        % for de in ctx.domain:
<tr>
<% total += len(de.values) %>
<td>${h.map_marker_img(request,de)}</td>
<td>${de.name}</td>
<td class="right">${len(de.values)}</td>
<td>${de.description}</td>
</tr>
        % endfor
<tr>
<td colspan="2" class="right"><b>Total:</b></td><td class="right">${total}</td><td>&nbsp;</td>
</tr>
</tbody>
</table>
% endif