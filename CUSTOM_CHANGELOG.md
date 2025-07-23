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
