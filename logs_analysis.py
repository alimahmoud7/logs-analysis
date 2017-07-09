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
