import sqlalchemy as sa
from schema import templates, versions
from sqlalchemy import func, text


class AppQueries:
    _versionsAlias = {k: f"version_{k}" for k in versions.columns.keys()}

    def buildTemplatesQuery():
        return templates.select()

    def buildTemplateByNameQuery(name):
        # versionsAlias = versions.alias(**AppQueries._versionsAlias)
        query = sa.select([templates, versions]).where(sa.and_(
            templates.c.name == versions.c.templateName,
            templates.c.name == name,
            versions.c.number == templates.c.activeVersion
        ))
        return query

    def buildTemplateVersionsQuery(templateName):
        q = sa.select([versions]).where(
            versions.c.templateName == templateName
        )
        return q

    def buildVersionQuery(templateName, versionNumber):
        return versions.select().where(sa.and_(
            versions.c.number == versionNumber,
            versions.c.templateName == templateName
        ))

    def buildInsertTemplateQuery(payload):
        try:
            return AppQueries._psqlFunction("insertTemplate")(
                payload['name'],
                payload['createdBy'],
                payload['subject'],
                payload['body'],
                payload['fromEmail'],
                payload['replyToEmail'],
            )
        except KeyError as e:
            raise KeyError(f"buildInsertTemplateQuery payload hasn't all keys required ({e})")

    def buildInsertVersionQuery(payload):
        try:
            return AppQueries._psqlFunction("insertVersion")(
                payload['name'],
                payload['createdBy'],
                payload['subject'],
                payload['body'],
                payload['fromEmail'],
                payload['replyToEmail'],
            )
        except KeyError as e:
            raise KeyError(f"buildInsertVersionQuery payload hasn't all keys required ({e})")

    def setActiveVersion(templateName, number):
        return AppQueries._psqlFunction("setActiveVersion")(templateName, number)

    def _psqlFunction(functionName):
        def call(*functionParams):
            # quoteText = lambda text: f"'{text}'" if isinstance(text, str) else text
            functionParams = list(map(repr, functionParams)) # repr will do the trick for quoting the string
            return f"SELECT {functionName}({', '.join(functionParams)})"
        return call
