from parse import compile, search, parse, findall
import datetime
text = 'DESKTOPBASICP:  (TOTAL OF 10 LICENSES ISSUED;  TOTAL OF 1 LICENSE IN USE)\n"DESKTOPBASICP" V10.1, VENDOR: ARCGIS, EXPIRY: PERMANENT(NO EXPIRATION DATE)\nFLOATING LICENSE\nSHILANDI WIN10-SHILANDI WIN10-SHILANDI (V10.1) (GV-GISLICENSE/27000 531), START MON 12/23 11:55\ngaumere Win07-drop5a7c ,_6!/#bE-mN*5kgRxhN~xU (v10.1) (gv-gislicense/27000 412), start Wed 12/18 18:33\n'

data3 = 'DESKTOPBASICP:  (TOTAL OF 10 LICENSES ISSUED;  TOTAL OF 1 LICENSE IN USE)\n"DESKTOPBASICP" V10.1, VENDOR: ARCGIS, EXPIRY: PERMANENT(NO EXPIRATION DATE)\nFLOATING LICENSE\nSHILANDI WIN10-SHILANDI WIN10-SHILANDI (V10.1) (GV-GISLICENSE/27000 531), START MON 12/23 11:55\n'

"""
    SHILANDI WIN10-SHILANDI WIN10-SHILANDI (V10.1) (GV-GISLICENSE/27000 531), START MON 12/23 11:55
    gaumere Win07-drop5a7c ,_6!/#bE-mN*5kgRxhN~xU (v10.1) (gv-gislicense/27000 412), start Wed 12/18 18:33
    rakovice WIN10-RAKOVICE ,?UAH<iz>]_#:RNDjP8yjE6 (v10.1) (gv-gislicense/27000 131), start Mon 12/23 12:27
    albukhg WIN10-ALBUKHG1 ,?UAH<Xt/TKm)-)m?{i@0n (v10.1) (gv-gislicense/27000 1408), start Mon 12/23 14:54

"""

arr = [{'user_id': 1, 'workstation_id': 1, 'time_out': datetime.datetime(2019, 12, 25, 1, 31)},
       {'user_id': 2, 'workstation_id': 2, 'time_out': datetime.datetime(2019, 12, 26, 2, 32)},
       {'user_id': 3, 'workstation_id': 3, 'time_out': datetime.datetime(2019, 12, 27, 3, 33)}]

