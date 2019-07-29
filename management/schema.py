import sqlalchemy

metadata = sqlalchemy.MetaData()

templates = sqlalchemy.Table(
    'templates',
    metadata,
    sqlalchemy.Column('name', sqlalchemy.CHAR(length=70), primary_key=True),
    sqlalchemy.Column('activeVersion', sqlalchemy.INT(), server_default=sqlalchemy.text('1')),

    sqlalchemy.Column('t_createdAt', sqlalchemy.TIMESTAMP(), server_default=sqlalchemy.text('NOW()'), nullable=False),
    sqlalchemy.Column('t_updatedAt', sqlalchemy.TIMESTAMP(), server_default=sqlalchemy.text('NOW()'), nullable=False),
    sqlalchemy.Column('t_deletedAt', sqlalchemy.TIMESTAMP()),

    sqlalchemy.Column('t_createdBy', sqlalchemy.CHAR(length=30), nullable=False),
    sqlalchemy.Column('t_updatedBy', sqlalchemy.CHAR(length=30), nullable=False),
    sqlalchemy.Column('t_deletedBy', sqlalchemy.CHAR(length=30))
)

versions = sqlalchemy.Table(
    'versions',
    metadata,
    sqlalchemy.Column('number', sqlalchemy.INT(), primary_key=True),
    sqlalchemy.Column('templateName', sqlalchemy.ForeignKey("templates.name"), primary_key=True),

    sqlalchemy.Column('subject', sqlalchemy.TEXT(), nullable=False),
    sqlalchemy.Column('body', sqlalchemy.TEXT(), nullable=False),

    sqlalchemy.Column('fromEmail', sqlalchemy.CHAR(length=320), nullable=False),
    sqlalchemy.Column('replyToEmail', sqlalchemy.CHAR(length=320), nullable=False),

    sqlalchemy.Column('v_createdAt', sqlalchemy.TIMESTAMP(), server_default=sqlalchemy.text('NOW()'), nullable=False),
    sqlalchemy.Column('v_updatedAt', sqlalchemy.TIMESTAMP(), server_default=sqlalchemy.text('NOW()'), nullable=False),
    sqlalchemy.Column('v_deletedAt', sqlalchemy.TIMESTAMP()),

    sqlalchemy.Column('v_createdBy', sqlalchemy.CHAR(length=30), nullable=False),
    sqlalchemy.Column('v_updatedBy', sqlalchemy.CHAR(length=30), nullable=False),
    sqlalchemy.Column('v_deletedBy', sqlalchemy.CHAR(length=30))
)

def createSchema(insertFake = False):
    from config import Config
    from sql import registeredStoredProcedures
    from sqlalchemy import text, func
    engine = sqlalchemy.create_engine(Config.DB_URL)
    metadata.drop_all(engine)
    metadata.create_all(engine)

    conn = engine.connect()
    for sp in registeredStoredProcedures:
        conn.execute(sp)
    if insertFake:
        from fakedata import faketemps, fakevers
        for table, fakeEntries in zip((templates, versions), (faketemps, fakevers)):
            conn.execute(table.insert(), fakeEntries)
        conn.execute(func.insertVersion('temp1                                                                 ', 3, 'ammar2', 'ammar3', 'ammarr', 'ammar5', 'ammar6'))
    conn.close()

if __name__ == "__main__":
    createSchema(insertFake=True)