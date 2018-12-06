class BaseConfig:
    INDEX_PER_PAGE = 6
    ADMIN_PER_PAGE = 5
    SECRET_KEY = 'haha'

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/simpledu?charset=utf8'

class TestingConfig(BaseConfig):
    pass


configs = dict(
    dev = DevelopmentConfig,
    test = TestingConfig
)
