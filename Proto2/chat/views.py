from rest_framework.views import APIView
from rest_framework.response import Response
from chat.pipelines.AmazonSalesBasic.amazon_sales_basic_p0 import amazon_sales_basic_p0
from chat.pipelines.POS.pos_p0_initial import pos_p0_initial
from .models import Conversation


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


class AmazonSalesBasicChatView(APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        if prompt:
            conversation = Conversation(dataset="AmazonSalesBasic",user_prompt=prompt)
            try:
                p0_response = amazon_sales_basic_p0(prompt,conversation)
                conversation.formatted_response = p0_response
                conversation.save()
                return Response(p0_response)
            except Exception as e:
                conversation.error = str(e)
                conversation.save()
                return Response({'error': str(e)})
        else:
            return Response({'error': 'No prompt provided.'})
