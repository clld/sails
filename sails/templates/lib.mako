<%def name="languages_contextnav()">
<ul class="nav nav-tabs">
<li class="${'active' if request.matched_route.name == 'languages' else ''}">
<a href="${request.route_url('languages')}">Browse</a>
</li>
</ul>
</%def>
