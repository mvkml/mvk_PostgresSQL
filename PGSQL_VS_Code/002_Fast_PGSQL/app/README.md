# VishAgent Application

FastAPI-based AI agent system for industrial AI assistance.

## Key Design Patterns

### API Buffer Memory Pattern

Reference: [api_buffer_memory.py](api/api_state/api_buffer_memory.py)

---

## 1. Dependency Injection Pattern

**Using `Annotated` with `Depends` for clean dependency injection:**

```python
from typing_extensions import Annotated
from fastapi import Depends
from app.dependencies.di_utilities import di_get_api_validation

# Define reusable dependency annotation at module level
di_api_validation = Annotated[IAPIValidation, Depends(di_get_api_validation)]

# Inject into endpoint
@router.post("/prompt")
async def post_default(
    request: PromptRequest,
    api_validation: di_api_validation  # Auto-injected by FastAPI
) -> PromptResponse:
    model = api_validation.validate_prompt_request(request)
    ...
```

**Benefits:**
- **Type-safe**: Static type checking with interfaces
- **Reusable**: Define once, use in multiple endpoints
- **Testable**: Easy to mock dependencies for unit tests
- **Clean**: Separates concerns from business logic

**Dependency Factory Pattern:**

```python
# File: app/dependencies/di_utilities.py
def di_get_api_validation() -> IAPIValidation:
    return APIValidation()
```

---

## 2. Protocol-Based Interface Pattern

**Define contracts using Python's Protocol:**

```python
from typing import Protocol

class IAPIValidation(Protocol):
    """Interface for API validation - defines contract"""
    def validate_prompt_request(self, request: PromptRequest) -> PromptModel:
        ...
```

**Concrete Implementation:**

```python
class APIValidation:
    """Concrete implementation of IAPIValidation"""
    def validate_prompt_request(self, request: PromptRequest) -> PromptModel:
        model = PromptModel()
        if request is None:
            model = self.set_inv_msg(model, "Request is None")
            return model
        if not request.question:
            model = self.set_inv_msg(model, "Question is required")
            return model
        return model
```

**Why Protocols?**
- **Loose coupling**: Code depends on interface, not implementation
- **Duck typing with types**: Python flexibility + static type safety
- **Swappable implementations**: Easy to replace without breaking API
- **Better testing**: Mock interfaces easily

---

## 3. Three-Layer Model Pattern

**Request → Model → Response architecture:**

```python
# Layer 1: API Request (Input)
class PromptRequest(BaseModel):
    question: Optional[str] = None
    context: Optional[str] = None
    session_id: Optional[str] = None

# Layer 2: Business Logic Model (Processing)
class PromptModel(ModelBase):
    request: Optional[PromptRequest] = None
    response: Optional[PromptResponse] = None
    # Inherited from ModelBase:
    # Message: str | None = None
    # IsInvalid: bool = False

# Layer 3: API Response (Output)
class PromptResponse(ItemBase):
    response: Optional[str] = None
    prompt_id: Optional[str] = None
    model_name: Optional[str] = None
    tokens_used: Optional[int] = None
```

**Base Classes Hierarchy:**

```python
# File: app/models/common/common_base.py
class ItemBase(BaseModel):
    """Base for all request/response models"""
    Message: str | None = None
    IsInvalid: bool = False

class ModelBase(BaseModel):
    """Base for business logic models"""
    Message: str | None = None
    IsInvalid: bool = False
```

**Benefits:**
- **Clear separation**: API contracts vs business logic
- **State tracking**: `IsInvalid` and `Message` available throughout processing
- **Consistent error handling**: All models can carry validation state
- **Reusability**: Common fields in base classes

---

## 4. Validation Pattern (Returns Model, Not Boolean)

**Key principle: Validators return enriched model objects:**

```python
def validate_prompt_request(self, request: PromptRequest) -> PromptModel:
    model = PromptModel()
    try:
        if request is None:
            model = self.set_inv_msg(model, "Request is None")
            return model  # Still returns model, not raising exception
            
        if not request.question:
            model = self.set_inv_msg(model, "Question is None or empty")
            return model
            
        return model  # Valid model
        
    except Exception as ex:
        model = self.set_inv_msg(model, str(ex))
        return model

def set_inv_msg(self, model: PromptModel, msg: str) -> PromptModel:
    model.IsInvalid = True
    model.Message = msg
    return model
```

**Why this pattern?**
- **No exceptions for validation**: Validation errors don't crash the flow
- **Enriched context**: Model carries validation state and error messages
- **Consistent flow**: Same return type whether valid or invalid
- **Chainable**: Can pass model through multiple validation layers

**Usage in endpoint:**

```python
@router.post("/prompt")
async def post_default(request: PromptRequest, api_validation: di_api_validation):
    response = PromptResponse()
    try:
        model = api_validation.validate_prompt_request(request)
        
        # Check validation result
        if model.IsInvalid:
            response.Message = model.Message
            return response
            
        # Continue processing...
        model.response = response
        
    except Exception as ex:
        response.Message = {"error": str(ex)}
    return response
```

---

## 5. Session Management Pattern

**In-memory session store for conversational AI:**

```python
# Module-level store (use Redis/DB in production)
store = {}

def get_session_history(session_id: str):
    """Lazy initialization of session history"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
```

**Usage with LangChain:**

```python
from langchain_core.chat_history import InMemoryChatMessageHistory

# Retrieve/create session history
history = get_session_history(session_id="user_123")

# Use in LLM chain for conversation continuity
history.add_user_message("What is AI?")
history.add_ai_message("AI is...")
```

**Use cases:**
- **Conversation continuity**: Maintain context across requests
- **Multi-turn dialogues**: Remember previous exchanges
- **Session isolation**: Each user has separate conversation history

**Production considerations:**
- Replace dict with Redis for distributed systems
- Add TTL for session expiration
- Implement session cleanup/garbage collection

---

## 6. Configuration Centralization Pattern

**Single source of truth for settings:**

```python
# File: app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    open_ai_key: str
    open_ai_model_name: str = "gpt-4o-mini"
    # ... other settings

settings = Settings()
```

**Access pattern with helper functions:**

```python
from app.core.config import settings

def get_llm():
    llm = ChatOpenAI(
        model_name=get_model_name(),
        temperature=0,
        openai_api_key=get_open_ai_key()
    )
    return llm

def get_model_name():
    return settings.open_ai_model_name

def get_open_ai_key():
    return settings.open_ai_key
```

**Benefits:**
- **Environment-based config**: `.env` file support
- **Type-safe**: Pydantic validation
- **Centralized**: One place to change configuration
- **Testable**: Easy to override in tests

---

## 7. Error Handling Pattern

**Always return response object, never raise to client:**

```python
@router.post("/prompt")
async def post_default(request: PromptRequest, api_validation: di_api_validation):
    response = PromptResponse()
    try:
        model = PromptModel()
        model = api_validation.validate_prompt_request(request)
        
        if model.IsInvalid:
            response.Message = model.Message
            return response
            
        # Process request...
        model.request = request
        model.response = response
        
    except Exception as ex:
        response.Message = {"error": str(ex)}
    
    return response  # Always return response
```

**Principles:**
- **No unhandled exceptions**: Top-level try-except in endpoints
- **Consistent structure**: Client always gets response object
- **Error details in Message**: Use `Message` field for error info
- **HTTP 200 with error flag**: Consider using `IsInvalid` flag vs HTTP error codes

---

## Applying These Patterns

### For AI Message Conversation API

1. **Create Protocol Interface:**
   ```python
   class IAIMessageValidation(Protocol):
       def validate_message_create(self, request: AiMessageCreate) -> AiMessageModel:
           ...
   ```

2. **Implement Validation:**
   ```python
   class AIMessageValidation:
       def validate_message_create(self, request: AiMessageCreate) -> AiMessageModel:
           model = AiMessageModel()
           if not request.content:
               return self.set_inv_msg(model, "Content is required")
           return model
   ```

3. **Setup Dependency:**
   ```python
   # di_utilities.py
   def di_get_ai_message_validation() -> IAIMessageValidation:
       return AIMessageValidation()
   
   # api endpoint
   di_ai_validation = Annotated[IAIMessageValidation, Depends(di_get_ai_message_validation)]
   ```

4. **Use in Endpoint:**
   ```python
   @router.post("/messages")
   async def create_message(
       request: AiMessageCreate,
       validation: di_ai_validation
   ) -> AiMessageResponse:
       response = AiMessageResponse()
       try:
           model = validation.validate_message_create(request)
           if model.IsInvalid:
               response.Message = model.Message
               return response
           # Process...
       except Exception as ex:
           response.Message = str(ex)
       return response
   ```

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────┐
│  API Layer (FastAPI Routes)                         │
│  - Dependency Injection                             │
│  - Error handling                                   │
│  - Request/Response models                          │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Validation Layer (Protocol-based)                  │
│  - IValidation interfaces                           │
│  - Concrete validators                              │
│  - Returns enriched models                          │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Business Logic Models                              │
│  - ModelBase (with IsInvalid, Message)              │
│  - Holds request + response                         │
│  - State tracking                                   │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Service Layer                                      │
│  - LLM invocation                                   │
│  - Business logic                                   │
│  - Session management                               │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  DAL Layer                                          │
│  - SQLAlchemy entities                              │
│  - Repository pattern                               │
│  - Database operations                              │
└─────────────────────────────────────────────────────┘
```

---

## Key Takeaways

✅ **Use Protocols for interfaces** - Better than abstract base classes for Python  
✅ **Dependency injection via Annotated** - Type-safe and reusable  
✅ **Validators return models** - Not booleans or exceptions  
✅ **Three-layer models** - Request → Model → Response  
✅ **Session management** - Per-user conversation history  
✅ **Centralized config** - Pydantic Settings pattern  
✅ **Graceful error handling** - Always return response objects  

This creates **clean, testable, maintainable** FastAPI applications following Python best practices.
