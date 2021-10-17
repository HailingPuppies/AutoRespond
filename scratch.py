from datetime import datetime
import parsedatetime as pdt # $ pip install parsedatetime

cal = pdt.Calendar()
now = datetime.now()
print("now: %s" % now)
for time_string in ["tomorrow at 6am", "next moday at noon",
                    "2 min ago", "3 weeks ago", "1 month ago"]:
   print("%s:\t%s" % (time_string, cal.parseDT(time_string, now)[0]))