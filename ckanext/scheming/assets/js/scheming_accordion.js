
this.ckan.module('scheming_accordion', function ($) {
  return {
    initialize: function () {

      this.el.on('click', this._onClick);
    },

    _onClick: function() {
        this.classList.toggle("accordion-expanded");
    }

  };
});