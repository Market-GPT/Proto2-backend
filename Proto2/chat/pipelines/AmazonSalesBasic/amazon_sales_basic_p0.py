from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from django.db import connection

def amazon_sales_basic_p0(prompt) :
    template = """
    The schema of the table defines the structure and data types of each column in the table. Based on the data provided, the schema of the table can be described as follows:

product_id: A unique identifier for each product. It seems to be an alphanumeric code used to distinguish between different products.

product_name: The name or title of the product. This column contains the name of the product being sold.

category: The category or categories to which the product belongs. It seems to be a hierarchical categorization of the product, separated by the "|" symbol.

discounted_price: The discounted price of the product. It is represented as a string with a currency symbol and numeric value.

actual_price: The actual/original price of the product before the discount. It is represented as a string with a currency symbol and numeric value.

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

product_link: The URL link to the product page on Amazon or an online marketplace. It represents the link to the product for users to view and potentially make a purchase."""
    return ''

def run_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    return rows