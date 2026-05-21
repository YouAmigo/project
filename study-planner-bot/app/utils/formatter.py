def format_schedule(schedule):
    lines = []

    for lesson in schedule:
        lines.append(
            f"{lesson.start_time} - {lesson.end_time} | "
            f"{lesson.subject} | {lesson.room}"
        )

    return "\n".join(lines)