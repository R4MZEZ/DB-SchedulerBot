from sqlalchemy import Column, String, BigInteger, Sequence, Integer, ForeignKey, Time, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Building(Base):
    __tablename__ = "КОРПУСА"

    id = Column("ИД", BigInteger, Sequence('corpus_seq'),
                primary_key=True, index=True)
    address = Column("АДРЕС", String)


class Classroom(Base):
    __tablename__ = "АУДИТОРИИ"

    id = Column("ИД", BigInteger, Sequence('audiences_seq'),
                primary_key=True, index=True)
    number = Column("НОМЕР", Integer, nullable=False)
    capacity = Column("ВМЕСТИМОСТЬ", Integer, nullable=False)
    building_code = Column("КОД_КОРПУСА", BigInteger)


class Equipment(Base):
    __tablename__ = "ТИПЫ_ОБОРУДОВАНИЯ"

    id = Column("ИД", BigInteger, Sequence('equipment_type_seq'),
                primary_key=True, index=True)
    name = Column("НАИМЕНОВАНИЕ", String, nullable=False)


class ClassroomEquipment(Base):
    __tablename__ = "ОСНАЩЕНИЕ_АУДИТОРИИ"

    eq_id = Column("ОБОРУД_ИД", ForeignKey("ТИПЫ_ОБОРУДОВАНИЯ.ИД"), primary_key=True)
    class_id = Column("АУД_ИД", ForeignKey("АУДИТОРИИ.ИД"))


class Group(Base):
    __tablename__ = "ГРУППЫ"

    id = Column("ИД", BigInteger, Sequence('group_seq'),
                primary_key=True, index=True)
    code = Column("КОД_ГРУППЫ", String)
    stud_count = Column("КОЛВО_ЛЮДЕЙ", Integer)


class AcademicHour(Base):
    __tablename__ = "АКАДЕМ_ЧАС"

    id = Column("ИД", BigInteger, Sequence('academic_hour_seq'),
                primary_key=True, index=True)
    code = Column(Integer)
    start_time = Column("ВРЕМЯ_НАЧ", Time)
    end_time = Column("ВРЕМЯ_КОН", Time)


class Discipline(Base):
    __tablename__ = "ДИСЦИПЛИНЫ"

    id = Column("ИД", BigInteger, Sequence('disciplines_seq'),
                primary_key=True, index=True)
    name = Column("НАИМЕНОВАНИЕ", String)


class Teacher(Base):
    __tablename__ = "УЧИТЕЛЯ"

    id = Column("ИД", BigInteger, Sequence('teacher_seq'),
                primary_key=True, index=True)
    code = Column("КОД_ПРЕДМЕТА", BigInteger, ForeignKey("ДИСЦИПЛИНЫ.ИД"))
    name = Column("ИМЯ", String)
    surname = Column("ФАМИЛИЯ", String)
    patronymic = Column("ОТЧЕСТВО", String)

    def __repr__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymic[0]}."


class Schedule(Base):
    __tablename__ = "РАСПИСАНИЕ"

    id = Column("ИД", BigInteger, Sequence('timetable_seq'),
                primary_key=True, index=True)
    classroom_id = Column("АУД_ИД", BigInteger, ForeignKey("АУДИТОРИИ.ИД"))
    discipline_id = Column("КОД_ПРЕДМЕТА", BigInteger, ForeignKey("ДИСЦИПЛИНЫ.ИД"))
    teacher_id = Column("УЧ_ИД", BigInteger, ForeignKey("УЧИТЕЛЯ.ИД"))
    group_id = Column("ГРУППА", BigInteger, ForeignKey("ГРУППЫ.ИД"))
    lesson_number = Column("НОМЕР_ПАРЫ", BigInteger, ForeignKey("АКАДЕМ_ЧАС.ИД"))
    weekday = Column("ДЕНЬ_НЕДЕЛИ", Integer)
    parity = Column("ЧЕТНОСТЬ", Integer, default=2)
    date = Column("ДАТА", Date)


class ScheduleView(Base):
    __tablename__ = "schedule_view_"

    id = Column("id", Integer)
    classroom = Column("classroom", String)
    campus = Column("campus", String)
    discipline = Column("discipline", String)
    teacher_name = Column("teacher_name", String)
    teacher_surname = Column("teacher_surname", String)
    teacher_patronymic = Column("teacher_patronymic", String)
    group = Column("group", String)
    begin_time = Column("begin_time", Time)
    end_time = Column("end_time", Time)
    week_day = Column("week_day", Integer)
    parity = Column("parity", Integer, default=2)
    lesson_date = Column("lesson_date", Date, primary_key=True)

    def __repr__(self):
        return str(self.__dict__)
