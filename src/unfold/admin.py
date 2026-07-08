from functools import update_wrapper
from typing import Any, TypedDict

from django import forms
from django.contrib.admin import ModelAdmin as BaseModelAdmin
from django.contrib.admin import StackedInline as BaseStackedInline
from django.contrib.admin import TabularInline as BaseTabularInline
from django.contrib.admin import display, helpers
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.contenttypes.admin import (
    GenericStackedInline as BaseGenericStackedInline,
)
from django.contrib.contenttypes.admin import (
    GenericTabularInline as BaseGenericTabularInline,
)
from django.db.models import BLANK_CHOICE_DASH, Model
from django.http import HttpRequest, HttpResponse
from django.urls import URLPattern, path
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _
from django.views import View

from unfold.checks import UnfoldModelAdminChecks
from unfold.forms import (
    ActionForm,
    PaginationGenericInlineFormSet,
    PaginationInlineFormSet,
)
from unfold.mixins import (
    ActionModelAdminMixin,
    DatasetModelAdminMixin,
    FormFieldModelAdminMixin,
    NestedInlinesModelAdminMixin,
)
from unfold.overrides import FORMFIELD_OVERRIDES_INLINE
from unfold.views import ChangeList
from unfold.widgets import UnfoldBooleanWidget

checkbox = UnfoldBooleanWidget(
    {
        "class": "action-select",
        "aria-label": _("Select record"),
    },
    lambda value: False,
)


class ListFilterOptionsItem(TypedDict):
    label: str | None
    horizontal: bool | None


class ModelAdmin(
    FormFieldModelAdminMixin,
    ActionModelAdminMixin,
    DatasetModelAdminMixin,
    NestedInlinesModelAdminMixin,
    BaseModelAdmin,
):
    action_form = ActionForm
    custom_urls = ()
    add_fieldsets = ()
    ordering_field = None
    hide_ordering_field = False
    list_horizontal_scrollbar_top = False
    list_filter_submit = False
    list_filter_sheet = True
    list_filter_options: dict[str, ListFilterOptionsItem] = {}
    list_fullwidth = False
    list_disable_select_all = False
    list_before_template = None
    list_after_template = None
    change_form_before_template = None
    change_form_after_template = None
    change_form_outer_before_template = None
    change_form_outer_after_template = None
    compressed_fields = True
    show_add_link = True
    readonly_preprocess_fields = {}
    warn_unsaved_form = False
    checks_class = UnfoldModelAdminChecks

    @property
    def media(self):
        media = super().media

        if hasattr(self, "nested_formset_media"):
            media += self.nested_formset_media

        if not hasattr(self, "request"):
            return media

        for filter in self.get_list_filter(self.request):
            if (
                isinstance(filter, tuple | list)
                and hasattr(filter[1], "form_class")
                and hasattr(filter[1].form_class, "Media")
            ):
                media += forms.Media(filter[1].form_class.Media)
            elif hasattr(filter, "form_class") and hasattr(filter.form_class, "Media"):
                media += forms.Media(filter.form_class.Media)

        return media

    def changelist_view(
        self, request: HttpRequest, extra_context: dict[str, str] | None = None
    ) -> HttpResponse:
        self.request = request

        if self.ordering_field and self.ordering_field not in self.list_editable:
            list_editable = list(getattr(self, "list_editable", []))
            list_editable.append(self.ordering_field)
            self.list_editable = list_editable

        return super().changelist_view(request, extra_context)

    def changeform_view(
        self,
        request: HttpRequest,
        object_id: str | None = None,
        form_url: str = "",
        extra_context: dict[str, Any] | None = None,
    ) -> Any:
        from unfold.forms import AdminForm, Fieldline

        helpers.AdminForm = AdminForm  # ty:ignore
        helpers.Fieldline = Fieldline  # ty:ignore

        response = super().changeform_view(request, object_id, form_url, extra_context)

        if self._show_ui_warnings(request):
            self._display_autocomplete_fields_warnings(request)

        return response

    def get_list_display(self, request: HttpRequest) -> list | tuple:
        list_display = super().get_list_display(request)

        if self.ordering_field and self.ordering_field not in list_display:
            if isinstance(list_display, tuple):
                list_display = (*list_display, self.ordering_field)
            elif isinstance(list_display, list):
                list_display.append(self.ordering_field)

        return list_display

    def get_fieldsets(
        self, request: HttpRequest, obj: Model | None = None
    ) -> list | tuple:
        if not obj and self.add_fieldsets:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def getLogMessage(self, form, add=False, formsetObj=None):
        """
        Return a list of messages describing the changes from the admin form.
        """
        changed_data = {} if form is None else form.changed_data
        data = {}
        change_message = []

        if formsetObj is not None:
            data = {
                "name": str(formsetObj._meta.verbose_name_plural),
                "object": f"{str(formsetObj)}({formsetObj.pk})",
            }
        if add:
            change_message.append({"added": data})
        elif form.changed_data:
            message = []
            for field in changed_data:
                initial = form.initial[field]
                cleaned_data = form.cleaned_data[field]

                message.append(
                    f"""[{form.fields[field].label}] "{str(initial)}" => "{str(cleaned_data)}" """
                )
            data["fields"] = message
            change_message.append({"changed": data})
        return change_message

    def construct_change_message(self, request, form, formsets, add=False):
        """
        Construct a JSON structure describing change details from a changed object and append it to change_messge in django_admin_log.
        """
        change_message = self.getLogMessage(form, add)

        if formsets:
            for formset in formsets:
                formList = {}

                pkName = ""
                if formset.__len__() > 0:
                    pkName = formset.forms[0]._meta.model._meta.pk.name

                for singleform in formset.forms:
                    try:
                        obj = singleform.cleaned_data[pkName]

                        if obj is None:
                            obj = singleform.initial.get(pkName)

                        if obj is not None:
                            formList[getattr(obj, pkName)] = singleform
                    except Exception as e:
                        print(e)

                for added_object in formset.new_objects:
                    message = self.getLogMessage(None, True, formsetObj=added_object)
                    change_message += message

                for changed_object, changed_fields in formset.changed_objects:
                    singleForm = formList[changed_object.pk]
                    message = self.getLogMessage(
                        singleForm, False, formsetObj=changed_object
                    )
                    change_message += message

                    self.log_change(
                        request, changed_object, self.getLogMessage(singleForm, False)
                    )

                for deleted_object in formset.deleted_objects:
                    change_message.append(
                        {
                            "deleted": {
                                "name": str(deleted_object._meta.verbose_name_plural),
                                "object": str(deleted_object),
                            }
                        }
                    )
        return change_message

    def get_custom_urls(self) -> tuple[tuple[str, str, View], ...]:
        """
        Method to get custom views for ModelAdmin with their urls

        Format of custom_urls item:
            ("path_to_view", "name_of_view", view_itself)
        """
        return () if self.custom_urls is None else self.custom_urls

    def get_urls(self) -> list[URLPattern]:
        urls = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        custom_urls = [
            self._path_from_custom_url(custom_url)
            for custom_url in self.get_custom_urls()
        ]

        actions_list_urls = [
            path(
                f"{action.path.removesuffix('/')}/",
                wrap(action.method),
                name=action.action_name,
            )
            for action in self._get_base_actions_list()
        ]

        action_detail_urls = [
            path(
                f"<path:object_id>/{action.path.removesuffix('/')}/",
                wrap(action.method),
                name=action.action_name,
            )
            for action in self._get_base_actions_detail()
        ]

        action_row_urls = [
            path(
                f"<path:object_id>/{action.path.removesuffix('/')}/",
                wrap(action.method),
                name=action.action_name,
            )
            for action in self._get_base_actions_row()
        ]

        return (
            custom_urls
            + action_row_urls
            + actions_list_urls
            + action_detail_urls
            + urls
        )

    def _path_from_custom_url(self, custom_url: tuple[str, str, View]) -> URLPattern:
        return path(
            custom_url[0],
            self.admin_site.admin_view(custom_url[2]),
            {"model_admin": self},
            name=custom_url[1],
        )

    def get_action_choices(
        self,
        request: HttpRequest,
        default_choices: list[tuple[str, str]] = BLANK_CHOICE_DASH,
    ) -> list[tuple[str, str]]:
        default_choices = [("", _("Select action"))]
        return super().get_action_choices(request, default_choices)

    @display(description=mark_safe(checkbox.render("action_toggle_all", 1)))
    def action_checkbox(self, obj: Model) -> SafeString:
        return checkbox.render(helpers.ACTION_CHECKBOX_NAME, str(obj.pk))

    def get_changelist(self, request: HttpRequest, **kwargs: Any) -> type[ChangeList]:
        return ChangeList

    def get_formset_kwargs(
        self, request: HttpRequest, obj: Model, inline: InlineModelAdmin, prefix: str
    ) -> dict[str, Any]:
        formset_kwargs = super().get_formset_kwargs(request, obj, inline, prefix)

        if hasattr(inline, "per_page") and inline.per_page:
            formset_kwargs["request"] = request
            formset_kwargs["per_page"] = inline.per_page

        if hasattr(inline, "show_count") and inline.show_count:
            if hasattr(inline, "get_count") and callable(inline.get_count):
                formset_kwargs["count"] = inline.get_count(request, obj)

            if hasattr(inline, "get_count_variant") and callable(
                inline.get_count_variant
            ):
                formset_kwargs["count_variant"] = inline.get_count_variant(request, obj)

        return formset_kwargs


class BaseInlineMixin:
    formfield_overrides = FORMFIELD_OVERRIDES_INLINE
    readonly_preprocess_fields = {}
    ordering_field = None
    per_page = None
    hide_ordering_field = False
    collapsible = False
    show_count = False
    hide_title = False
    tab = False


class TabularInline(BaseInlineMixin, FormFieldModelAdminMixin, BaseTabularInline):
    formset = PaginationInlineFormSet


class StackedInline(BaseInlineMixin, FormFieldModelAdminMixin, BaseStackedInline):
    formset = PaginationInlineFormSet


class GenericStackedInline(
    BaseInlineMixin, FormFieldModelAdminMixin, BaseGenericStackedInline
):
    formset = PaginationGenericInlineFormSet


class GenericTabularInline(
    BaseInlineMixin, FormFieldModelAdminMixin, BaseGenericTabularInline
):
    formset = PaginationGenericInlineFormSet
