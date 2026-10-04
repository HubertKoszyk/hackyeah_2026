from django.contrib import admin, messages
from .models import RoadRestriction
from .services import find_conflicts


@admin.register(RoadRestriction)
class RoadRestrictionAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "organization", "start_at", "end_at", "status", "conflict_count")
    list_filter = ("type", "organization")
    search_fields = ("title", "organization")

    @admin.display(description="Konflikty")
    def conflict_count(self, obj):
        return len(find_conflicts(obj))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        conflicts = find_conflicts(obj)
        if conflicts:
            names = ", ".join(c.title for c in conflicts)
            self.message_user(request, f"UWAGA - kolizja z: {names}", level=messages.WARNING)
