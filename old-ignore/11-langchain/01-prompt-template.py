from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

llm = OpenAI(temperature=0.7)

prompt = PromptTemplate(
    input_variables=['topic'],
    template='Tell me a short, funny story about {topic}.'
)

chain = prompt | llm

result = chain.invoke({'topic': 'a confused robot'})
print(result)
