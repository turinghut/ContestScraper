import json
import sqlite3

class Contest:
    URL = None
    start = None
    end = None
    def __inti__(self,contest):
        URL = contest[0]
        start = contest[1]
        end = contest[2]

class DB_helper:
    cursor = connection.cursor()
    def insert_contest(json_responce):
        data = json.load(json_responce)
        for contest_details in data["objects"]["contest"]:
            URL = contest_details["href"]
            start_date = contest_details["start"]
            end_date = contest_details["end"]
            status = 0
            insert_query = "INSERT INTO CONTESTS(URL,START_DATE,END_DATE,STATUS) VALUES(" +'"' + URL + '","' + start_date + '","' + end_date + '",' + "0" + ");"
            cursor.execute(insert_query)
    def get_contests(date):
        contests = []
        select_query = "SELECT * FROM CONTESTS WHERE START_DATE = " + '"' + date + '"' + "AND STATUS = 0"
        cursor.execute(select_query)
        for row in cursor:
            contest = Contest(row)
            contests.append(contest)
        for contest in contests:
            update_query = "UPDATE CONTESTS SET STATUS = 1 WHERE URL = " + contest.URL + " AND START_DATE = " + contest.start + " AND END_DATE = " + contest.end
            cursor.execute(update_query)
        return contests;
