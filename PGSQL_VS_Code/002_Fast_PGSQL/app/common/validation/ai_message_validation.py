    


from app.models.conv.ai_message_model import AIMessageModel,AiMessageRequest


class AIMessageValidation():
    def __init__(self):
        pass
    def set_inv_msg(self, model: AIMessageModel, msg: str) -> AIMessageModel:
        model.IsInvalid = True
        model.Message = msg
        return model

    def validate_request(self,request:AiMessageRequest)->AIMessageModel:
        model = AIMessageModel()
        try:
            if request == None:
                model.request = AiMessageRequest()
                model = self.set_inv_msg(model=model,msg="Request is None")
                return model
            if request.content == None:
                model = self.set_inv_msg(model=model,msg="Content is None")
                return model
            return model
        except Exception as ex:
            model = self.set_inv_msg(model=model,msg=str(ex))
        return model
