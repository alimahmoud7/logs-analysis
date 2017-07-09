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

if __name__ == '__main__':
    # Writing the output of the queries
    with open('output.txt', 'w') as f:
        f.write('1. What are the most popular three articles of all time?\n')
        write_output(f, query1, 'views')

