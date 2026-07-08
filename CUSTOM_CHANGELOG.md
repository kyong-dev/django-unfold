## 0.43.0 (2024-12-28)

- Logentry saves both previous value and changed value in the database field

## 0.47.1 (2025-02-09)

- Change list entire row clickable except inputs

## 0.47.0 (2025-02-08)

- RangeDateFilter filter query changed from datetime to date

## 0.49.2.5 (2025-03-03)

- import_export logentry

## 0.51.0 (2025-03-16)

- django admin object history page order by recent action

## 0.53.0 (2025-03-28)

- Table component HTML tags available

## 0.58.1 (2025-05-25)

- Support adminsortable2 with django admin log
- Support group badge callback 

## 0.62.0 (2025-07-06)

- Change form submit button loading feature

## 0.62.0.3 (2025-07-09)

- Changelist custom_select_filters & custom_filter_script

## 0.89.0.1 (2026-06-09)

- Changelist submit bug fixed

```python
def changelist_view(self, request, extra_context=None):
    extra_context = extra_context or {}
    extra_context['custom_select_filters'] = [
        {"id": "all", "value": "/admin/user/user/", "label": "전체보기"},
        {"id": "exclude_test", "value": "?is_test__exact=0", "label": "테스트 제외"},
        {"id": "include_test", "value": "?is_test__exact=1", "label": "테스트"},
    ]
    extra_context['custom_filter_script'] = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const urlParams = new URLSearchParams(window.location.search);
        const isTestExact = urlParams.get('is_test__exact');
        
        const selectElement = document.getElementById('custom-filter-select');
        if (selectElement) {
            if (window.location.search.includes('is_test__exact=0')) {
                selectElement.value = 'exclude_test';
                document.querySelector('#custom-filter-select option[id="exclude_test"]').selected = true;
            } else if (window.location.search.includes('is_test__exact=1')) {
                selectElement.value = 'include_test';
                document.querySelector('#custom-filter-select option[id="include_test"]').selected = true;
            } else if (window.location.search === '' || window.location.pathname.endsWith('/')) {
                selectElement.value = 'all';
                document.querySelector('#custom-filter-select option[id="all"]').selected = true;
            }
        }
        
        if (selectElement) {
            selectElement.addEventListener('change', function() {
                const selectedOption = this.options[this.selectedIndex];
                if (selectedOption && selectedOption.dataset.url) {
                    window.location.href = selectedOption.dataset.url;
                }
            });
        }
    });
    </script>
    """
    return super().changelist_view(request, extra_context=extra_context)
```

## 0.63.0.1 (2025-07-24)

- Button Spinner
    modified:   src/unfold/templates/admin/actions.html
    modified:   src/unfold/templates/admin/pagination.html
    modified:   src/unfold/templates/admin/submit_line.html


## 0.67.0.1 (2025-10-06)

- Table div error fixed
    modified: src/unfold/templates/unfold/components/table.html


## 0.84.0.1 (2026-03-14)

- Hide nav-bar items the logged-in user is not authorized to access.


## 0.89.0.4 (2026-06-13)

- Changelist action/save button double-submit spinner
    added:      src/unfold/static/unfold/js/PreventDoubleSubmitChangelist.js
    modified:   src/unfold/templates/admin/change_list.html (script tag in {% block extrahead %})
    added:      tests/test_prevent_double_submit.py (guards both double-submit patches against upstream rebases)
    modified:   pyproject.toml (removed stale duplicate poetry-core [build-system] block left over from a merge — it made the TOML unparsable; name/version now committed as django-unfold-patrick)
    modified:   src/unfold/admin.py (removed stale pre-mixin copies of get_actions_list/_detail/_row/_submit_line and _filter_unfold_actions_by_permissions — merge residue that shadowed ActionModelAdminMixin and crashed dict-style dropdown actions with "TypeError: attribute name must be string"; 203 tests failed because of it, also broken in published 0.89.0.1–0.89.0.3)
    restored:   tests/__init__.py, tests/server/example/{__init__,settings,urls}.py, tests/server/example/migrations/__init__.py, tests/server/manage.py (test infra accidentally deleted by the 2025-03-02 "git cache cleared" commit — restored from merged upstream 6b62dcd; test suite was unrunnable without them)

    Contract (consumer projects, e.g. siseon, depend on this):
    - Always active for #changelist-form submits; any other form opts in via a data-spinner attribute.
    - Spinner label comes from the button's data-spinner-label attribute, fallback "Processing…".
    - Only the actually clicked button (ev.submitter) is swapped to a spinner.
    - disabled is applied on the next tick so the submitter's name/value stays in the POST.
    - Companion of PreventDoubleSubmit.js (change_form only) — template scopes do not overlap.


## 0.100.0.1 (2026-07-09)

- Changelist crash + table merge-residue fixed (merge b3fe7755 was committed with unresolved conflict markers in three files)
    modified:   src/unfold/templates/admin/change_list.html (botched conflict resolution left a duplicate inner {% block filters %} plus an unclosed <a> and {% if %} — two same-named blocks raise TemplateSyntaxError so the changelist would not render at all; removed the duplicate block, moved the change_list_filter_button.html include inside the anchor, closed </a> / {% endif %} / {% endblock %})
    modified:   src/unfold/templates/unfold/components/table.html (resolved leftover <<<<<<< HEAD / ======= / >>>>>>> b3fe7755 markers in the title <h3> block; also removed a stray </table> and a duplicated {% if not table.rows %} "No data" block at the empty-table footer that rendered "No data" twice — matched the tail to the clean b3fe7755 structure: one "No data" <p> then </div></div>. Recurrence of the 0.67.0.1 "Table div error fixed" issue)
    modified:   src/unfold/templatetags/unfold.py (resolved b3fe7755 markers at the end of the filter block — kept both sides: has_visible_items alongside format_traceback / model_verbose_name)