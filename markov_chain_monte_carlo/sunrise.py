"""
Sunrise - sunset calculator modified from:
https://michelanders.blogspot.com/2010/12/calulating-sunrise-and-sunset-in-python.html
"""
from math import sin, asin, cos, acos, tan, atan2, radians, degrees
import datetime

def __timefromdecimalday(day):
    hours = 24.0*day
    h = int(hours)
    minutes= (hours-h)*60
    m = int(minutes)
    seconds= (minutes-m)*60
    s = int(seconds)
    return h,m,s

def excel_date(date1):
    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def sunrise(d=datetime.datetime.now(), lat=42.416248,lon=-71.156670, time_zone=-5): # time_zone is offset in hours from UTC

    date = excel_date(d) # number format from excel spreadsheet 
    time = 0.1/24 

    # setup parameters
    B3 = lat
    B4 = lon
    B5 = time_zone
    B7 = date
    # cut and pasted equations fron NOAA spreadsheet
    # may have to change case (capitals to lower case, etc) of functions
    D2 = B7
    E2 = 0.1/24 # day is a decimal fraction of 24 hours between 0.0 and 1.0 (e.g. noon = 0.5) 
    F2 = D2 + 2415018.5 + E2 - B5 / 24
    G2 = (F2 - 2451545) / 36525
    I2 = (280.46646+G2*(36000.76983 + G2*0.0003032)) % 360
    J2 = 357.52911+G2*(35999.05029 - 0.0001537*G2)
    K2 = 0.016708634-G2*(0.000042037+0.0000001267*G2)
    L2 = sin(radians(J2))*(1.914602-G2*(0.004817+0.000014*G2))+sin(radians(2*J2))*(0.019993-0.000101*G2)+sin(radians(3*J2))*0.000289
    M2 = I2 + L2
    P2 = M2-0.00569-0.00478*sin(radians(125.04-1934.136*G2))
    Q2 = 23+(26+((21.448-G2*(46.815+G2*(0.00059-G2*0.001813))))/60)/60
    R2 = Q2+0.00256*cos(radians(125.04-1934.136*G2))
    T2 = degrees(asin(sin(radians(R2))*sin(radians(P2))))
    U2 = tan(radians(R2/2))*tan(radians(R2/2))
    V2 = 4*degrees(U2*sin(2*radians(I2))-2*K2*sin(radians(J2))+4*K2*U2*sin(radians(J2))*cos(2*radians(I2))-0.5*U2*U2*sin(4*radians(I2))-1.25*K2*K2*sin(2*radians(J2)))
    W2 = degrees(acos(cos(radians(90.833))/(cos(radians(B3))*cos(radians(T2)))-tan(radians(B3))*tan(radians(T2))))
    X2 = (720-4*B4-V2+B5*60)/1440
    Y2 = X2-W2*4/1440 # sunrise
    Z2 = X2+W2*4/1440 # sunset

    hrs,mins,secs = __timefromdecimalday(Y2)
    rise = datetime.datetime(d.year, d.month, d.day, hrs, mins, secs)

    hrs,mins,secs = __timefromdecimalday(Z2)
    set = datetime.datetime(d.year, d.month, d.day, hrs, mins, secs)
    
    return (rise, set)