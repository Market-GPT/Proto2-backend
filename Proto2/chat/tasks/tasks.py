from celery import shared_task
from chat.models import Conversation
from chat.pipelines.AmazonSalesBasic.amazon_sales_basic_p0 import amazon_sales_basic_p0

@shared_task
def amazon_sales_basic_p0_task(prompt, conversation_id):
    # Retrieve the conversation instance inside the task because
    # database objects can't be passed directly to tasks
    conversation = Conversation.objects.get(id=conversation_id)
    try:
        p0_response = amazon_sales_basic_p0(prompt, conversation)
        conversation.formatted_response = p0_response
        conversation.save()
        return p0_response
    except Exception as e:
        conversation.error = str(e)
        conversation.save()
        return {'error': str(e)}
