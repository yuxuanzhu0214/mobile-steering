from pisugar import *

conn, event_conn = connect_tcp('127.0.0.1')
s = PiSugarServer(conn, event_conn)

s.register_single_tap_handler(lambda: print('single'))
s.register_double_tap_handler(lambda: print('double'))

version = s.get_version()
print(s.get_battery_level())