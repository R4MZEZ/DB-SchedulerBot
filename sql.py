SELECT_FREE_CLASSROOMS: str = """SELECT НОМЕР as classroom, АДРЕС as campus, ВРЕМЯ_НАЧ as begin_time, ВРЕМЯ_КОН as end_time FROM
                                (SELECT АУДИТОРИИ.НОМЕР, КОД_КОРПУСА, ВРЕМЯ_НАЧ, ВРЕМЯ_КОН
                                FROM АУДИТОРИИ,
                                     АКАДЕМ_ЧАС
                                WHERE АУДИТОРИИ.ИД NOT IN
                                    (SELECT АУД_ИД
                                     FROM РАСПИСАНИЕ
                                     WHERE ЧЕТНОСТЬ = {0}
                                       AND ГРУППА = {1}
                                       AND ДЕНЬ_НЕДЕЛИ = {2})
                                AND АКАДЕМ_ЧАС.ИД NOT IN
                                    (SELECT НОМЕР_ПАРЫ
                                     FROM РАСПИСАНИЕ
                                     WHERE ЧЕТНОСТЬ = {0}
                                       AND ГРУППА = {1}
                                       AND ДЕНЬ_НЕДЕЛИ = {2})
                                  AND КОД_КОРПУСА IN
                                    (SELECT * FROM get_available_campuses({0},{1},{2}))
                                  AND ВМЕСТИМОСТЬ >= {3}
                                  AND АУДИТОРИИ.ИД IN
                                    (SELECT АУД_ИД
                                     FROM ОСНАЩЕНИЕ_АУДИТОРИИ
                                     INNER JOIN ТИПЫ_ОБОРУДОВАНИЯ ON ОБОРУД_ИД = ИД
                                     WHERE НАИМЕНОВАНИЕ = '{4}')
                                ORDER BY АУДИТОРИИ.НОМЕР) AS _INNER
                                INNER JOIN КОРПУСА ON КОД_КОРПУСА=КОРПУСА.ИД;"""

SELECT_FREE_CLASSROOMS_NO_EQ: str = """SELECT АУД_ИД_ as classroom_id, НОМЕР as classroom, АДРЕС as campus, ВРЕМЯ_НАЧ as begin_time, ВРЕМЯ_КОН as end_time FROM
                                (SELECT АУДИТОРИИ.ИД as АУД_ИД_, АУДИТОРИИ.НОМЕР, КОД_КОРПУСА, ВРЕМЯ_НАЧ, ВРЕМЯ_КОН
                                FROM АУДИТОРИИ,
                                     АКАДЕМ_ЧАС
                                WHERE АУДИТОРИИ.ИД NOT IN
                                    (SELECT АУД_ИД
                                     FROM РАСПИСАНИЕ
                                     WHERE ЧЕТНОСТЬ = {0}
                                       AND ГРУППА = {1}
                                       AND ДЕНЬ_НЕДЕЛИ = {2})
                                AND АКАДЕМ_ЧАС.ИД NOT IN
                                    (SELECT НОМЕР_ПАРЫ
                                     FROM РАСПИСАНИЕ
                                     WHERE ЧЕТНОСТЬ = {0}
                                       AND ГРУППА = {1}
                                       AND ДЕНЬ_НЕДЕЛИ = {2})
                                  AND КОД_КОРПУСА IN
                                    (SELECT * FROM get_available_campuses({0},{1},{2}))
                                  AND ВМЕСТИМОСТЬ >= {3}
                                  
                                ORDER BY АУДИТОРИИ.НОМЕР) AS _INNER
                                INNER JOIN КОРПУСА ON КОД_КОРПУСА=КОРПУСА.ИД;"""

SELECT_DISCIPLINE_ID: str = "SELECT ДИСЦИПЛИНЫ.ИД as id FROM УЧИТЕЛЯ INNER JOIN ДИСЦИПЛИНЫ " \
                            "ON КОД_ПРЕДМЕТА = ДИСЦИПЛИНЫ.ИД WHERE ФАМИЛИЯ='{}'"

SELECT_SPECIFIC_CLASSROOM_EQ: str = "SELECT ОБОРУД_ИД FROM ОСНАЩЕНИЕ_АУДИТОРИИ WHERE АУД_ИД = {0}"
