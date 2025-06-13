/** @odoo-module */

import { NavBar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";

patch(NavBar.prototype, {

    onToggleMenu(ev) {
        $('.o_main_navbar').toggleClass('o_main_navbar_shown');
    },

});