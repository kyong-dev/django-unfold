![screenshot](https://github.com/user-attachments/assets/b5ec09b6-c8c7-454a-85af-1bba97593632)

## Unfold Django Admin Theme Customized Version

[![PyPI - Version](https://img.shields.io/pypi/v/django-unfold.svg?style=for-the-badge)](https://pypi.org/project/django-unfold-patrick/)
[![Build](https://img.shields.io/github/actions/workflow/status/unfoldadmin/django-unfold/release.yml?style=for-the-badge)](https://github.com/unfoldadmin/django-unfold/actions?query=workflow%3Arelease)
![Pre Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge)
![Code Style - Ruff](https://img.shields.io/badge/code%20style-ruff-30173D.svg?style=for-the-badge)

Unfold is a theme for Django admin that incorporates common best practices for building full-fledged admin areas. It is designed to work on top of the default administration provided by Django. However this package is little customized by [@kyong-dev](https://github.com/kyong-dev/django-unfold). As Unfold gets updated, this package will also be updated accordingly.

- **Documentation:** Full docs are available at [unfoldadmin.com](https://unfoldadmin.com).
- **Unfold:** Demo site is available at [unfoldadmin.com](https://unfoldadmin.com).
- **Formula:** Repository with demo implementation at [github.com/unfoldadmin/formula](https://github.com/unfoldadmin/formula).
- **Turbo:** Django & Next.js boilerplate implementing Unfold at [github.com/unfoldadmin/turbo](https://github.com/unfoldadmin/turbo).
- **Discord:** Join the Unfold community on [Discord](https://discord.gg/9sQj9MEbNz).



## Are you using Unfold and need help?

Have you decided to start using Unfold but don’t have time to make the switch from the native Django admin? [Get in touch with us](https://unfoldadmin.com/consulting?utm_medium=github&utm_source=unfold) and let’s supercharge your development with our expertise.

## Fully Customized Support
If you’re based in Korea or need support in Korean, feel free to reach out to me personally. I’ll be happy to assist you and ensure you get the help you need. Don’t hesitate to get in touch! 


## Installation

```bash
pip install django-unfold-patrick
```

your_project/settings.py
```python

INSTALLED_APPS = [
    ...
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    ...
]
```

## Features

- **Visual**: Provides a new user interface based on the Tailwind CSS framework.
- **Sidebar:** Simplifies the creation of sidebar navigation with icons, collapsibles, and more.
- **Dark mode:** Supports both light and dark mode versions.
- **Actions:** Offers multiple ways to define actions within different parts of the admin interface.
- **Filters:** Custom dropdowns, numeric, datetime, and text fields.
- **Dashboard:** Includes helpers for creating custom dashboard pages.
- **Components:** Reusable UI components such as cards, buttons, and charts.
- **WYSIWYG widget:** Built-in support for WYSIWYG (Trix).
- **Array widget:** Built-in widget for `django.contrib.postgres.fields.ArrayField`.
- **Inline tabs:** Groups inlines into tab navigation in the change form.
- **Model tabs:** Allows defining custom tab navigation for models.
- **Fieldset tabs:** Merges multiple fieldsets into tabs in the change form.
- **Sortable inlines:** Allows sorting inlines by dragging and dropping.
- **Environment label**: Distinguishes between environments by displaying a label.
- **Nonrelated inlines**: Displays nonrelated models as inlines in the change form.
- **Favicons**: Built-in support for configuring various site favicons.
- **Colors:** Allows customization of the default color scheme.
- **Changeform modes:** Displays fields in compressed mode in the change form.
- **Parallel admin**: Supports [running the default admin](https://unfoldadmin.com/blog/migrating-django-admin-unfold/?utm_medium=github&utm_source=unfold) alongside Unfold.
- **Third party packages:** Default support for multiple popular applications.
- **Configuration:** Most basic options can be changed in `settings.py`.
- **Dependencies:** Fully based on `django.contrib.admin`.
- **VS Code**: Project configuration and development container included.

## Customized Features

- **Django_admin_log**: 


## PyPi

change detail in pyproject.toml

```bash
virtualenv venv
source venv/bin/activate

pip install setuptools wheel twine build
```

```bash
git fetch

python -m build  
twine upload dist/*
```