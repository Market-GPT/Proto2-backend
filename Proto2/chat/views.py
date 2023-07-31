from rest_framework.views import APIView
from rest_framework.response import Response
from chat.pipelines.AmazonSalesBasic.amazon_sales_basic_p0 import amazon_sales_basic_p0
from chat.pipelines.POS.pos_p0_initial import pos_p0_initial
from .models import Conversation
from .tasks.tasks import amazon_sales_basic_p0_task
from celery.result import AsyncResult

class POSChatView(APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        if prompt:
            try:
                p0_response = pos_p0_initial(prompt)
                return Response(p0_response)
            except Exception as e:
                return Response({'error': str(e)})
        else:
            return Response({'error': 'No prompt provided.'})


# class AmazonSalesBasicChatView(APIView):
#     def post(self, request, *args, **kwargs):
#         prompt = request.data.get('prompt')
#         if prompt:
#             conversation = Conversation(dataset="AmazonSalesBasic",user_prompt=prompt)
#             try:
#                 p0_response = amazon_sales_basic_p0(prompt,conversation)
#                 conversation.formatted_response = p0_response
#                 conversation.save()
#                 return Response(p0_response)
#             except Exception as e:
#                 conversation.error = str(e)
#                 conversation.save()
#                 return Response({'error': str(e)})
#         else:
#             return Response({'error': 'No prompt provided.'})

class AmazonSalesBasicChatView(APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        if prompt:
            conversation = Conversation(dataset="AmazonSalesBasic", user_prompt=prompt)
            conversation.save()  # Save the conversation first to get an ID
            # Run the task asynchronously
            task = amazon_sales_basic_p0_task.delay(prompt, conversation.id)
            return Response({'task_id': task.id, 'status': task.status})
        else:
            return Response({'error': 'No prompt provided.'})
        
class TaskStatus(APIView):
    def get(self, request, task_id, *args, **kwargs):
        result = AsyncResult(task_id)
        response_data = {
            'task_id': task_id,
            'status': result.status,
            'result': result.result,
        }
        return Response(response_data)