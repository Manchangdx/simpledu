import os, json, faker
from random import randint
from simpledu.models import *
'''
如果要在上一层目录中使用 python3 -m scripts.generate 直接运行文件生成数据，添加以下两行代码即可
'''
from manage import app
app.app_context().push()

fake = faker.Faker('zh-cn')

def iter_users():
    yield User(
        name = 'Kobe',
        email = 'kobe@qq.com',
        password = 'shiyanlou',
        job = '前 NBA 超级巨星'
    )

def iter_courses():
    author = User.query.filter_by(name='Jack Lee').first()
    with open(os.path.join(os.getcwd(), 'scripts/courses.json')) as f:
        courses = json.load(f)
    for course in courses:
        yield Course(
            name=course['name'],
            description=course['description'],
            image_url=course['image_url'],
            author=author
        )

def iter_chapters():
    for course in Course.query:
        for i in range(randint(3, 10)):
            yield Chapter(
                name=fake.sentence(),
                course=course,
                video_url='https://labfile.oss.aliyuncs.com/courses/923/week2_mp4/2-1-1-mac.mp4',
                video_duration='{}:{}'.format(randint(10, 30), randint(10, 59))
            )


def run():
    try:
        for user in iter_users():
            db.session.add(user)
            db.session.commit()

        for course in iter_courses():
            db.session.add(course)
            db.session.commit()

        for chapter in iter_chapters():
            db.session.add(chapter)
            db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

if __name__ == '__main__':
    run()
