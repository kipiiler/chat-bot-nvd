from langchain_community.llms import VLLMOpenAI

llm = VLLMOpenAI(
    openai_api_key="EMPTY",
    openai_api_base="http://localhost:8000/v1",
    # model_name="meta-llama/Llama-3.1-8B-Instruct",
    model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    max_tokens=1000,
    top_p=0.90,
    temperature=0.85,
    # stop=["<|eot_id|>"],
)
