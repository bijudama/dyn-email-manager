'''
    This module take the rows data, and return dict format ready for json converting
'''

import datetime


def serializeTemplates(templates):
    '''
        serialize templates
    '''
    def serializeOne(template):
        if not template:
            return template
        d = dict(template)
        print("template record after converting to dict:", d)
        _convertDateTimeFromDict(d)
        _cleanDict(d)
        return d
    return [serializeOne(template) for template in templates]


def serializeTemplate(template):
    if not template:
        return template
    d = dict(template)
    print("template record after converting to dict:", d)
    _convertDateTimeFromDict(d)
    _cleanDict(d)
    return d


def serializeVersion(version):
    if not version:
        return version
    verAsDict = dict(version)
    _convertDateTimeFromDict(verAsDict)
    _cleanDict(verAsDict)
    return verAsDict

def serializeVersions(versions):
    return [serializeVersion(v) for v in versions]

def _cleanDict(d):
    '''
        clean dict by removing None value keys, remove any extra spaces
    '''
    for key in list(d.keys()):
        if d[key] == None:
            del d[key]
    for key in d.keys():
        if(isinstance(d[key], str)):
            d.update({key: d[key].strip()})

def _convertDateTimeFromDict(d):
    '''
        Take a dictionary that have createdAt, updatedAt and/or deletedAt keys
        update them in place with string equiv.
        If value is none, this key is removed
    '''
    for timeKey in ["t_createdAt", "t_updatedAt", "t_deletedAt", "v_createdAt", "v_updatedAt", "v_deletedAt"]:
        if d.get(timeKey):
            print(d[timeKey], str(d[timeKey]))
            d.update({timeKey: str(d[timeKey])})