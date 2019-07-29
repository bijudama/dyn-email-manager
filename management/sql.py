from schema import templates, versions

registeredStoredProcedures = [
    f'''
        CREATE OR REPLACE FUNCTION insertVersion(
            name character(70),
            createdBy character(30),
            subject text, 
            body text, 
            fromEmail character(320),
            replyToEmail character(320)
        ) RETURNS void AS $$
        BEGIN
            INSERT INTO {versions.name}("templateName", "number", "subject", "body", "fromEmail", "replyToEmail", "v_createdBy", "v_updatedBy")
            VALUES(name, (SELECT max(v.number) + 1 as nextVersionNumber from versions as v where v."templateName" = name), subject, body, fromEmail, replyToEmail, createdBy, createdBy);
        END;
        $$ LANGUAGE plpgsql
    ''',
    f'''
        CREATE OR REPLACE FUNCTION insertTemplate(
            name character(70), 
            createdBy character(30), 
            subject text, 
            body text, 
            fromEmail character(320),
            replyToEmail character(320)
        ) RETURNS void AS $$
        BEGIN
            INSERT INTO {templates.name}("name", "t_createdBy", "t_updatedBy") VALUES (name, createdBy, createdBy);
            INSERT INTO {versions.name}("templateName", "number", "subject", "body", "fromEmail", "replyToEmail", "v_createdBy", "v_updatedBy")
            VALUES(name, 1, subject, body, fromEmail, replyToEmail, createdBy, createdBy);
        END;
        $$ LANGUAGE plpgsql
    ''',
    # TODO: return the rows affected as 1 means the updates happened, 0 means can't update
    f'''
        CREATE OR REPLACE FUNCTION setActiveVersion(
            tempName character(70),
            activeVersionNumber integer
        ) RETURNS void AS $$
        BEGIN
            UPDATE {templates.name}
            SET "activeVersion" = activeVersionNumber
            WHERE {templates.name}."name" = tempName AND
	        activeVersionNumber = any(SELECT v."number" from public.{versions.name} as v where v."templateName" = tempName and v."number" = activeVersionNumber);
        END;
        $$ LANGUAGE plpgsql
    '''
]


# import psycopg2
# con = psycopg2.connect(database="dynemailtemplates_1", user="postgres", password="159753", host="127.0.0.1", port="5432")
# cursor = con.cursor()
# createTemplateTable = '''CREATE TABLE Templates
#       (Name         CHAR(70) PRIMARY KEY NOT NULL UNIQUE,

#       Subject       TEXT            NOT NULL,
#       Body          TEXT            NOT NULL,

#       FromEmail          CHAR(320)       NOT NULL,
#       ReplyToEmail       CHAR(320)       NOT NULL,

#       ActiveVersion INT Default 1,

#       CreatedAt    TIMESTAMP       NOT NULL DEFAULT now(),
#       UpdatedAt    TIMESTAMP       NOT NULL DEFAULT now(),
#       DeletedAt    TIMESTAMP,

#       CreatedBy    CHAR(30),
#       UpdatedBy    CHAR(30),
#       DeletedBy    CHAR(30)
#       );'''


# createVersionTable = '''CREATE TABLE VERSIONS
#       (Number         INT NOT NULL,
#       TemplateName CHAR(70) NOT NULL,
#       Subject       TEXT            NOT NULL,
#       Body          TEXT            NOT NULL,

#       FromEmail          CHAR(320)       NOT NULL,
#       ReplyToEmail      CHAR(320)       NOT NULL,

#       CreatedAt    TIMESTAMP       NOT NULL DEFAULT now(),
#       UpdatedAt    TIMESTAMP       NOT NULL DEFAULT now(),
#       DeletedAt    TIMESTAMP,

#       CreatedBy    CHAR(30),
#       UpdatedBy    CHAR(30),
#       DeletedBy    CHAR(30),

#       FOREIGN KEY (TemplateName) REFERENCES Templates(Name),
#       PRIMARY KEY (Number, TemplateName)
#     );'''
# cursor.execute(createTemplateTable)
# cursor.execute(createVersionTable)
# con.commit()
# print("committed")
