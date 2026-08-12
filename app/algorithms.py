import heapq
from datetime import date


def choose_next_task(tasks):
    heap = []

    for task in tasks:
        if task["completed"]:
            continue

        priority_value = -task["priority"]

        if task["due_date"]:
            due_date_value = date.fromisoformat(
                str(task["due_date"])
            ).toordinal()
        else:
            due_date_value = date.max.toordinal()

        heapq.heappush(
            heap,
            (
                priority_value,
                due_date_value,
                task["id"],
                task,
            ),
        )

    if not heap:
        return None

    next_task = heapq.heappop(heap)

    return next_task[3]