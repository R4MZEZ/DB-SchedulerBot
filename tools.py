import datetime as dt

from aiogram import types

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


async def stringify_lesson(lesson: ScheduleView, for_teacher: bool) -> str:
    if for_teacher:
        lesson_str = f"{parities[lesson.parity - 1]}\. {weekdays[lesson.week_day - 1]}\n"
    else:
        lesson_str = ""

    lesson_str += f"{lesson.begin_time.strftime('%H:%M')}\-" \
                 f"{lesson.end_time.strftime('%H:%M')} \- *{lesson.discipline}*\n"
    if for_teacher:
        lesson_str += f"гр\. {lesson.group}\n"
    else:
        lesson_str += f"{lesson.teacher_surname} {lesson.teacher_name} {lesson.teacher_patronymic}\n"
    classroom = f"ауд\. {str(lesson.classroom)}, {lesson.campus}" if lesson.classroom != 0 else "Онлайн"
    lesson_str += classroom + "\n\n"
    return lesson_str


async def stringify_daily_schedule_list(_list: list[ScheduleView], date=dt.datetime.today()) -> str:
    result = f"{date.day} {months[date.month - 1]}, {parities[await get_parity(date)]}\. {weekdays[await get_weekday(date)]}\n"
    if len(_list) != 0:
        result += f"{len(_list)} пар\(ы\):\n"
        _list.sort(key=lambda x: x.begin_time)

        for lesson in _list:
            result += await stringify_lesson(lesson, False)
    else:
        result += "Нет пар\."

    return result


async def stringify_schedule_list(_list: list[ScheduleView]) -> str:
    if len(_list) != 0:
        result = f"У вас {len(_list)} занятия\(ий\) в расписании:\n"
        _list.sort(key=lambda x: x.week_day)
        for lesson in _list:
            result += f"{_list.index(lesson)}\. "
            result += await stringify_lesson(lesson, True)
    else:
        result = "У вас нет занятий в расписании."

    return result


async def stringify_raw_list(_list: list) -> str:
    result = ""
    if len(_list) != 0:
        result += f"{len(_list)} доступных вариантов\(а\):\n"
        _list.sort(key=lambda x: x.begin_time)

        count = 0
        for option in _list:
            result += f"{count}\. {option.begin_time.strftime('%H:%M')}\-" \
                      f"{option.end_time.strftime('%H:%M')} \- "
            classroom = f"*ауд\. {str(option.classroom)}*, {option.campus}" if option.classroom != 0 else "Онлайн"
            result += classroom + "\n"
            count += 1
    else:
        result += "Нет доступных вариантов на этот день\."

    return result


async def get_datetime_from_callback(callback_query: types.CallbackQuery):
    day, month, parity, weekday = callback_query.message.text.split()[:4]
    month = months.index(month[:-1]) + 1
    parity = parities.index(parity[:-1])
    weekday = weekdays.index(weekday)

    year = dt.date.today().year
    month = month if month >= 10 else "0" + str(month)
    day = day if len(day) == 2 else "0" + str(day)
    date = dt.date.fromisoformat(str(year) + "-" + str(month) + "-" + str(day))

    if callback_query.data[:4] == "next":
        date += dt.timedelta(days=1)
        if weekday == 6:
            weekday = 0
            parity = not parity
        else:
            weekday += 1
    else:
        date += dt.timedelta(days=-1)
        if weekday == 0:
            weekday = 6
            parity = not parity
        else:
            weekday -= 1

    weekday += 1  # because in bd they are 1-7
    parity += 1  # same because 1-2 in bd

    return date
