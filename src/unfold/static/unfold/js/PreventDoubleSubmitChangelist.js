/* Changelist action/save button spinner — swaps the clicked submit button to a
   spinner and disables it, preventing double submits.
   Targets: ① #changelist-form (actions "Run" + list_editable save)
            ② any form with a data-spinner attribute (opt-in, e.g. upload forms).
   Companion of PreventDoubleSubmit.js (change_form only) — scopes must not overlap. */
(function () {
    "use strict";

    var style = document.createElement("style");
    style.textContent =
        "@keyframes udsc-spin{to{transform:rotate(360deg)}}" +
        ".udsc-spinner{display:inline-block;width:14px;height:14px;border:2px solid currentColor;" +
        "border-right-color:transparent;border-radius:9999px;animation:udsc-spin .6s linear infinite;" +
        "vertical-align:-2px;margin-right:6px;}";
    document.head.appendChild(style);

    function toSpinner(btn) {
        if (!btn || btn.dataset.udscSpinning) return;
        btn.dataset.udscSpinning = "1";
        // keep current width so the label→spinner swap doesn't shift layout
        btn.style.minWidth = btn.offsetWidth + "px";
        btn.innerHTML =
            '<span class="udsc-spinner" aria-hidden="true"></span>' +
            (btn.dataset.spinnerLabel || "Processing…");
        btn.setAttribute("aria-busy", "true");
        // disabling immediately would drop the submitter's name/value from the POST —
        // defer to the next tick, after the submit has been serialized.
        window.setTimeout(function () {
            btn.disabled = true;
        }, 0);
    }

    document.addEventListener(
        "submit",
        function (ev) {
            var form = ev.target;
            if (!(form instanceof HTMLFormElement)) return;
            if (form.id !== "changelist-form" && !form.hasAttribute("data-spinner")) return;
            toSpinner(ev.submitter || form.querySelector('button[type="submit"]'));
        },
        true,
    );
})();
