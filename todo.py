from sqlalchemy import create_engine
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task
        
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
rows = session.query(Table).all()

from datetime import datetime, timedelta
today = datetime.today()
import calendar


def to_do():
    while True:
        print('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
        user = int(input())
        if user == 1:
            print(f"Today {today.day} {today.strftime('%b')}:")
            if session.query(Table).filter(Table.deadline == today.date()).all() == []:
                print("Nothing to do!")
            else:
                for i in session.query(Table).filter(Table.deadline == today.date()).all():
                    print(i)
        elif user == 2:
            week = 0
            while week < 7:
                w = today + timedelta(days=week)
                print(f"{calendar.day_name[w.weekday()]} {w.day} {w.strftime('%b')}:")
                if session.query(Table).filter(Table.deadline == w.date()).all() == []:
                    print("Nothing to do!")
                    print()
                else:
                    for i in session.query(Table).filter(Table.deadline == w.date()).all():
                        print(i)
                        print()
                week += 1
        elif user == 3:
            if rows == []:
                print("Nothing to do!")
            else:
                print("All tasks:")
                count = 1
                for j in session.query(Table).order_by(Table.deadline).all():
                    print(f"{count}. {j}. {j.deadline.strftime('%#d %b')}")
                    count += 1
        elif user == 4:
            if session.query(Table).filter(Table.deadline < datetime.today()).all() == []:
                print("Nothing is missed!")
                print()
            else:
                print("Missed tasks:")
                count = 1
                for m in session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all():
                    print(f"{count}. {m}. {m.deadline.strftime('%#d %b')}")
                    count += 1
                print()
        elif user == 5:
            print("Enter task")
            new = input()
            print("Enter deadline")
            do_by = input()
            new_row = Table(task=new,
                            deadline=datetime.strptime(do_by, '%Y-%m-%d').date())
            session.add(new_row)
            session.commit()
            print("The task has been added!")
        elif user == 6:
            print("Choose the number of the task you want to delete:")
            count = 1
            for t in session.query(Table).order_by(Table.deadline).all():
                print(f"{count}. {t}. {t.deadline.strftime('%#d %b')}")
                count += 1
            delete = int(input())
            session.delete(rows[delete-1])
            session.commit()

        elif user == 0:
            print("Bye!")
            break

to_do()
#Base.metadata.drop_all(engine)
