import datetime

#iso8601Time = "2022-01-18T05:30:01.845563Z"

def strip8601Time(iso8601Time):
    stripper = str(iso8601Time).split(".")
    stripper = stripper[0].split("T")

    mytime = stripper[0] + " " + stripper[1]
    return mytime

def getCurrentDate():
    currentDate = datetime.datetime.now()

    return currentDate.strftime("%m-%d-%Y %I:%M:%S")





def timeexample():
    timestring = "2022-01-18T05:30:01Z"

    # Create datetime objects
    d0 = datetime.datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
    d1 = datetime.datetime.now()  # Current time

    print(d0)
    print(d1)
    # Calculate timedelta
    dt = d1 - d0

    passed_days = dt.days
    passed_seconds = dt.days  # remaining seconds
    passed_microseconds = dt.microseconds  # remaining microseconds
    total_seconds = dt.total_seconds()



