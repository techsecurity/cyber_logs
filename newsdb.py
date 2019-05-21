# "Database code" for the DB News.
# !/usr/bin/env python2.7.12
import datetime
import psycopg2
DBNAME = "news"
try:
    db = psycopg2.connect(database=DBNAME)
except psycopg2.Error as e:
    print "Unable to connect to DB!"
    print e.pgerror
    print e.diag.message_detail
    sys.exit(1)
else:
        print "Connected to DB!"

c = db.cursor()
c.execute("select title, count(*) as views                                                                                                                                        from articles a, log l                                                                                                                                                  where a.slug=substring(l.path, 10)                                                                                                                                      group BY title order                                                                                                                                                    BY views desc limit 3;")
data = c.fetchall()
# print the rows
for row in data:
    print row[0], row[1]
db.close()
print("end of query, disconnected from DB")
print("---------------------------------------------")
try:
    db = psycopg2.connect(database=DBNAME)
except psycopg2.Error as e:
    print "Unable to connect to DB!"
    print e.pgerror
    print e.diag.message_detail
    sys.exit(1)
else:
        print "Connected to DB!"
c = db.cursor()
c.execute("select name, count(*) as views                                                                                                                                         from articles a, log l, authors au                                                                                                                                      where a.slug=substring(l.path, 10)                                                                                                                                      and a.author=au.id                                                                                                                                                      group BY name order BY views desc;")
data = c.fetchall()
# print the rows
for row in data:
    print row[0], row[1]
db.close()
print("end of query, disconnected from DB")
print("---------------------------------------------")
try:
    db = psycopg2.connect(database=DBNAME)
except psycopg2.Error as e:
    print "Unable to connect to DB!"
    print e.pgerror
    print e.diag.message_detail
    sys.exit(1)
else:
        print "Connected to DB!"
c = db.cursor()
# view httplogs
c.execute("create view logs as                                                                                                                                                    select time                                                                                                                                                             from log;")
c.execute("create view HTTPlogsOK as                                                                                                                                              select cast(count(*)as float) as num                                                                                                                                    from log where status!= '200 OK'                                                                                                                                        group by time limit 10;")
c.execute("create view HTTPlogsNotOK as                                                                                                                                           select cast(count(*)as float) as num                                                                                                                                    from log where status!= '404 NOT FOUND'                                                                                                                                 group by time limit 10;")
c.execute("select date(l.time), count(hNOK.num/hOK.num)                                                                                                                           as views from HTTPlogsOK hOK, HTTPlogsNotOK hNOK, logs l                                                                                                                group by l.time having count(hNOK.num/hOK.num)>1.0                                                                                                                      order by count(hNOK.num/hOK.num) desc limit 10 ;") 
data = c.fetchall()
# print the rows
for row in data:
    print row[0], row[1]
db.close()
print("end of query, disconnected from DB")
print("---------------------------------------------")