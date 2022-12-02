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

    eq_id = Column("ОБОРУД_ИД", ForeignKey("ТИПЫ_ОБОРУДОВАНИЯ.ИД"))
    class_id = Column("АУД_ИД", ForeignKey("АУДИТОРИИ.ИД"))


class Group(Base):
    __tablename__ = "ГРУППЫ"

    id = Column("ИД", BigInteger, Sequence('group_seq'),
                primary_key=True, index=True)
    code = Column(String)
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
    surname = Column("ИМЯ", String)
    patronymic = Column("ОТЧЕСТВО", String)


class Schedule(Base):
    __tablename__ = "РАСПИСАНИЕ"

    id = Column("ИД", BigInteger, Sequence('timetable_seq'),
                primary_key=True, index=True)
    classroom_id = Column("АУД_ИД", BigInteger, ForeignKey("АУДИТОРИИ.ИД"))
    discipline_id = Column("КОД_ПРЕДМЕТА", BigInteger, ForeignKey("ДИСЦИПЛИНЫ.ИД"))
    group_id = Column("УЧ_ИД", BigInteger, ForeignKey("УЧИТЕЛЯ.ИД"))
    lesson_number = Column("НОМЕР_ПАРЫ", BigInteger, ForeignKey("АКАДЕМ_ЧАС.ИД"))
    weekday = Column("ДЕНЬ_НЕДЕЛИ", Integer)
    parity = Column("ЧЕТНОСТЬ", Integer, default=2)
    date = Column("ДАТА", Date)
