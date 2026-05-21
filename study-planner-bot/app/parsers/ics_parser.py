from icalendar import Calendar


def parse_ics(file_path: str):
    with open(file_path, "rb") as f:
        calendar = Calendar.from_ical(f.read())

    lessons = []

    for component in calendar.walk():
        if component.name == "VEVENT":
            lessons.append(
                {
                    "subject": str(component.get("summary")),
                    "room": str(component.get("location")),
                    "start": component.get("dtstart").dt,
                    "end": component.get("dtend").dt,
                }
            )

    return lessons