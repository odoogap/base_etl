// Copyright 2019 - 2019 OdooGap <info@odoogap.com> https://www.odoogap.com
// License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

odoo.define('base_etl.jsonb_widget', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');


    var FieldJsonb = AbstractField.extend({
        template: 'FieldJsonb',
        supportedFieldTypes: ['jsonb'],

        start: function () {
            var self = this;
            return this._super().then(function () {
                self.$el.text(this.value);
            });
        },

        _formatValue: function (value) {
            return JSON.stringify(value);
        },

        _renderReadonly: function () {
            this.$el.text(this._formatValue(this.value));
        },

        _renderEdit: function () {
            this.$el.text(this._formatValue(this.value));
        }
    });



registry.add('jsonb_widget', FieldJsonb);

return {
    FieldJsonb: FieldJsonb
};

});