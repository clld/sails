sails.NumberedDivIcon = L.Icon.extend({
    options: {
        number: '',
        className: 'my-div-icon'
    },
    createIcon: function () {
        var div = document.createElement('div');
        var img = this._createImg(this.options['iconUrl']);
        $(img).width(this.options['iconSize'][0]).height(this.options['iconSize'][1]);
        var numdiv = document.createElement('div');
        numdiv.setAttribute ( "class", "number" );
        $(numdiv).css({
            top: -this.options['iconSize'][0].toString() + 'px',
            left: 0 + 'px',
            'font-size': '12px'
        });
        numdiv.innerHTML = this.options['number'] || '';
        div.appendChild (img);
        div.appendChild (numdiv);
        this._setIconStyles(div, 'icon');
        return div;
    }
});

CLLD.MapIcons['sailslettericons'] = function(feature, size) {
    return new sails.NumberedDivIcon({
        iconUrl: url == feature.properties.icon,
        iconSize: [size, size],
        iconAnchor: [Math.floor(size/2), Math.floor(size/2)],
        popupAnchor: [0, 0],
        number: feature.properties.number
    });
}
