#!/usr/bin/python
# -*- coding: utf-8 -*-

###########################################################################
#  mylsm.py -- module that provides UJI authentication for Django         #
#  ---------------------------------------------------------------------  #
#    copyright            : (C) 2009-12 by Sergio Barrachina Mir          #
#    email                : barrachi@icc.uji.es                           #
###########################################################################

###########################################################################
#                                                                         #
#  This program is free software; you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation; either version 2 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful, but    #
#  WITHOUT ANY WARRANTY; without even the implied warranty of             #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      #
#  General Public License for more details.                               #
#                                                                         #
###########################################################################



import xmlrpclib
from django.http import HttpResponseRedirect


class LSM:
    "Class that manages the UJI authentication."

    def __init__(self):
        self.Server = "http://xmlrpc.uji.es/lsm/server.php";
        #@todo: Obtain the application domain automatically
        self.Domain = "eros.act.uji.es";
        self.SessionName = "LSMSession" + self.get_app_domain(True)
        self.SessionValue = "";
        self.SessionAuth = "uji-autenticado";
        self.Path = "/"
        self.debug = 0


    def show_title(self, text):
        "Shows a title text. Used to debug."
        print
        print "<<<------------------------------"
        print "<<< %s" % text
        print "<<<------------------------------"
            

    def get_app_domain(self, n_fqdn=False):
        "from get_app_domain function [lsm.inc.php]"
        if n_fqdn:
            return self.Domain.replace(".uji.es", "").replace(".", "_")
        else:
            return self.Domain


    def get_url(self, request, url=""):
        "from get_url function [lsm.inc.php]"
        if url == "":
            url=request.build_absolute_uri()
        return url


    def login(self, request, url="", host=""):
        "from lsm_login function [lsm.inc.php]"
        cookies = request.COOKIES
        url = self.get_url(request, url)
        LSMSessionCookie = ""
        if self.debug == 1:
            self.show_title("login")
            print "<<< cokies"
            print cookies
        if cookies.has_key(self.SessionName):
            if self.debug == 1:
                print "<<< cokies dict has hey %s" % self.SessionName
            LSMSessionCookie = cookies[self.SessionName]
        connect = xmlrpclib.Server(self.Server)
        resul = connect.lsm.check_session(LSMSessionCookie, self.get_app_domain(True))
        redirect = HttpResponseRedirect("https://xmlrpc.uji.es/lsm/lsmanage.php?Tok=%s&Url=%s" % ("", url))
        if resul:
            if self.debug == 1:
                print "<<< resul"
                print resul
            autenticado = resul[0]
            gLSMSession = resul[1]
            redirect = HttpResponseRedirect("https://xmlrpc.uji.es/lsm/lsmanage.php?Tok=%s&Url=%s" % (gLSMSession, url))
            redirect.set_cookie(self.SessionName, gLSMSession, None, None, '/', self.Domain, False)
            if autenticado:
                return (True, None)
            else:
                redirect.set_cookie(self.SessionAuth, "", None, -1, '/', self.Domain, False)
                return (False, redirect)
        return (False, redirect)

    def get_login(self, request, url=""):
        "From lsm_get_login function [lsm.inc.php]"
        LSMSessionCookie = ""
        cookies = request.COOKIES
        url = self.get_url(request, url)
        if self.debug == 1:
            self.show_title("get_login")
            print "<<< cokies"
            print cookies
        if cookies.has_key(self.SessionName):
            LSMSessionCookie = cookies[self.SessionName]
            if self.debug == 1:
                print "<<< cokies dict has hey %s" % self.SessionName
                print "LSMSessionCookie cookie: %s" % LSMSessionCookie
        connect = xmlrpclib.Server(self.Server)
        resul = connect.lsm.get_login_session(LSMSessionCookie, self.get_app_domain(True))
        user = ""
        gLSMSession = ""
        if resul:
            if self.debug == 1:
                print "<<< resul"
                print resul
            user = resul[0]
            if len(resul) > 1:
                gLSMSession = resul[1]
        redirect = HttpResponseRedirect("https://xmlrpc.uji.es/lsm/lsmanage.php?Tok=%s&Url=%s" % (gLSMSession, url))
        redirect.set_cookie(self.SessionName, gLSMSession, None, 0, '/', self.Domain, False)
        return (user, redirect)


    def logout(self, request, url="http://www.uji.es/"):
        "From lsm_logout function [lsm.inc.php]"
        cookies = request.COOKIES
        redirect = HttpResponseRedirect("https://xmlrpc.uji.es/lsm/logout_sso.php?Url=%s" % url)
        if cookies.has_key(self.SessionName):
            redirect.set_cookie(self.SessionName, "", None, 0, '/', self.Domain, False)
        return redirect
