from rest_framework.views import APIView
from rest_framework.response import Response
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from django.db import connection
from .models import Logs

class IndexView(APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        if prompt:
            try:
                # Processed Prompt
                template = """There is a SQL Table by the name "Sales" which contains information in the following format:
                    MONTH	STORECODE	DAY	BILL_ID	BILL_AMT	QTY	VALUE	PRICE	GRP	SGRP	SSGRP	CMP	MBRD	BRD
                    M1	N1	4	T375	225	1	225	225	BUTTER MARGR  (4/94)	BUTTER	SALTED	G C M M F	AMUL	AMUL
                    M1	N1	4	T379	95	1	95	95	CONFECTIONERY - ECLAIRS	CONFECTIONERY - ECLAIRS	CONFECTIONERY - ECLAIRS	PARLE PRODS	MELODY	MELODY CHOCOLATY
                    M1	N1	4	T381	10	1	10	10	CHOCOLATE	CHOCOLATE PANNED	CHOCOLATE PANNED	MONDELEZ INTERNATIONAL	CADBURY SHOTS	CADBURY SHOTS
                    M1	N1	4	T382	108	1	108	108	PACKAGED TEA	MAIN PACKS	MAIN PACKS	GUJ TEA PROCESSORS	WAGH BAKRI	WAGH BAKRI INSTANT
                    
                    Create a SQL Program to answer the following question for the Sales Table:
                    {prompt}
                    Format the output as JSON with the following keys:
                    query: The SQL query that should be executed. All identifiers in the query should be in quotes."""
                
                prompt_template = ChatPromptTemplate.from_template(template)
                print("Stage 1 : Prompt Template\n\n")
                print(prompt_template)
                stage1 = prompt_template
                
                messages = prompt_template.format_messages(prompt=prompt)
                chat = ChatOpenAI(temperature=0.0, openai_api_key="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")
                response = chat(messages)
                print("\n\nStage 2: Initial Response\n\n")
                print(response.content)

                stage2 = response.content

                
                querySchema = ResponseSchema(name="query", description="A SQL query that should be executed. All identifiers in the query should be in quotes.")
                responseSchemas = [querySchema]
                output_parser = StructuredOutputParser.from_response_schemas(responseSchemas)
                format_instructions = output_parser.get_format_instructions()
                print("\n\nStage 3: Format Instructions\n\n")
                print(format_instructions)

                stage3 = format_instructions
                
                template2 = """There is a SQL Table by the name "Sales" which contains information in the following format:
                    MONTH	STORECODE	DAY	BILL_ID	BILL_AMT	QTY	VALUE	PRICE	GRP	SGRP	SSGRP	CMP	MBRD	BRD
                    M1	N1	4	T375	225	1	225	225	BUTTER MARGR  (4/94)	BUTTER	SALTED	G C M M F	AMUL	AMUL
                    M1	N1	4	T379	95	1	95	95	CONFECTIONERY - ECLAIRS	CONFECTIONERY - ECLAIRS	CONFECTIONERY - ECLAIRS	PARLE PRODS	MELODY	MELODY CHOCOLATY
                    M1	N1	4	T381	10	1	10	10	CHOCOLATE	CHOCOLATE PANNED	CHOCOLATE PANNED	MONDELEZ INTERNATIONAL	CADBURY SHOTS	CADBURY SHOTS
                    M1	N1	4	T382	108	1	108	108	PACKAGED TEA	MAIN PACKS	MAIN PACKS	GUJ TEA PROCESSORS	WAGH BAKRI	WAGH BAKRI INSTANT
                    
                    Create a SQL Program to answer the following question for the Sales Table:
                    {prompt}
                    
                    {format_instructions}"""
                    
                prompt_template2 = ChatPromptTemplate.from_template(template=template2)
                messages = prompt_template2.format_messages(prompt=prompt, 
                                    format_instructions=format_instructions)
                print("\n\nStage 4: Better Prompt Template\n\n")
                print(messages[0].content)

                stage4 = messages[0].content
                
                response = chat(messages)
                print("\n\nStage 5: Better Response\n\n")
                print(response.content)

                stage5 = response.content
                
                output_dict = output_parser.parse(response.content)
                query = output_dict.get('query')
                print(query)
                # template3 = """Enclose all the identifiers in the following query by double quotes so as to preserve their\
                #     case sensitive nature:
                #     query: {query}
                #     The output should be an execute SQL query."""
                    
                # prompt_template3 = ChatPromptTemplate.from_template(template3)
                # messages = prompt_template3.format_messages(query=query)
                # response=chat(messages)
                # print("\n\nStage 6: Filtered Query\n\n")
                # print(response.content)
                
                final_response = run_query(query)
                
                template4 = """This query was run on a database:
                {query}
                ---
                This is response of the query: 
                {final_response}
                ---
                Format the response as html in a meaningful manner."""
                prompt_template4 = ChatPromptTemplate.from_template(template=template4)
                messages = prompt_template4.format_messages(query=query,final_response=final_response)
                html_response = chat(messages)
                
                print("\n\nStage 6: HTML Response\n\n")
                print(html_response.content)

                stage6 = html_response.content
                logs_instance = Logs(
                    prompt_template=stage1,
                    initial_response=stage2,
                    format_instructions=stage3,
                    better_prompt_template=stage4,
                    better_response=stage5,
                    html_response = stage6
                )


                logs_instance.save()
                
                return Response(html_response.content)
            except Exception as e:
                return Response({'error': str(e)})
        else:
            return Response({'error': 'No prompt provided.'})

def run_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    return rows
