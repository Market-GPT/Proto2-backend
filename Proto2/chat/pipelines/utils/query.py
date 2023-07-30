from django.db import connection

def execute_query(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = [cursor.fetchall()]

            # If rows is empty, return an error
            if not rows:
                return {"result": "error",
                        "stacktrace": "No rows returned by the query"}

            if len(rows)>20:
                return {"result": "sucess",
                        "stacktrace": rows[:20]}
            
            else:
                # Return the rows
                return {"result": "success",
                        "stacktrace": rows}

    except Exception as e:
        # An error occurred while executing the query
        # Return a meaningful error message as a dictionary
        return {"result": "error",
                "stacktrace": str(e)}
