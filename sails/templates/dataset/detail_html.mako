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
The South American Indigenous Language Structures (SAILS) is a large database of grammatical properties of languages gathered from descriptive materials (such as reference grammars) by a team directed by Pieter Muysken. SAILS Online was programmed by Harald Hammarstr&ouml;m using the CLLD framework, with support from Robert Forkel.
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
SAILS Online is a publication, published by the
${h.external_link('http://www.eva.mpg.de', label='Max Planck Institute for Evolutionary Anthropology')}, by an authored team from the
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
Olga Krasnoukhova. 2014. Noun Phrase (NP). In Muysken, Pieter et al. (eds.) South American Indian Language Structures (SAILS) Online. Leipzig: Online Max Planck Institute of Evolutionary Anthropology. (Available at http://sails.clld.org)
</blockquote>
</p>
<p>
If you are citing all the data, use:
<blockquote>
Muysken, Pieter, Harald Hammarstr&ouml;m, Olga Krasnoukhova, Neele M&uuml;ller, Joshua Birchall, Simon van de Kerke, Loretta O'Connor, Swintha Danielsen, Rik van Gijn & George Saad. 2014. <I>South American Indigenous Language Structures (SAILS) Online</I>. Leipzig: Online Publication of the Max Planck Institute for Evolutionary Anthropology. (Available at http://sails.clld.org)
</blockquote>
</p>

<h3>Terms of use</h3>
<p>
The content of this web site is published under a Creative Commons Licence.
We invite the community of users to think about further applications for the available data
and look forward to your comments, feedback and questions.
</p>

<h3>Acknowledgements</h3>
<p>
SAILS Online was supported by funding from ERC, KNAW and Radboud University.
<table>
<tr>
<td>
 <img src="http://www.knaw.nl/nl/de-knaw/organisatie/shared/resources/images/KNAW_100pt_RGB.jpg" alt="http://www.knaw.nl" width="304">
</td>
<td>
 <img src="http://erc.europa.eu/sites/default/files/content/LOGO-ERC.jpg" alt="http://erc.europa.eu" width="104" height="142">
</td>
<td>
 <img src="http://www.ru.nl/publish/pages/610085/ru_nl_a4_pms.jpg" alt="http://www.ru.nl" width="204">
</td>
</table> 
</p>
