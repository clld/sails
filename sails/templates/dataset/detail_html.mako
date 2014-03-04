<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
<div id="wals_search">
<script>
(function() {
var cx = '012093784907070887713:a7i_0y3rwgs';
var gcse = document.createElement('script');
gcse.type = 'text/javascript';
gcse.async = true;
gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
'//www.google.com/cse/cse.js?cx=' + cx;
var s = document.getElementsByTagName('script')[0];
s.parentNode.insertBefore(gcse, s);
})();
</script>
<gcse:search></gcse:search>
</div>
</%def>

<h2>Welcome to SAILS Online</h2>

<p class="lead">
The South American Indigenous Language Structures (SAILS) is a large database of grammatical properties of languages gathered from descriptive materials (such as reference grammars) by a team directed by Pieter Muysken.
</p>

<p>
<table class="table table-condensed">
 <thead>
<tr>
<th>Statistics</th>
<th></th>
</tr>
</thead>
<tr><td>Languages</td><td>${stats['language']}</td></tr>
<tr><td>Features</td><td>${stats['parameter']}</td></tr>
<tr><td>Datapoints</td><td>${stats['value']}</td></tr>
</table>
</p>



<p>
SAILS Online is a publication of the
${h.external_link('http://www.ru.nl/linc/', label='Languages in Contact Group (LinC) at Radboud University')}.
</p>

<h3>How to use SAILS Online</h3>
<p>
Using SAILS Online requires a browser with Javascript enabled.
</p>
<p>
You find the features or languages of SAILS through the items "Features" and "Languages"
in the navigation bar.
</p>

<h3>How to cite SAILS Online</h3>
<p>
If you are citing data only from a specific <a href="${request.route_url('contributions')}">domain</a> of SAILS, cite the specific contribution, e.g., for the Noun Phrase (NP) domain:
<blockquote>
Krasnoukhova, Olga. 2013. <I>The Noun Phrase in the Languages of South America</I>. Radboud Universiteit Nijmegen Doctoral Dissertation.
</blockquote>
</p>
<p>
If you are citing all the data, use:
<blockquote>
Muysken, Pieter, Harald Hammarstr&ouml;m, Olga Krasnoukhova, Neele M&uuml;ller, Joshua Birchall, Simon van de Kerke, Loretta O'Connor, Swintha Danielsen, Rik van Gijn & George Saad. 2014. <I>South American Indian Language Structures (SAILS) Online</I>. Online Publication of the Radboud University. (Available at http://sails.science.ru.nl)
</blockquote>
</p>

<h3>Terms of use</h3>
<p>
The content of this web site is published under a Creative Commons Licence.
We invite the community of users to think about further applications for the available data
and look forward to your comments, feedback and questions.
</p>