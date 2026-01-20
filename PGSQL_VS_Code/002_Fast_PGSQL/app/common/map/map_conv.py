
from app.models.conv.ai_message_model import AIMessageItem, AIMessageModel, AiMessageRequest

class MapConv:
    def __init__(self):
        pass

    def get_item_by_request(
                        self,
                        source: AiMessageRequest,
                        destination: AIMessageItem | None = None
                            ) -> AIMessageItem:

        if destination is None:
            destination = AIMessageItem()
            
        if source is None:
            raise ValueError("AiMessageRequest cannot be None")

        destination.message_id = source.message_id
        destination.session_id = source.session_id
        destination.tenant_id = source.tenant_id
        destination.user_id = source.user_id
        destination.role = source.role
        destination.content = source.content
        destination.meta = source.meta
        destination.created_at = source.created_at

        return destination

