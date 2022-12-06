import datetime as dt

from database_tools.entities import ScheduleView

weekdays = ["понедельник",
            "вторник",
            "среда",
            "четверг",
            "пятница",
            "суббота",
            "воскресенье"]


months = ["января",
          "февраля",
          "марта",
          "апреля",
          "мая",
          "июня",
          "июля",
          "августа",
          "сентября",
          "октября",
          "ноября",
          "декабря"]

parities = ["чёт",
            "нечёт"]


async def get_weekday(date=dt.datetime.today()) -> int:
    return date.weekday()


async def get_parity(date=dt.datetime.today()) -> int:
    return date.isocalendar()[1] % 2


async def stringify_schedule_list(_list: list[ScheduleView], date=dt.datetime.today()) -> str:
    result = f"{date.day} {months[date.month-1]}, {parities[await get_parity(date)]}\. {weekdays[await get_weekday(date)]}\n"
    if len(_list) != 0:
        result += f"{len(_list)} пар\(ы\):\n"
        _list.sort(key=lambda x: x.begin_time)
        for lesson in _list:
            result += f"{lesson.begin_time.strftime('%H:%M')}\-" \
                      f"{lesson.end_time.strftime('%H:%M')} \- *{lesson.discipline}*\n" \
                      f"{lesson.teacher_surname} {lesson.teacher_name} {lesson.teacher_patronymic}\n"
            classroom = "ауд\." + str(lesson.classroom) if lesson.classroom != 0 else "Онлайн"
            result += classroom + "\n\n"
    else:
        result += "Нет пар\."

    return result
