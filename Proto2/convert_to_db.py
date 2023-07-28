import pandas as pd
import sqlite3

# Load spreadsheet
xl = pd.ExcelFile('D:\Proto2-backend\Proto2\Hackathon.xlsx')

# Load a sheet into a DataFrame by its name
df = xl.parse('Table1')

# Create a SQLite database
conn = sqlite3.connect('pos_database.db')

# Write the DataFrame to the SQLite database
df.to_sql('Sales', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
