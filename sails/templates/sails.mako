<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="header">
    <a href="${request.route_url('dataset')}">
        <img src="${request.static_url('sails:static/header.gif')}"/>
    </a>
</%block>

${next.body()}
