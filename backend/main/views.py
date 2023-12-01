from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import tempfile
import pandas as pd
from .models import User, Team, Family


def parse_spreadsheet(spreadsheet):
    new = 0
    existing = 0
    errors = 0
    new_users = []
    existing_users = []
    error_rows = []
    spreadsheet = spreadsheet.fillna("")

    for index, row in spreadsheet.iterrows():
        team = None
        family = None

        try:
            user, created_user = User.objects.get_or_create(
                profile_id=row["Profile id"],
                first_name=row["Firstname"],
                last_name=row["Lastname"],
                email_address=row["Email"],
                parent_email_address=row["Parent/Guardian Email"],
            )

        except Exception as e:
            errors += 1
            error_rows.append(f"Row {index + 2}")
            continue

        if row["Teamname"]:
            team, _ = Team.objects.get_or_create(team_name=row["Teamname"])

        family_member = (
            User.objects.filter(email_address=row["Email"])
            .exclude(profile_id=user.profile_id)
            .first()
        )

        if family_member:
            family = family_member.family
            if not family:
                family, _ = Family.objects.get_or_create(family_name=row["Lastname"])
                family_member.family = family
                family_member.save()

        user.team = team
        user.family = family
        user.save()

        if not created_user:
            existing += 1
            existing_users.append(f"{user.first_name} {user.last_name}")

        else:
            new += 1
            new_users.append(f"{user.first_name} {user.last_name}")
            user.save()

    return new, existing, errors, new_users, existing_users, error_rows


def check_columns(df):
    return set(
        ["Profile id", "Firstname", "Lastname", "Email", "Parent/Guardian Email"]
    ).difference(df.columns)


# Create your views here.
def index(request):
    return JsonResponse({"message": "Good"})


@csrf_exempt
def process_csv(request):
    body = request.body

    if not request.method == "POST":
        return JsonResponse({"message": "Invalid request method."})

    if request.FILES.get("spreadsheet") is None:
        return JsonResponse({"message": "Could not find spreadsheet in request."})

    spreadsheet = request.FILES["spreadsheet"]
    if not spreadsheet.name.endswith(".xlsx"):
        return JsonResponse({"message": "Invalid file type."})

    # parse the spreadsheet
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
            tmp_file.write(request.body)
            tmp_file.seek(0)  # Go back to the beginning of the file

            # Now you can read the file using Pandas
            df = pd.read_excel(tmp_file.name, engine="openpyxl")

            missing_cols = check_columns(df)
            if missing_cols:
                return JsonResponse({"message": f"Missing columns: {missing_cols}"})

            # Process the DataFrame 'df' as needed
            (
                new,
                existing,
                errors,
                new_users,
                existing_users,
                error_rows,
            ) = parse_spreadsheet(df)

        print(f"New {new}, Existing {existing}, Existing users: {existing_users}")
        return JsonResponse(
            {
                "data": {
                    "new": new,
                    "existing": existing,
                    "errors": errors,
                    "new_users": new_users,
                    "existing_users": existing_users,
                    "error_rows": error_rows,
                }
            }
        )
    except Exception as e:
        return JsonResponse({"message": f"Error processing file: {e}"})
