from django.contrib import admin
from .models import User, Team, Family

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "profile_id",
        "first_name",
        "last_name",
        "email_address",
        "parent_email_address",
        "family",
        "team",
    )
    list_filter = ("family", "team")

    def team(self, obj):
        return obj.team.team_name if obj.team else None

    def family(self, obj):
        return obj.family.family_name if obj.family else None


class TeamAdmin(admin.ModelAdmin):
    # list team name and all users in the team
    list_display = ("team_name", "users")

    def users(self, obj):
        return "\n".join(
            [
                f"{u.first_name} {u.last_name},"
                if index == 0 and obj.team_members.count() > 1
                else f"{u.first_name} {u.last_name}"
                for index, u in enumerate(obj.team_members.all())
            ]
        )


class FamilyAdmin(admin.ModelAdmin):
    # list family name and all users in the family
    list_display = ("family_name", "users")

    def users(self, obj):
        return "\n".join(
            [
                f"{u.first_name} {u.last_name},"
                if index == 0 and obj.family_members.count() > 1
                else f"{u.first_name} {u.last_name}"
                for index, u in enumerate(obj.family_members.all())
            ]
        )


admin.site.register(Team, TeamAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(User, UserAdmin)
