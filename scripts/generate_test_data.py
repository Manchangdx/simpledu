import json
from random import randint
from faker import Faker

from simpledu.models import db, User, Course, Chapter
from manage import app


app.app_context().push()

fake = Faker('zh-cn')


def iter_users():

    yield User(
        username='Jack',
        email='jack@example.com',
        password='shiyanlou',
        job='研发小能手'
    )


def iter_courses():

    author = User.query.filter_by(username='Jack').first()

    with open('scripts/courses.json') as f:
        courses = json.load(f)

    for course in courses:
        yield Course(
            name=course['name'],
            description=course['description'],
            image_url=course['image_url'],
            author=author
        )


def iter_chapters():

    for course in Course.query.all():
        for _ in range(randint(3, 10)):
            yield Chapter(
                name=fake.sentence(),
                course=course,
                video_url='https://labfile.oss.aliyuncs.com/courses/923/week2_mp4/2-1-1-mac.mp4',
                video_duration='{}:{}'.format(randint(10, 30), randint(10, 59))
            )


def run():

    for user in iter_users():
        db.session.add(user)

    for course in iter_courses():
        db.session.add(course)

    for chapter in iter_chapters():
        db.session.add(chapter)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


run()
