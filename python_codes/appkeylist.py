
from os import getcwd

APPKEY_FILENAME = getcwd() + '/appkey.txt'

# registered appkey list
REG_CASH_APPKEY_LIST = ['5e228d8d-c869-437c-ae70-8dd87b089f64']

# 2017 July update  by jwkang
# REG_CLiP_APPKEY_LIST = ['6227368d-7a59-4805-a110-24b23e8c87b3',\ # CLiP (android)
#                         '8fb51470-f709-4d9b-b4a6-b0cd49e606ac',\ # devCLiP
#                         '658248d8-8e06-4e49-b00d-1b4591a7fbe7',\ # CLip (sale)
#                         '0378a4f0-fb73-4715-b55f-723cb564ad1f'] # CLip (iOS)

REG_CLiP_APPKEY_LIST = ['6227368d-7a59-4805-a110-24b23e8c87b3',\
                        '8fb51470-f709-4d9b-b4a6-b0cd49e606ac',\
                        '658248d8-8e06-4e49-b00d-1b4591a7fbe7',\
                        '0378a4f0-fb73-4715-b55f-723cb564ad1f']

REG_USER_APPKEY_LIST = ['25166e7c-ecfc-4074-857f-f4487a6557c1',
                        '5c44a99e-a4ad-4a1c-874b-8343526b3451',  # test monitoring
                        't-est-sche-dule'] # test schedule data

REG_APPKEY_LIST         = REG_CASH_APPKEY_LIST + REG_CLiP_APPKEY_LIST + REG_USER_APPKEY_LIST

class AppkeyList(object):
    def __init__(self):
        self.isInit = False

    def setAppkeyList(self, appname='None'): # Appkey is set to the first element of each app list
        print '# [AppkeyList] init by appname starts -'

        self.isInit = True
        if appname == 'clip': # CLiP
            self.appkey = REG_CLiP_APPKEY_LIST[0]

        elif appname == 'cash':  # CASH
            self.appkey = REG_CASH_APPKEY_LIST[0]

        elif appname == 'user':  # USER
            self.appkey = REG_USER_APPKEY_LIST[0]
        elif appname == 'monitoring':           # monitoring test
            self.appkey = REG_USER_APPKEY_LIST[1]
        elif appname == 'schedule':         # schedule data test
            self.appkey = REG_USER_APPKEY_LIST[2]
        elif appname == 'None': # Default
            appname = 'clip' # Default as CLiP
            self.appkey = REG_CLiP_APPKEY_LIST[0]

        else:
            print '# [AppkeyList] The configured appname \"%s\" is not supported!' % appname
            self.isInit = False
            return self.isInit

        self.setAppname(appname)
        print '# [AppkeyList]  - appname is set to \"%s\"' % self.appname
        print '# [AppkeyList]  - appkey is set to \"%s\"' % self.appkey
        print '# [AppkeyList] ----- init finished! ---------------------'

        return self.isInit

    def setAppkeyListByAppkey(self, appkey):
        print '# [AppkeyList] init by appkey starts -'

        self.isInit = True

        if appkey in '\t'.join(REG_CLiP_APPKEY_LIST): # CLiP
            self.setAppname('clip')

        elif appkey in '\t'.join(REG_CASH_APPKEY_LIST): # CASH
            self.setAppname('cash')

        elif appkey in '\t'.join(REG_USER_APPKEY_LIST): # USER Test
            self.setAppname('user')

        elif appkey == 'None': # Default
            self.setAppname('clip') # Default as CLiP
            appkey = REG_CLiP_APPKEY_LIST[0]

        else:
            print 'The configured appkey \"%s\" is not supported!' % appkey
            self.isInit = False
            return self.isInit

        self.appkey = appkey
        print '# [AppkeyList]  - appname is set to \"%s\"' % self.appname
        print '# [AppkeyList]  - appkey is set to \"%s\"' % self.appkey
        print '# [AppkeyList] ----- init finished! ---------------------'

        return self.isInit

    # set methods
    def setAppname(self, appname):
        self.appname = appname

    # get methods
    def getAppkey(self):
        if self.isInit:
            return self.appkey
        else:
            print '# [AppkeyList] AppkeyList is not initialized yet!'
            return '\0'

    def getAppname(self):
        if self.isInit:
            return self.appname
        else:
            print '# [AppkeyList] AppkeyList is not initialized yet!'
            return '\0'
