from datetime import timedelta


def calculate_free_time(schedule):
    free_slots = []

    for i in range(len(schedule) - 1):
        current_lesson = schedule[i]
        next_lesson = schedule[i + 1]

        gap = next_lesson.end_time - current_lesson.start_time

        if gap > timedelta(minutes=10):
            free_slots.append(gap)

    return free_slots