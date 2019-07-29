from sanic.response import json
from schema import templates as templatesTable, versions as versionsTable
from sanic.response import dumps as defaultJsonDumps

from serialization import serializeTemplate, serializeTemplates, serializeVersion, serializeVersions
from queries import AppQueries


#* TODO (Enhancements): In every route handler function, there should be a class that is requested and do the whole logic of
#* building the query and also executing it
def setup(app):
    @app.route("/templates")
    async def getTemplates(request):
        templatesRows = await request.app.db.fetch_all(AppQueries.buildTemplatesQuery())
        return json({
            'templates': serializeTemplates(templatesRows)
        })

    @app.route("/templates/<templateName>")
    async def getTemplate(request, templateName):
        query = AppQueries.buildTemplateByNameQuery(templateName)
        templateRow = await request.app.db.fetch_one(query)
        # templateRow = templateRow[0] if len(templateRow) > 0 else None
        return json({
            'template': serializeTemplate(templateRow)
        })

    @app.route("/templates/<templateName>/versions")
    async def getVersions(request, templateName):
        rows = await request.app.db.fetch_all(AppQueries.buildTemplateVersionsQuery(templateName))
        return json({
            'versions': serializeVersions(rows)
        })

    @app.route("/templates/<templateName>/versions/<versionNumber>")
    async def getVersion(request, templateName, versionNumber):
        row = await request.app.db.fetch_one(AppQueries.buildVersionQuery(templateName, int(versionNumber)))
        return json({
            'version': serializeVersion(row)
        })


    @app.route("/templates", methods=['POST'])
    async def insertTemplate(request):
        body = request.json
        if not body:
            return json({"err": "there is no request body, you should provide json data of the template having name, createdBy, fromEmail, replyToEmail, body, subject"})
        templatesRows = await request.app.db.execute(AppQueries.buildInsertTemplateQuery(body))
        return json({
            'mes': "2shta yaba"
        })

    @app.route("/templates/<templateName>/versions", methods=['POST'])
    async def insertVersion(request, templateName):
        body = request.json
        if not body:
            return json({"err": "there is no request body, you should provide json data of the version having createdBy, fromEmail, replyToEmail, body, subject"})
        _ = await request.app.db.execute(AppQueries.buildInsertVersionQuery({**body, "name": templateName}))
        return json({
            'mes': "2shta yaba"
        })

    @app.route("/templates/<templateName>/activeVersion/<activeVersion:int>", methods=['PUT'])
    async def setActiveVersion(request, templateName, activeVersion):
        templatesRows = await request.app.db.execute(AppQueries.setActiveVersion(templateName, activeVersion))
        return json({
            'mes': "2shta yaba"
        })