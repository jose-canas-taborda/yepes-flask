class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flasksdv'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/flasksdv'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://admin:DDigit3st@database-1.cel5wjgrlt3s.us-east-1.rds.amazonaws.com/database-1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'production' : ProductionConfig
}