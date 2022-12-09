from data import db_session
from data.channels import Channel


text = """английский -1001643098015
база -1001852082784
инфо -1001756961605
физика -1001886356109
история -1001654213580
обществознание -1001844425642
химия -1001854554723
профиль -1001891713501
литература -1001848540227
русский -1001583931415
биология -1001855161880"""

db_session.global_init("db/ege_bot.db")
db_sess = db_session.create_session()


for i in text.split('\n'):
    splitted = i.split(' ')
    a = Channel()
    a.channel_id = splitted[1]
    a.lesson_title = splitted[0]
    a.month_title = 'октябрь'
    a.school_title = 'умскул'
    db_sess.add(a)
    db_sess.commit()

