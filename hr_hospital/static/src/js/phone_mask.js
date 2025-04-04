
odoo.define('hr_hospital.phone_mask', ['web.public.widget'], function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.PhoneMask = publicWidget.Widget.extend({
        selector: '.phone_mask',
        start: function () {
            this.$el.inputmask({
                mask: '+380 (99) 999-99-99',
                showMaskOnHover: false,
                clearIncomplete: true
            });
        },
    });

    return publicWidget.registry.PhoneMask;
});