from datetime import datetime, timedelta

def get_birthdays_per_week(users):
    # определяем начало новой недели/отсчет берем с СБ так как нужно захватить тех у кого был ДН на выходных и поздравить их в ПН
    new_week = datetime.now()+timedelta(days=5-datetime.now().weekday())
    birthday = []
    weekendBirthday =[] #формируем отдельный список тех у кого ДН на выходных
    n=0
    while n <7:
        delta = timedelta(days=n)
        week = new_week + delta

        for el in users:
            if users[el].month == week.month and users[el].day == week.day:
                if week.weekday()==5 or week.weekday() ==6: #если день недели сб или вс добавляет в отдельный список Дн выходного дня
                    weekendBirthday.append(el)
                else:
                    birthday.append(el)

        if len(birthday)==0 or len(birthday)>0:
            if len(birthday)>0 and week.strftime('%A')=="Monday" and len(weekendBirthday)>0:
                print("{:<8} : {}, {}".format(week.strftime('%A'),', '.join(weekendBirthday), ', '.join(birthday)))
            elif week.strftime('%A')=="Monday" and len(weekendBirthday)>0:
                print("{:<8} : {}".format(week.strftime('%A'), ', '.join(weekendBirthday)))
            elif len(birthday)>0:
                print("{:<8} : {}".format(week.strftime('%A'), ', '.join(birthday)))

        birthday.clear()
        n += 1


#тестовый список
users = {
    "Roma" : datetime(year=1998, month=2, day=5),
    "Jack" : datetime(year=1999, month=2, day=6),
    "Bill": datetime(year=2000, month=2, day=2),
    "Nastya": datetime(year=2005, month=3, day=8),
    "Lil": datetime(year=1998, month=2, day=8),
    "Vasya": datetime(year=1998, month=2, day=10),
    "Haio": datetime(year=1998, month=2, day=11),
    "Operato": datetime(year=1998, month=3, day=3)
}


get_birthdays_per_week(users)