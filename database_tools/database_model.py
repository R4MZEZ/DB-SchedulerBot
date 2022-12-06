from typing import List

from sqlalchemy import create_engine, select
from sqlalchemy.engine import Row
from sqlalchemy.orm import sessionmaker

from database_tools.entities import Group, Teacher, ScheduleView


class DBConnection(object):
    def __init__(self, access_url):
        self.url = access_url
        self.engine = create_engine(access_url)
        self.Session = sessionmaker(autoflush=False, bind=self.engine)
        self.database = self.Session()
        self.connect = self.engine.connect()

    async def get_groups(self):
        return set(map(lambda x: x.code, self.database.query(Group).all()))

    async def group_exists(self, code):
        return code in list(map(lambda x: x.code, self.database.query(Group).all()))

    async def get_teachers(self):
        return set(self.database.query(Teacher).all())

    async def teacher_exists(self, name: str):
        return name.split()[0] in set(map(lambda x: x.surname, self.database.query(Teacher).all()))

    async def teacher_id_by_name(self, name: str):
        res = self.connect.execute(
            "SELECT ИД as id FROM УЧИТЕЛЯ WHERE ФАМИЛИЯ='{}'".format(name.split(' ')[0]))
        value = res.first().id
        return value

    async def get_schedule(self, group: str) -> list[ScheduleView]:
        stmt = select("*").select_from(ScheduleView).where(ScheduleView.group.like(group))
        return list[ScheduleView](self.connect.execute(stmt).all())

    async def get_schedule_by_weekday(self, group: str, weekday: int, parity: int) -> list[ScheduleView]:
        stmt = select("*").select_from(ScheduleView).where(ScheduleView.group.like(group)).where(
            ScheduleView.weekday == weekday).where(ScheduleView.parity == parity)

        return list[ScheduleView](self.connect.execute(stmt).all())
