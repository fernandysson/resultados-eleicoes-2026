#!/usr/bin/env python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import settings

def upload2spreadsheet(df, worksheet=0):

    
    uf = settings.uf
    uf_dict = {
        "sp": 0,
        "pe": 1,
        "ba": 2
    }
    
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.json_keyfile, scope)
    gc = gspread.authorize(credentials)
    
    sh = gc.open('apuracao')
    worksheet = sh.get_worksheet(uf_dict[uf])
    
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    
