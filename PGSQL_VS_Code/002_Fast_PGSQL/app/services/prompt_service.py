


from app.common.validation.api_validation import APIValidation
from app.dal.repositories.prompt_repository import PromptRepository
from app.models.common.prompts.prompt_model import PromptModel
from app.services.conv.ai_message_service import AIMessageService


class PromptService():
    def __init__(self,repo:PromptRepository,ai_msg_service:AIMessageService,validation_utility:APIValidation):
        self.repo = repo
        self.ai_msg_service = ai_msg_service
        self.validation_utility = validation_utility
    
    def set_inv_msg(self, model: PromptModel, msg: str) -> PromptModel:
        # Implement the method to set an invocation message on the model
        model.IsInvalid= True
        model.Message = msg
        return model

    def invoke_llm(self,model:PromptModel)->PromptModel:
        try:
            
              # code
                       
            return model
        except Exception as ex:
            model = self.set_inv_msg(model=model,msg=str(ex))
        return model