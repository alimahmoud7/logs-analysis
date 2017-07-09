#!/usr/bin/env python3
#
# A Reporting tool
# By `Ali Mahmoud` in `Udacity`

import psycopg2


def get_query(q, db="news"):
    """Connect to the database, Execute and return query results."""
    conn = psycopg2.connect(dbname=db)
    c = conn.cursor()
    c.execute(q)
    results = c.fetchall()
    conn.close()
    return results


def write_output(file, query, word=''):
    """Write query results in a text file with some modifications.

    Args:
        file: a file object to write in it
        query: the query that we want to get and print it
        word: an extra string added to describe numeric types
    """
    for i in get_query(query):
        file.write("- {} -- {} {}\n".format(str(i[0]), str(i[1]), word))
    file.write('\n\n')

# 1. What are the most popular three articles of all time?
query1 = """
SELECT article_title, views
FROM   collect
LIMIT 3;"""

# 2. Who are the most popular article authors of all time?
query2 = """
SELECT author_name, sum(collect.views)::INTEGER AS views
FROM   collect
GROUP BY author_name
ORDER BY views DESC;"""

# 3. On which days did more than 1% of requests lead to errors?
query3 = """
SELECT to_char(day, 'FMMonth DD,YYYY'),  -- For output style only
       error_percent::NUMERIC
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

if __name__ == '__main__':
    # Writing the output of the queries
    with open('output.txt', 'w') as f:
        f.write('1. What are the most popular three articles of all time?\n')
        write_output(f, query1, 'views')
        f.write('2. Who are the most popular article authors of all time?\n')
        write_output(f, query2, 'views')
        f.write('3. On which days did more than 1% of requests '
                'lead to errors?\n')
        write_output(f, query3, '% errors')
