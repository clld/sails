<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>
<%! from sails.models import Designer %>


<h2>Welcome to SAILS Online</h2>

<p class="lead">
    The South American Indigenous Language Structures (SAILS) is a large database of
    grammatical properties of languages gathered from descriptive materials (such as
    reference grammars) by a team directed by Pieter Muysken. SAILS Online was programmed
    by Harald Hammarstr&ouml;m using the
    <span style="font-family: monospace">clld</span> framework, with support from Robert Forkel.
</p>

<p>
    SAILS consists of a number of data subsets (<a
        href="${request.route_url('contributions')}">domains</a>) for South American
    languages not all of which are uniform in terms of the languages covered or the design
    of the data:
</p>
<div>
    ${request.get_datatable('contributions', Designer, short=True).render()}
</div>


Note the following differences among the data subsets:
<ul>
    <li><b>Domain:</b> Some domains (NP, ARGEX, TAME, SUB) cover a certain typological
        division, while other domains cover a geographical area (FFQ, AND, IC)
        or a specific language family (ARW).
    </li>

    <li><b>Languages:</b>
        Four datasets (NP, ARGEX, TAME, SUB) span roughly the same sample of
        South American languages, while the other datasets overlap only
        sporadically with the aforementioned set and each other.
    </li>

    <li><b>Typology:</b>
        All datasets record structural characteristics of languages and one
        dataset (AND) also contains features sensitive to the form of certain
        key morphemes.
    </li>

    <li><b>Orientation:</b>
        All datasets except one (SUB) are language-based in their design,
        meaning that a language can logically take only one value per
        feature. The subordination (SUB) dataset is construction-based,
        meaning that a construction can logically take only one value per
        (construction-)feature, but a language can have any number of
        constructions. This difference calls for different browsing capabilities
        in that the language-based features can be found in the menu under Features
        and the construction-based data can be found under Constructions.
    </li>

    <li><b>Design space:</b> All features are designed such that the set of possible
        answers exhaust the logical possibilities for a language.
    </li>

    <li><b>Logical dependencies between features:</b> The NP, ARGEX, TAME, and SUB
        datasets are designed such that logical dependencies between features are absent
        except for a controlled kind of dependency with overarching versus specializing
        features. Such dependencies are indicated in the coding scheme of the feature id
        where X.1, X.2, .. X.n indicates that features X.1-X.n are logically dependent on
        the overarching feature X. To obtain only logically independent features one may
        simply use only the overarching features or use only the specializing features.
    </li>

</ul>

<p>
    Further information can be found in the descriptions of the individual
    (<a href="${request.route_url('contributions')}">domains</a>). All
    datasets were published online in 2014 except the SUB dataset which
    was published online in 2016. SAILS may be thus referred to as SAILS
    2014 and SAILS 2016 accordingly.

</p>

<p>
    SAILS Online is a publication, published by the
    ${h.external_link('http://http://www.eva.mpg.de', label='Department of Linguistic and Cultural Evolution')}
    at the Max Planck Institute for Evolutionary Anthropology, Leipzig, authored by a team
    from the Languages in Contact Group (LinC) at Radboud University Nijmegen.
</p>

<h3>How to use SAILS Online</h3>
<p>
    Using SAILS Online requires a browser with Javascript enabled.
</p>
<p>
    You find the features or languages of SAILS through the items "Features" and
    "Languages"
    in the navigation bar.
</p>

<h3>How to cite SAILS Online</h3>
<p>
    If you are citing data only from a specific <a
        href="${request.route_url('contributions')}">domain</a> of SAILS, cite the
    specific contribution, e.g., for the Noun Phrase (NP) domain:
</p>
<blockquote>
    Olga Krasnoukhova. 2016. Noun Phrase (NP). In Muysken, Pieter et al. (eds.) South
    American Indian Language Structures (SAILS) Online. Jena: Max Planck
    Institute for the Science of Human History. (Available at https://sails.clld.org)
</blockquote>
<p>
    If you are citing all the data, use:
</p>
<blockquote>
    Muysken, Pieter, Harald Hammarstr&ouml;m, Olga Krasnoukhova, Neele M&uuml;ller, Joshua
    Birchall, Simon van de Kerke, Loretta O'Connor, Swintha Danielsen, Rik van Gijn &
    George Saad. 2016. <i>South American Indigenous Language Structures (SAILS) Online</i>.
    Jena: Max Planck Institute for the Science of Human History.
    (Available at https://sails.clld.org)
</blockquote>

<h3>Terms of use</h3>
<p>
    The content of this web site is published under a Creative Commons Licence.
    We invite the community of users to think about further applications for the available
    data
    and look forward to your comments, feedback and questions.
</p>

<h3>Acknowledgements</h3>
<p>
    SAILS Online was supported by funding from ERC, KNAW and Radboud University Nijmegen.
</p>
<div class="span12">
    <table width="100%">
        <tr>
            <td style="text-align: center" width="33%">
                <img src="${req.static_url('sails:static/KNAW_100pt_RGB.jpg')}"
                     alt="https://www.knaw.nl" width="304">
            </td>
            <td style="text-align: center" width="33%">
                <img src="${req.static_url('sails:static/LOGO-ERC.jpg')}"
                     alt="https://erc.europa.eu" width="104" height="142">
            </td>
            <td style="text-align: center" width="33%">
                <img src="${req.static_url('sails:static/ru_nl.svg')}" width="250">
            </td>
    </table>
</div>
