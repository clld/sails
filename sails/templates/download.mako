<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>


<h3>Downloads</h3>

<div class="alert alert-info">
    <p>
        SAILS Online serves the latest
        ${h.external_link('https://github.com/cldf-datasets/sails/releases', label='released version')}
        of data curated at
        ${h.external_link('https://github.com/cldf-datasets/sails', label='cldf-datasets/sails')}.
        All released versions in CLDF format are accessible via <br/>
        <a href="https://doi.org/10.5281/zenodo.3608861"><img
                src="https://zenodo.org/badge/DOI/10.5281/zenodo.3608861.svg" alt="DOI"></a>
        <br/>
        on ZENODO as well.
    </p>
</div>
