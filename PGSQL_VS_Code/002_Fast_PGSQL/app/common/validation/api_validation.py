

from typing import Protocol
from app.models.common.prompts.prompt_model import PromptModel, PromptRequest


class IAPIValidation(Protocol):
     def validate_prompt_request(self,request: PromptRequest)->PromptModel:
          ...


class APIValidation:
    def __init__(self):
        pass
    
    def set_inv_msg(self, model: PromptModel, msg: str) -> PromptModel:
        # Implement the method to set an invocation message on the model
        model.IsInvalid= True
        model.Message = msg
        return model

    def validate_prompt_request(self,request: PromptRequest)->PromptModel:
            model = PromptModel()
            try:
                # code
                if request == None:
                    model.request = PromptRequest()
                    model = self.set_inv_msg(model=model,msg="Request is None")
                    return model
                if request.question == None or request.question == "":
                    model = self.set_inv_msg(model=model,msg="Question is None or empty")
                    return model
                return model
            except Exception as ex:
                model = self.set_inv_msg(model=model,msg=str(ex))
                return model
