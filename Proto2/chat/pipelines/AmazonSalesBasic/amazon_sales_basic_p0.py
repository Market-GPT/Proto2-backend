import json
from Proto2.chat.pipelines.utils.openai import curtail_output
from chat.pipelines.utils.openai import get_completion_from_messages
from chat.pipelines.utils.query import execute_query

############################### Classification #############################################
delimiter = "####"
system_message_classify = f"""
You are a data analyst. You have to classify user queries appropriately.
The user query will be delimited with four hashtags,\
i.e. {delimiter}.
You have to solve user questions from a table of amazon sales data. The table name is "Table1". This name is case-sensitive.
The schema of the table can be described as follows:

product_id: A unique identifier for each product. It seems to be an alphanumeric code used to distinguish between different products.

product_name: The name or title of the product. This column contains the name of the product being sold.

category: The category or categories to which the product belongs. It seems to be a hierarchical categorization of the product, separated by the "|" symbol.

discounted_price: The discounted price of the product. It is represented as a numeric value.

actual_price: The actual/original price of the product before the discount. It is represented as a numeric value.

discount_percentage: The percentage of discount offered on the product. It is represented as a string with the percentage symbol.

rating: The average rating of the product based on user reviews. It is represented as a numeric value with one decimal place.

rating_count: The total number of ratings/reviews received for the product. It is represented as an integer.

about_product: A description or information about the product. This column contains details about the product's features, compatibility, and warranty.

user_id: A unique identifier for each user who provided a review for the product. It appears to be an alphanumeric code used to distinguish between different users.

user_name: The name of the user who provided the review. It contains the names of the users who shared their feedback.

review_id: A unique identifier for each review. It seems to be an alphanumeric code used to distinguish between different reviews.

review_title: The title or heading of the review provided by the user. It represents a brief summary of the review.

review_content: The main content or body of the review provided by the user. It contains detailed feedback, opinions, or experiences with the product.

img_link: The URL link to an image associated with the product. It appears to be an image link that may represent the product.

product_link: The URL link to the product page on Amazon or an online marketplace. It represents the link to the product for users to view and potentially make a purchase.

Understand and think what the user wants. You have to classify the type of user query.
Provide your output in json format with the following keys:

"related" : <Is the user query related to the amazon sales data table?> Either "yes" or "no"
"meta" : <Is the user query related to meta information of the amazon sales data table?> Either "yes" or "no"
"sql" : <Does this question need to be answered by performing sql query on the table?> Either "yes" or "no"
"""
'''Returns a json formatted string with "related", "meta", "sql" keys'''
def get_completion_classify(user_prompt):
    messages =  [
      {'role':'system',
      'content': system_message_classify},
      {'role':'user',
      'content': f"{delimiter}{user_prompt}{delimiter}"},
    ]

    return get_completion_from_messages(messages=messages)


################################ Generation ##################################
system_message_generate_sql = f"""
You are a data analyst. You have to create one or more sql queries to solve user query.
The user query will be delimited with four hashtags,\
i.e. {delimiter} .
You have to solve user questions from a table of amazon sales data. The table name is "Table1". This name is case-sensitive.
The schema of the table can be described as follows:

product_id: A unique identifier for each product. It seems to be an alphanumeric code used to distinguish between different products.

product_name: The name or title of the product. This column contains the name of the product being sold.

category: The category or categories to which the product belongs. It seems to be a hierarchical categorization of the product, separated by the "|" symbol.

discounted_price: The discounted price of the product. It is represented as a numeric value.

actual_price: The actual/original price of the product before the discount. It is represented as a numeric value.

discount_percentage: The percentage of discount offered on the product. It is represented as a string with the percentage symbol.

rating: The average rating of the product based on user reviews. It is represented as a numeric value with one decimal place.

rating_count: The total number of ratings/reviews received for the product. It is represented as an integer.

about_product: A description or information about the product. This column contains details about the product's features, compatibility, and warranty.

user_id: A unique identifier for each user who provided a review for the product. It appears to be an alphanumeric code used to distinguish between different users.

user_name: The name of the user who provided the review. It contains the names of the users who shared their feedback.

review_id: A unique identifier for each review. It seems to be an alphanumeric code used to distinguish between different reviews.

review_title: The title or heading of the review provided by the user. It represents a brief summary of the review.

review_content: The main content or body of the review provided by the user. It contains detailed feedback, opinions, or experiences with the product.

img_link: The URL link to an image associated with the product. It appears to be an image link that may represent the product.

product_link: The URL link to the product page on Amazon or an online marketplace. It represents the link to the product for users to view and potentially make a purchase.

Provide your output in json array format with each object having the following keys:

"assumptions" : <Make intelligent assumptions if what user wants cannot be directly answered considering the table's schema>
"sql" : <The sql query that will display the result that the user wants>
"""
'''Returns a json formatted string with "assumption" and "sql" keys'''
def get_completion_generate_sql(user_prompt):
    messages =  [
      {'role':'system',
      'content': system_message_generate_sql},
      {'role':'user',
      'content': f"{delimiter}{user_prompt}{delimiter}"},
    ]

    return get_completion_from_messages(messages=messages)

system_message_generate_text = f"""
You are a data analyst. You have to answer user query appropriately.
The user query will be delimited with four hashtags,\
i.e. {delimiter} .
You have to solve user questions from a table of amazon sales data. The table name is "Table1". This name is case-sensitive.
The schema of the table can be described as follows:

product_id: A unique identifier for each product. It seems to be an alphanumeric code used to distinguish between different products.

product_name: The name or title of the product. This column contains the name of the product being sold.

category: The category or categories to which the product belongs. It seems to be a hierarchical categorization of the product, separated by the "|" symbol.

discounted_price: The discounted price of the product. It is represented as a numeric value.

actual_price: The actual/original price of the product before the discount. It is represented as a numeric value.

discount_percentage: The percentage of discount offered on the product. It is represented as a string with the percentage symbol.

rating: The average rating of the product based on user reviews. It is represented as a numeric value with one decimal place.

rating_count: The total number of ratings/reviews received for the product. It is represented as an integer.

about_product: A description or information about the product. This column contains details about the product's features, compatibility, and warranty.

user_id: A unique identifier for each user who provided a review for the product. It appears to be an alphanumeric code used to distinguish between different users.

user_name: The name of the user who provided the review. It contains the names of the users who shared their feedback.

review_id: A unique identifier for each review. It seems to be an alphanumeric code used to distinguish between different reviews.

review_title: The title or heading of the review provided by the user. It represents a brief summary of the review.

review_content: The main content or body of the review provided by the user. It contains detailed feedback, opinions, or experiences with the product.

img_link: The URL link to an image associated with the product. It appears to be an image link that may represent the product.

product_link: The URL link to the product page on Amazon or an online marketplace. It represents the link to the product for users to view and potentially make a purchase.

Understand user query and provide answer in a step by step manner. Output each step delimited by {delimiter}.
"""
'''Returns a text string'''
def get_completion_generate_text(user_prompt):
    messages =  [
      {'role':'system',
      'content': system_message_generate_text},
      {'role':'user',
      'content': f"{delimiter}{user_prompt}{delimiter}"},
    ]

    return get_completion_from_messages(messages=messages)


################################### Enhancement #################################
system_message_enhace="""
You are a data analyst. You will be given a sql query delimited by {delimiter}.
You have to check if the problem is correctly solved by the given user sql query.
The problem is based on the table of amazon sales data. The table name is "Table1". This name is case-sensitive.
The schema of the table can be described as follows:

product_id: A unique identifier for each product. It seems to be an alphanumeric code used to distinguish between different products.

product_name: The name or title of the product. This column contains the name of the product being sold.

category: The category or categories to which the product belongs. It seems to be a hierarchical categorization of the product, separated by the "|" symbol.

discounted_price: The discounted price of the product. It is represented as a numeric value.

actual_price: The actual/original price of the product before the discount. It is represented as a numeric value.

discount_percentage: The percentage of discount offered on the product. It is represented as a string with the percentage symbol.

rating: The average rating of the product based on user reviews. It is represented as a numeric value with one decimal place.

rating_count: The total number of ratings/reviews received for the product. It is represented as an integer.

about_product: A description or information about the product. This column contains details about the product's features, compatibility, and warranty.

user_id: A unique identifier for each user who provided a review for the product. It appears to be an alphanumeric code used to distinguish between different users.

user_name: The name of the user who provided the review. It contains the names of the users who shared their feedback.

review_id: A unique identifier for each review. It seems to be an alphanumeric code used to distinguish between different reviews.

review_title: The title or heading of the review provided by the user. It represents a brief summary of the review.

review_content: The main content or body of the review provided by the user. It contains detailed feedback, opinions, or experiences with the product.

img_link: The URL link to an image associated with the product. It appears to be an image link that may represent the product.

product_link: The URL link to the product page on Amazon or an online marketplace. It represents the link to the product for users to view and potentially make a purchase.
####
The problem: {user_prompt}.
Assumptions : {assumptions}.
####
Follow these instructions to check if the query is correct:
Step 1:
Check if the query is logically correct and is answering the intended question of the user?
Don't rush to conclusions and check if the assumptions are correct. If no, correct the query. If yes, go to the next step.
Step 2:
Given the schema of the table, check if the query is syntactically correct? If no, correct the query. If yes, go to the next step.
Step 3:
Enhance the information shown by the query with some additional information which may be relevant to the problem.
Step 4:
LIMIT the query output to 6 rows only if it is more than that.

Finally, Output the modified query.
"""
'''Returns a text string'''
def get_completion_enhanced(user_prompt,assumptions,sql_query):
    messages =  [
      {'role':'system',
      'content': system_message_enhace.format(delimiter=delimiter, user_prompt=user_prompt, assumptions=assumptions)},
      {'role':'user',
      'content': f"{delimiter}{sql_query}{delimiter}"},
    ]

    return get_completion_from_messages(messages=messages)


################################### Filtering ###################################
system_message_filter=f"""
You'll be a given a user text containing sql code delimited by {delimiter}. Your role is to extract and analyse the query.
The query will operate on the table of amazon sales data. The table name is "Table1". This name is case-sensitive.

Extract SQL Query from the text.
Analyse the SQL Query step-by-step
Provide output as json with the following keys 
"sql" : sql code which does not modify or delete any data from the table such as DELETE, ALTER, DROP, INSERT, REMOVE, etc.
"modifies": Either 'yes' if query is trying to modify  "Table1" using any operations such as DELETE, ALTER, DROP, INSERT, REMOVE, UPDATE, etc.
otherwise 'no'
"""
'''Returns a json formatted string with keys "sql" and "modifies" key.'''
def get_completion_filter(text):
    messages =  [
      {'role':'system',
      'content': system_message_filter},
      {'role':'user',
      'content': f"{delimiter}{text}{delimiter}"},
    ]

    return get_completion_from_messages(messages=messages)


################################# Re-Entrancy ###################################
user_message_reentrancy="""
SQL Query : {delimiter}{sql_query}{delimiter}
Error while executing: {error}
"""
'''Returns a text string'''
def get_completion_enhanced_error(user_prompt,assumptions,sql_query,error):
    messages =  [
      {'role':'system',
      'content': system_message_enhace.format(delimiter=delimiter, user_prompt=user_prompt, assumptions=assumptions)},
      {'role':'user',
      'content': f"{delimiter}{user_message_reentrancy.format(delimiter=delimiter, sql_query=sql_query, error=error)}{delimiter}"},
    ]

    return get_completion_from_messages(messages=messages)


################################# Formatting #################################
system_message_formatted_sql="""
You'll be a given a user text delimited by {delimiter}. 
Your role is to format the text appropriately as html suitable to be displayed on
a webpage. You have to follow the following steps:
Step - 1 : Format the text as pure html. The html should contain three seperate sections for SQL Query, Assumptions and Output.
Step - 2 : The Output is a python double array. Convert it to html table.
Step - 3 : The Output should be displayed as a table that fits in a window width of 400px. If any column has a large body of text wrap or truncate the text if needed.
Step - 4 : Check that the html is valid for rendering.
Step - 5 : Provide your output as an html string.
"""
'''Returns an HTML string'''
def get_completion_formatted_sql(response):
    messages =  [
      {'role':'system',
      'content': system_message_formatted_sql.format(delimiter=delimiter)},
      {'role':'user',
      'content': f"{delimiter}{response}{delimiter}"},
    ]

    return get_completion_from_messages(messages=messages, model="gpt-3.5-turbo-16k")

system_message_formatted="""
You'll be a given a user text delimited by {delimiter}. 
Your role is to format the text appropriately as html suitable to be displayed on
a webpage. You have to follow the following steps:
Step - 1 : Format the text as pure html.
Step - 2 : The html content should be responsive.
Step - 3 : Check that the html is valid for rendering.
Step - 4 : Provide your output as an html string.
"""
'''Returns an HTML string'''
def get_completion_formatted(response):
    messages =  [
      {'role':'system',
      'content': system_message_formatted.format(delimiter=delimiter)},
      {'role':'user',
      'content': f"{delimiter}{response}{delimiter}"},
    ]

    return get_completion_from_messages(messages=messages)

        
############################### SQL Processing Pipeline ##########################
def sql_process(prompt,conversation,assumptions,sql_query,trace='',recheck=False):
    enhancement_response=""
    if(recheck):
        conversation.recheck=True
        enhancement_response = get_completion_enhanced_error(prompt,assumptions,sql_query,trace)
        conversation.regeneration=enhancement_response
    else:
        enhancement_response = get_completion_enhanced(prompt,assumptions,sql_query)
        conversation.enhancement=enhancement_response
        
    print(f"recheck:\n {recheck}",enhancement_response)
    filtered_response=get_completion_filter(enhancement_response)
    conversation.filtering=filtered_response
    json2 = json.loads(filtered_response)
    print(json2)
    sql = json2["sql"]
    modifies = json2["modifies"]
    conversation.modifies=(modifies == 'yes') if True else False
    if modifies=='yes':
        return f"SQL Query : {sql}\n\
            Assumptions : {assumptions}\n\
            The query cannot be executed as it tries to modify the database."
    else:
        execution_response = execute_query(sql)
        print(execution_response)
        conversation.execution=str(execution_response)
        print(execution_response)
        result = execution_response["result"]
        stacktrace = execution_response["stacktrace"]
        if result=="error":
            if recheck==True:
                return f"SQL Query : {sql}\n\
                    Assumptions : {assumptions}\n\
                    Error while executing: {stacktrace}"
            else:
                sql_process(prompt,conversation,assumptions,sql,stacktrace,recheck=True)
        else:
            conversation.execution_result=True
            return f"SQL Query : {sql}\n\
                Assumptions : {assumptions}\n\
                Output : {stacktrace}"  # Stacktrace would be rows if result is "success"
    
def amazon_sales_basic_p0(prompt, conversation) :
    output = ''
    json_response=json.loads(get_completion_classify(prompt))
    conversation.classification = json_response
    conversation.related=(json_response["related"] == 'yes') if True else False
    conversation.meta=(json_response["meta"] == 'yes') if True else False
    conversation.sql=(json_response["sql"] == 'yes') if True else False
    print(json_response)
    if(json_response["related"]=='yes' and json_response["sql"]=='yes' and json_response["meta"]=='no'):
        #Further processing
        generation_response=get_completion_generate_sql(prompt)
        json_res = json.loads(generation_response)
        conversation.generation=json_res
        print(json_res)
        assumptions = json_res["assumptions"]
        conversation.assumptions = assumptions
        sql_query = json_res["sql"]
        output = sql_process(prompt, conversation, assumptions, sql_query)
        conversation.final_response = output
        return get_completion_formatted_sql(curtail_output(output))
    else:
        output = get_completion_generate_text(prompt)
        conversation.generation = output
        conversation.final_response = output
        return get_completion_formatted(output)
    
    