//odoo.define('custom_addons.AccountPaymentPopOver', function (require) {
//    "use strict";
//
//    const AccountPaymentPopOver = require('account.AccountPaymentPopOver'); // Import the original class
//    const { patch } = require('web.utils'); // Use the patching mechanism for cleaner inheritance
//
//    props: {
//    // Existing properties
//    treatment_id: this.treatment_id,  // Add treatment_id here
//    ...
//}
//    // Extend the AccountPaymentPopOver component using the patching mechanism
//    patch(AccountPaymentPopOver.prototype, 'custom_addons.AccountPaymentPopOver', {
//        // Add custom events if needed
//        events: _.extend({}, AccountPaymentPopOver.prototype.events, {
//            'click .o_custom_button': '_onCustomButtonClick', // Example: Add a custom button event
//        }),
//
//        // Add or override methods as needed
//        _onCustomButtonClick: function () {
//            console.log("Custom button clicked");
//            // You can add custom logic here
//        },
//
//
//        // If needed, override init or other lifecycle methods
//        /**
//         * Override render to add additional logic or behavior.
//         */
//        render: function () {
//            this._super.apply(this, arguments); // Call the parent method
//            console.log("Custom render logic for AccountPaymentPopOver");
//        },
//    });
//
//    return AccountPaymentPopOver;
//});
