import requests
from json import dumps as json
from uuid import uuid1 as generateClientID
import getpass
import pickle

__author__ = "JiaJiunn Chiou"
__license__= ""
__version__= "0.0.2"
__status__ = "Prototype"

class Pointer:
    def __init__ (self, value):
        try:
            self.value = value.value
        except:
            self.value = value

    def __call__ (self, value=None):
        if value == None:
            return self.value
        try:
            self.value = value.value
        except:
            self.value = value


class HTTPService:
    def __init__ (self, session, response=None, origin=None, referer=None):
        self.userAgent = "Python (X11; Linux x86_64)"
        try:
            self.session = session.session
            self.response = session.response
            self.origin = session.origin
            self.referer = session.referer
        except:
            session = session
            self.response = response
            self.origin = origin
            self.referer = referer


class IdmsaAppleService(HTTPService):
    def __init__ (self, session):
        super(IdmsaAppleService, self).__init__(session)
        self.url = "https://idmsa.apple.com"
        self.urlAuth = self.url + "/appleauth/auth/signin?widgetKey="

        self.appleSessionToken = None

    def requestAppleSessionToken (self, user, password, appleWidgetKey):
        self.session.headers.update(self.getRequestHeader(appleWidgetKey))
        self.response.value = self.session.post(self.urlAuth + appleWidgetKey,
                self.getRequestPayload(user, password))
        try:
            self.appleSessionToken = self.response().headers["X-Apple-Session-Token"]
        except Exception as e:
            raise Exception("requestAppleSessionToken: Apple Session Token query failed",
                             self.urlAuth, repr(e))
        return self.appleSessionToken

    def getRequestHeader (self, appleWidgetKey):
        if not appleWidgetKey:
            raise NameError("getRequestHeader: clientID not found")
        return {
                "Accept": "application/json, text/javascript",
                "Content-Type": "application/json",
                "User-Agent": self.userAgent,
                "X-Apple-Widget-Key": appleWidgetKey,
                "X-Requested-With": "XMLHttpRequest",
                "Origin": self.origin,
                "Referer": self.referer,
                }

    def getRequestPayload (self, user, password):
        if not user:
            raise NameError("getAuthenticationRequestPayload: user not found")
        if not password:
            raise NameError("getAuthenticationRequestPayload: password not found")
        return json({
            "accountName": user,
            "password": password,
            "rememberMe": False,
            })


class SetupiCloudService(HTTPService):
    def __init__ (self, session):
        super(SetupiCloudService, self).__init__(session)
        self.url = "https://setup.icloud.com/setup/ws/1"
        self.urlKey = self.url + "/validate"
        self.urlLogin = self.url + "/accountLogin"

        self.appleWidgetKey = None
        self.cookies = None
        self.dsid = None

    def requestAppleWidgetKey (self, clientID):
        #self.urlBase + "/system/cloudos/16CHotfix21/en-us/javascript-packed.js"
        self.session.headers.update(self.getRequestHeader())
        self.response.value = self.session.get(self.urlKey, params=self.getQueryParameters(clientID))
        try:
            self.appleWidgetKey = self.findQyery(self.response().text, "widgetKey=")
        except Exception as e:
            raise Exception("requestAppletWidgetKey: Apple Widget Key query failed",
                             self.urlKey, repr(e))
        return self.appleWidgetKey

    def requestCookies (self, appleSessionToken, clientID):
        self.session.headers.update(self.getRequestHeader())
        self.response.value = self.session.post(self.urlLogin,
                                          self.getLoginRequestPayload(appleSessionToken),
                                          params=self.getQueryParameters(clientID))
        try:
            self.cookies = self.response().headers["Set-Cookie"]
        except Exception as e:
            raise Exception("requestCookies: Cookies query failed",
                             self.urlLogin, repr(e))
        try:
            self.dsid = self.response().json()["dsInfo"]["dsid"]
        except Exception as e:
            raise Exception("requestCookies: dsid query failed",
                             self.urlLogin, repr(e))
        return self.cookies, self.dsid

    def findQyery (self, data, query):
        response = ''
        foundAt = data.find(query)
        if foundAt == -1:
            raise Exception("findQyery: " + query + " could not be found in data")
        foundAt += len(query)
        char = data[foundAt]
        while char.isalnum():
            response += char
            foundAt += 1
            char = data[foundAt]
        return response


    def getRequestHeader (self):
        return {
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Content-Type": "text/plain",
                "User-Agent": self.userAgent,
                "Origin": self.origin,
                "Referer": self.referer,
               }

    def getQueryParameters (self, clientID):
        if not clientID:
            raise NameError("getQueryParameters: clientID not found")
        return {
                "clientBuildNumber": "16CHotfix21",
                "clientID": clientID,
                "clientMasteringNumber": "16CHotfix21",
               }

    def getLoginRequestPayload (self, appleSessionToken):
        if not appleSessionToken:
            raise NameError("getLoginRequestPayload: X-Apple-ID-Session-Id not found")
        return json({
                "dsWebAuthToken": appleSessionToken,
                "extended_login": False,
                })


class ICloudWebService(HTTPService):
    def __init__ (self, session):
        super(ICloudWebService, self).__init__(session)
        self.url = "https://www.icloud.com"
        self.urlApp = self.url + "/applications"

    def requestReminderWidget(self, cookies, clientID, dsid):
        self.response.value = self.session.get("https://p47-remindersws.icloud.com/rd/startup", #TODO: hardcoded!
                params=self.getQueryParameters(clientID, dsid))
        self.reminderResponse = self.response()

    def getReminderLists (self):
        reminderLists = []
        for collection in self.reminderResponse.json()["Collections"]:
            reminderLists.append(collection["title"])
        return reminderLists

    def getCollectionGUID (self, title):
        for collection in self.reminderResponse.json()["Collections"]:
            if title == collection["title"]:
                return collection["guid"]

    def getReminderList (self, collection):
        reminderList = []
        print(self.getReminderLists())
        if collection not in self.getReminderLists():
            raise Exception("getReminderList: " + collection + " could not be found") #TODO: error handling full class
        guid = self.getCollectionGUID(collection)
        for reminder in self.reminderResponse.json()["Reminders"]:
            if guid == reminder["pGuid"]:
                reminderList.append(reminder["title"])
        return reminderList

    def getRequestHeader (self, cookies):
        return {
                "Accept": "*/*",
                "Accpet-Encoding": "gzip, deflate, sdch",
                "Connection": "keep-alive",
                "Content-Type": "text/plain",
                "Cookie": cookies,
                "Origin": self.origin,
                "Referer": self.referer,
                "User-Agent": self.userAgent,
               }

    def getQueryParameters (self, clientID, dsid):
        return {
                "clientBuildNumber": "16CProject50",
                "clientId": clientID,
                "clientMasteringNumber": "16C149",
                "dsid": dsid,
                "clientVersion": "4.0",
                "lang": "en-gb", #TODO: hardcoded!
                "usertz": "Europe/Madrid", #TODO: hardcoded!
               }


class PyiCloudService (HTTPService):
    def __init__ (self):
        self.session = requests.Session()
        self.session.verify = True
        self.response = Pointer(None)
        self.origin = "https://www.icloud.com"
        self.referer = "https://www.icloud.com"
        super(PyiCloudService, self).__init__(self)

        self._ESCAPE_CHAR = ",;&%!?|(){}[]~>*\'\"\\"

        self.clientID = self.generateClientID()

        self.idmsaApple = IdmsaAppleService(self)
        self.setupiCloud = SetupiCloudService(self)
        self.iCloudWeb = ICloudWebService(self)
        self.iCloudResponse = None

    def login (self):
        user = self.parseAccountName(input("User: "))
        password = getpass.getpass()
        try: #Try to restore previous login
            self.session.cookies.update(self.restoreCookies())
        except:
            pass #TODO: raise something?
        self.initSession(user, password)

    def initSession (self,user, password): #TODO: to much selfs!
        self.clientID = self.generateClientID()
        widgetKey = self.setupiCloud.requestAppleWidgetKey(self.clientID)
        sessionToken = self.idmsaApple.requestAppleSessionToken(user, password, widgetKey)
        self.cookies, self.dsid = self.setupiCloud.requestCookies(sessionToken, self.clientID)
        self.iCloudResponse = self.response()
        appsOrder = self.iCloudResponse.json()["appsOrder"]
        webservices = self.iCloudResponse.json()["webservices"]
        self.storeCookies()

    def get_session_token (self,user, password): #TODO: to much selfs!
        self.clientID = self.generateClientID()
        widgetKey = self.setupiCloud.requestAppleWidgetKey(self.clientID)
        return self.idmsaApple.requestAppleSessionToken(user, password, widgetKey)

    def storeCookies (self): #TODO: path hardcoded
        with open (".config/cookies", "wb") as cookieFile:
            pickle.dump(self.session.cookies, cookieFile, pickle.HIGHEST_PROTOCOL)

    def restoreCookies (self): #TODO: path hardcoded
        cookies = None
        with open (".config/cookies", "rb") as cookieFile:
            cookies = pickle.load(cookieFile)
        return cookies

    def generateClientID (self):
        return str(generateClientID()).upper()

    def parseAccountName (self, accountName):
        cleanAccountName = self.stripSpaces(self.cleanSpecialChar(accountName))
        if '@' not in cleanAccountName:
            cleanAccountName += "@icloud.com"
        return cleanAccountName


    def cleanSpecialChar (self, text):
        cleanText = text
        for char in self._ESCAPE_CHAR:
            cleanText = cleanText.replace(char, '')
        return cleanText

    def stripSpaces (self, text):
        return text.replace(' ', '').replace('\t', '')

if __name__ == "__main__":
    myICloud = PyiCloudService()
    myICloud.login()
    myICloud.iCloudWeb.requestReminderWidget(myICloud.cookies, myICloud.clientID, myICloud.dsid)
    TODO_LIST = myICloud.iCloudWeb.getReminderList("TODO")
    print(TODO_LIST)

### TEST ###
    #tPyiCloudService = PyiCloudService()
    #tPyiCloudService.requestAppleWidgetKey()
    #assert tPyiCloudService.appleWidgetKey == "83545bf919730e51dbfba24e7e8a78d2"
