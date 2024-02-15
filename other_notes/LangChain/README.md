# LangChain Tutorial

## Table of Content

- [LangChain Tutorial](#langchain-tutorial)
  - [Table of Content](#table-of-content)
  - [Access An LLM Without Chains](#access-an-llm-without-chains)
  - [Access An LLM With Chains](#access-an-llm-with-chains)
    - [Advantages of LangChain](#advantages-of-langchain)
    - [LLM Chain](#llm-chain)
    - [Connecting Chains Together](#connecting-chains-together)
    - [ChatPrompt Template](#chatprompt-template)
      - [Example of ChatPrompt Template](#example-of-chatprompt-template)
    - [Memory](#memory)
    - [Message PlaceHolder](#message-placeholder)
      - [Example of Using Memory](#example-of-using-memory)
    - [Add Persistent Memory](#add-persistent-memory)
  - [Loading Files With Document Loaders](#loading-files-with-document-loaders)
    - [Text Loader](#text-loader)
  - [Embeddings](#embeddings)

## Access An LLM Without Chains

[![image.png](https://i.postimg.cc/RVLp2WgH/image.png)](https://postimg.cc/0brCwyRk)

## Access An LLM With Chains

### Advantages of LangChain

- Ease of Use

- Simplified Development: LangChain provides a high-level API that abstracts away the complexity of working with LLMs. This allows developers with less machine learning expertise to build sophisticated applications.

- Wide Range of Applications: LangChain is adaptable and can be used to build various applications, from chatbots and question-answering systems to content generation and data analysis tools.

- Model Agnostic: LangChain is not tied to a specific LLM provider. You can integrate with different LLMs (e.g., OpenAI API, Google AI) within the same interface.

### LLM Chain

- It contains the required arguments:
  - `LLM`
  - `Prompt Template`

```py
# Used for text completion LLMs
prompt_str: str = """Write a very short {language} function that will {task}"""
code_prompt = PromptTemplate(
    input_variables=["language", "task"], template=prompt_str
)
code_chain = LLMChain(llm=llm, prompt=code_prompt)

# Hardcoded inputs!
language, task = ("Python", "generate a list of numbers")

result = code_chain(inputs={"language": language, "task": task})
```

### Connecting Chains Together

- e.g using `SequentialChain`

[![image.png](https://i.postimg.cc/8Cdgm9wV/image.png)](https://postimg.cc/GBpfcMZM)

```py
from langchain.chains import SequentialChain

# Used for text completion LLMs
code_prompt_str: str = (
    """Write a very short {language} function that will {task}"""
)
unittest_prompt_str: str = (
    """Write a unit test for the following {language} code: \n{code}"""
)

# Propmt(s)
code_prompt = PromptTemplate(
    input_variables=["language", "task"], template=code_prompt_str
)
unittest_prompt = PromptTemplate(
    input_variables=["language", "code"], template=unittest_prompt_str
)

# Chain(s)
code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key="code",  # from text to code
)
unittest_chain = LLMChain(
    llm=llm,
    prompt=unittest_prompt,
    output_key="test",  # from text to test
)
# Feed the output of code_chain into unittest_chain
final_chain = SequentialChain(
    chains=[code_chain, unittest_chain],
    input_variables=["language", "task"],
    output_variables=["code", "test"], # output keys
)
# Hardcoded inputs!
language, task = ("Python", "generate a list of numbers")

result = final_chain(inputs={"language": language, "task": task})
print(result)
```

### ChatPrompt Template

[![image.png](https://i.postimg.cc/s2nTM32Z/image.png)](https://postimg.cc/4K96MkVJ)

[![image.png](https://i.postimg.cc/FRgxXmJ6/image.png)](https://postimg.cc/YG0FQ5RN)

#### Example of ChatPrompt Template

```py
TEMPERATURE: float = 0.5
OPENAI_CHAT_MODEL: str = "gpt-3.5-turbo"

chat_llm = ChatOpenAI(
    model=OPENAI_CHAT_MODEL,
    temperature=TEMPERATURE,
)

# Used for chat completion LLMs
prompt = ChatPromptTemplate(
    input_variables=["content"],
    messages=[HumanMessagePromptTemplate.from_template("{content}")],
)
chain: LLMChain = LLMChain(llm=chat_llm, prompt=prompt)
content: str = "Hello, who are you?"

result: dict[str, Any] = chain({"content": content})
print(result)
# {
#     'content': 'Hello, who are you?',
#     'text': 'Hello! I am an AI assistant created by OpenAI. I am here to help answer any questions you may have.
# How can I assist you today?'
# }
```

### Memory

- Memory allows LLMs to access and consider previous conversations or inputs, leading to more coherent and contextually relevant responses.

- Conversation Buffer
- Conversation Buffer Window
- Conversation Summary
- Conversation Summary Buffer, etc

[![image.png](https://i.postimg.cc/MGPkWySn/image.png)](https://postimg.cc/8F6X4fsG)

### Message PlaceHolder

- It's used to track the conversations.
- It contains the contents of the chat. i.e. the human and the AI messages.

[![image.png](https://i.postimg.cc/3wPBCRjL/image.png)](https://postimg.cc/p9JzPP68)

#### Example of Using Memory

```py
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

chat_llm = ChatOpenAI(
    model=OPENAI_CHAT_MODEL,
    temperature=TEMPERATURE,
)

# Set up memory
memory = ConversationBufferMemory(
    memory_key="messages",  # key for storing the chat history
    return_messages=True,  # returns the prompt classes. e.g. HumanMsg, AIMsg, etc
)

# Used for chat completion LLMs
prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        HumanMessagePromptTemplate.from_template("{content}"),
        MessagesPlaceholder(
            variable_name="messages"  # used to track the conversations
        ),
    ],
)

chain = LLMChain(
    llm=chat_llm,
    prompt=prompt,
    memory=memory,  # Add memory (new!)
)

content: str = "Hello, who are you?"

result: dict[str, Any] = chain({"content": content})
print(result)
```

### Add Persistent Memory

- You can add a memory that can be used to `permanently` store previous conversations.
- e.g. `FileChatMessageHistory`

[![image.png](https://i.postimg.cc/B6FGMXrt/image.png)](https://postimg.cc/bDqMvNNj)

```py
from langchain.memory import FileChatMessageHistory


chat_llm = ChatOpenAI(
    model=OPENAI_CHAT_MODEL,
    temperature=TEMPERATURE,
)

memory = ConversationBufferMemory(
    chat_memory=FileChatMessageHistory(file_path="chat_history.json"),  # New!
    memory_key="messages",  # key for storing the chat history
    return_messages=True,  # returns the promp classes. e.g. HumanMsg, AIMsg, etc
)

# Used for chat completion LLMs
prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        HumanMessagePromptTemplate.from_template("{content}"),
        MessagesPlaceholder(
            variable_name="messages" # used to track the conversations
        ),
    ],
)

chain = LLMChain(
    llm=chat_llm,
    prompt=prompt,
    memory=memory,  # Add memory
)

content: str = "Hello, what is 20+5?"
result: dict[str, Any] = chain({"content": content})

# Follow up question
content: str = "subtract 10 from the result"
result: dict[str, Any] = chain({"content": content})


print(result)
```

## Loading Files With Document Loaders

[![image.png](https://i.postimg.cc/8CDcCFjL/image.png)](https://postimg.cc/TK7f73jP)

### Text Loader

[![image.png](https://i.postimg.cc/yNV6HwbP/image.png)](https://postimg.cc/rDP2GYc0)

```py
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

fp: Path = Path("../../../data/facts.txt")
loader = TextLoader(file_path=fp)
docs: list[Any] = loader.load()

CHUNK_SIZE: int = 200
CHUNK_OVERlAP: int = 0

# Used to chunk the texts
text_splitter = CharacterTextSplitter(
    chunk_size=CHUNK_SIZE,  # 1. dets the rel. number of chars per chunk
    separator="\n",  # 2. each hunk is separated by this!
    chunk_overlap=CHUNK_OVERlAP,
)

# Load and split
docs: list[Any] = loader.load_and_split(text_splitter=text_splitter)

for d in docs:
    print(d.page_content)
```

## Embeddings
