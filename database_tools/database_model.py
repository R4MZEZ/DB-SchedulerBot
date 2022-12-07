import datetime

from sqlalchemy import create_engine, select, and_, or_
from sqlalchemy.orm import sessionmaker

from database_tools.entities import Group, Teacher, ScheduleView, Equipment, Schedule, Classroom, AcademicHour
from sql import SELECT_FREE_CLASSROOMS, SELECT_DISCIPLINE_ID
from tools import get_weekday, get_parity


class DBConnection(object):
    def __init__(self, access_url):
        self.url = access_url
        self.engine = create_engine(access_url)
        self.Session = sessionmaker(autoflush=False, bind=self.engine)
        self.database = self.Session()
        self.connect = self.engine.connect()

    async def get_groups(self):
        return set(map(lambda x: x.code, self.database.query(Group).all()))

    async def get_group_id(self, group: str):
        return self.database.query(Group.id).filter(Group.code == group).first()[0]

    async def group_exists(self, code):
        return code in list(map(lambda x: x.code, self.database.query(Group).all()))

    async def get_teachers(self):
        return set(self.database.query(Teacher).all())

    async def teacher_exists(self, name: str):
        return name.split()[0] in set(map(lambda x: x.surname, self.database.query(Teacher).all()))

    async def get_eq(self):
        return set(map(lambda x: x.name, self.database.query(Equipment).all()))

    async def eq_exists(self, eq: str):
        return eq in set(map(lambda x: x.name, self.database.query(Equipment).all()))

    async def teacher_id_by_name(self, name: str):
        res = self.connect.execute(
            "SELECT ИД as id FROM УЧИТЕЛЯ WHERE ФАМИЛИЯ='{}'".format(name.split()[0]))
        value = res.first().id
        return value

    async def discipline_by_teacher(self, name: str):
        res = self.connect.execute(SELECT_DISCIPLINE_ID.format(name.split()[0]))
        value = res.first().id
        return value

    async def classroom_id(self, classroom_code):
        return self.database.query(Classroom.id).filter(Classroom.number == classroom_code).first()[0]

    async def lesson_number_by_begin_time(self, begin_time):
        return self.database.query(AcademicHour.id).filter(AcademicHour.start_time == begin_time).first()[0]

    async def get_schedule_by_date(self, param: str, is_stud: bool,
                                   date=datetime.datetime.today()) -> list[ScheduleView]:
        weekday = await get_weekday(date) + 1
        parity = await get_parity(date) + 1
        result = select("*").select_from(ScheduleView)
        if is_stud:
            result = result.where(ScheduleView.group.like(param))
        else:
            result = result.where(ScheduleView.teacher_surname.like(param))

        result = result.where(or_(and_(ScheduleView.weekday == weekday, ScheduleView.parity == parity),
                                  ScheduleView.lesson_date == date.strftime("%Y-%m-%d")))

        return list[ScheduleView](self.connect.execute(result).all())

    async def get_teacher_schedule_by_date(self, teacher_name: str,
                                           date=datetime.datetime.today()) -> list[ScheduleView]:
        return await self.get_schedule_by_date(teacher_name, False, date)

    async def get_stud_schedule_by_date(self, group: str,
                                        date=datetime.datetime.today()) -> list[ScheduleView]:
        return await self.get_schedule_by_date(group, True, date)

    async def get_group_stud_count(self, group: str):
        return self.database.query(Group.stud_count).filter(Group.code == group).first()[0]

    async def get_free_classrooms(self, group: str, eq: str, date):
        parity = await get_parity(date) + 1
        weekday = await get_weekday(date) + 1
        capacity = await self.get_group_stud_count(group)
        group = await self.get_group_id(group)
        stmt = SELECT_FREE_CLASSROOMS.format(parity, group, weekday, capacity, eq)
        res = self.connect.execute(stmt)
        value = res.all()
        return value

    async def add_lesson(self, teacher, date, location, group):
        new_schedule = Schedule()
        new_schedule.teacher_id = await self.teacher_id_by_name(teacher.split()[0])
        new_schedule.parity = await get_parity(date) + 1
        new_schedule.weekday = await get_weekday(date) + 1
        new_schedule.group_id = await self.get_group_id(group)
        new_schedule.discipline_id = await self.discipline_by_teacher(teacher)
        new_schedule.classroom_id = await self.classroom_id(location.classroom)
        new_schedule.lesson_number = await self.lesson_number_by_begin_time(location.begin_time)
        self.database.add(new_schedule)
        self.database.commit()
