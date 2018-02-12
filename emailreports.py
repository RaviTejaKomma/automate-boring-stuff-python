"""  Assignment6 """
'''
This exercise builds on assignment 5 and explores sending mail programatically using smtplib

Assuming that you have imported the data into the database in previous assignment,
write a click script (collegereport.py) which will take a college acronym (say gvp)
and sends out a class report to a specified email (use your friends email).

The report should contain 3 parts:
The list of college students and their scores
The college summary (count of students, min, max, avg) and
The global summary for the whole class (for comparison).

Use smtplib and and send email from gmail.
 You can take the gmail credentials as environment variables (click supports reading arguments from env variables).
'''

import click
import smtplib
import MySQLdb
from MySQLdb import Error
import getpass

def generate_report(collegeacronym):

    try:
        conn = MySQLdb.connect(host="localhost",user="root",passwd="raviprince57",db="statistics")
        cur1 = conn.cursor()
        cur2 = conn.cursor()

        query = '''SELECT STUDENTS.NAME,MARKS.TRANFORM,MARKS.FROM_CUSTOM_BASE26,MARKS.GET_PIG_LATIN,MARKS.TOP_CHARS,MARKS.TOTAL
        FROM STUDENTS INNER JOIN MARKS ON
        TRIM(TRAILING '_mock'  FROM TRIM( LEADING 'ol2016_%s_' FROM MARKS.STUDENT)) = LOWER(STUDENTS.DBNAMES)''' % collegeacronym
        cur1.execute(query)
        college_report = list(cur1.fetchall())

        college_report = [[report[0], str(report[1]), str(report[2]), str(report[3]), str(report[4])] for report in college_report]

        query = query = "SELECT CAST(COUNT(TOTAL) AS CHAR(8)), CAST(AVG(TOTAL) AS CHAR(8)),CAST(MAX(TOTAL) AS CHAR(8))," \
                        "CAST(MIN(TOTAL) AS CHAR(8)) " \
                        "FROM MARKS WHERE STUDENT LIKE '%"+collegeacronym+"%'"

        cur1.execute(query)
        college_summary = list(cur1.fetchall()[0])

        query = "SELECT COUNT(COLLEGE),COLLEGE FROM STUDENTS GROUP BY COLLEGE"
        cur1.execute(query)
        students_count = {tup[1]: tup[0] for tup in cur1.fetchall()}  ## collegename : count

        query = "SELECT STUDENTS.COLLEGE,AVG(MARKS.TOTAL),MAX(MARKS.TOTAL),MIN(MARKS.TOTAL) FROM MARKS , STUDENTS " \
                "WHERE MARKS.STUDENT LIKE CONCAT(CONCAT('%',STUDENTS.COLLEGE),'%') GROUP BY STUDENTS.COLLEGE"
        cur1.execute(query)
        result = cur1.fetchall()
        global_summary = []
        for report in result:
            count = students_count[report[0]]
            global_summary.append([report[0], str(count), str(report[1]), str(report[2]), str(report[3])])

        conn.close()
    except Error as e:
        print e

    return (college_report,college_summary,global_summary)

@click.command()
@click.argument("collegeacronym",nargs=1)
@click.argument("emailidstosendreports",nargs=-1)
def emailreports(collegeacronym,emailidstosendreports):

    college_report,college_summary,global_summary = generate_report(collegeacronym)
    global_summary = ["        ".join(report) for report in global_summary]
    college_report = ["        ".join(report) for report in college_report]

    "sending the generated reports as email"
    gmail_user = "ravieee929374s@gmail.com"
    gmail_password = getpass.getpass("Enter the password : ")
    sent_from = gmail_user
    to = emailidstosendreports
    subject = "%s student's performance report" % collegeacronym

    body = "%s college students results\n\n" % collegeacronym +\
           "\n".join(college_report)+\
           "\n\n%s summary\n\n" % collegeacronym + \
           "         ".join(college_summary)+\
           "\n\nAll colleges summary\n\n" +\
           "\n".join(global_summary)

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print "--Reports sent successfully!--"
    except:
        print 'Something went wrong...'

    pass

if __name__=='__main__':
    emailreports()