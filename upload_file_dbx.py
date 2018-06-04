#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dropbox 
access_token = '****************************************************************'
#file_from = 'C:/DATA/ARCHIVE/201805240936/AKAMALIK_201805240936_MET_GPS.txt'
#file_to = '/RG/AKAMALIK_201805240936_MET_GPS.txt'
def upload_file_dbx(file_from, file_to):
    dbx = dropbox.Dropbox(access_token,timeout=300)
    f = open(file_from, 'rb')
    try:
        dbx.files_upload(f.read(), file_to)
    except dbx.requests.exceptions.ReadTimeout:
        print "Timeout occurred"

#upload_file(file_from,file_to)