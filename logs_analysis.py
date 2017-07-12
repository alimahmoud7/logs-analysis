#!/usr/bin/env python3
#
# A Reporting tool
# By `Ali Mahmoud` in `Udacity`

import psycopg2
import sys


def connect(db_name="news"):
    """
    Connect to the PostgreSQL database.
    Returns a database connection and cursor.
    """
    try:
        db = psycopg2.connect(dbname=db_name)
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)
        # raise e


def fetch_query(query):
    """
    Connect to the database, query, fetch results,
    close connection, return results
    """
    db, c = connect()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def print_top_articles():
    """Fetch top articles using helper function, print results"""
    # 1. What are the most popular three articles of all time?
    query1 = """
    SELECT article_title, views
    FROM   collect
    LIMIT 3;"""
    results = fetch_query(query1)

    print('1. What are the most popular three articles of all time?')
    for i in results:
        print("- {} -- {} {}".format(str(i[0]), str(i[1]), 'views'))


def print_top_authors():
    """ Fetch top authors using helper function, print results"""
    # 2. Who are the most popular article authors of all time?
    query2 = """
    SELECT author_name, sum(collect.views) AS views
    FROM   collect
    GROUP BY author_name
    ORDER BY views DESC;"""
    results = fetch_query(query2)

    print('2. Who are the most popular article authors of all time?')
    for i in results:
        print("- {} -- {} {}".format(str(i[0]), str(i[1]), 'views'))


def print_top_error_days():
    """ Fetch top error days using helper function, print results"""
    # 3. On which days did more than 1% of requests lead to errors?
    query3 = """
    SELECT to_char(day, 'FMMonth DD,YYYY'),  -- For output style only
           error_percent
    FROM (SELECT error.day,
                 round((error_count/total_count)*100, 1) AS error_percent
          FROM (SELECT cast(time AS DATE) AS day,
                       cast(count(status) AS DECIMAL) AS error_count
                FROM   log
                WHERE  status LIKE '404%'
                GROUP BY day) AS error,
               (SELECT cast(time AS DATE) AS day,
                       cast(count(status) AS DECIMAL) AS total_count
                FROM   log
                GROUP BY day) AS total
          WHERE error.day = total.day
          ORDER BY error_percent DESC) AS percent
    WHERE error_percent > 1.0;"""
    results = fetch_query(query3)

    print('3. On which days did more than 1% of requests lead to errors?')
    for i in results:
        print("- {} -- {} {}".format(str(i[0]), str(i[1]), '% errors'))


if __name__ == '__main__':
    print_top_articles()
    print()  # For output style only
    print_top_authors()
    print()  # For output style only
    print_top_error_days()
