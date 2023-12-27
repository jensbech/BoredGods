
from llama_index import SimpleDirectoryReader
from llama import client, logger
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.callbacks import CallbackManager, LlamaDebugHandler
from llama_index import ServiceContext
import os
import openai
from llama_index.callbacks.schema import CBEventType, EventPayload


os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.environ["OPENAI_API_KEY"]


llama_debug = LlamaDebugHandler(print_trace_on_end=True)

callback_manager = CallbackManager([llama_debug])

service_context = ServiceContext.from_defaults(
    callback_manager=callback_manager
)

ingestion_data = SimpleDirectoryReader(
    input_dir="../data", recursive=True).load_data()

vector_query_engine = VectorStoreIndex.from_documents(
    ingestion_data,
    use_async=True,
    service_context=service_context
).as_query_engine()

query_engine_tools = [
    QueryEngineTool(
        query_engine=vector_query_engine,
        metadata=ToolMetadata(
            name="Kazar Campaign Wiki",
            description="A Wiki about the Dungeons and Dragons campaign Kazar"
        )
    )
]

query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools,
    service_context=service_context,
    use_async=True,
)

for i, (start_event, end_event) in enumerate(
    llama_debug.get_event_pairs(CBEventType.SUB_QUESTION)
):
    qa_pair = end_event.payload[EventPayload.SUB_QUESTION]
    print("Sub Question " + str(i) + ": " + qa_pair.sub_q.sub_question.strip())
    print("Answer: " + qa_pair.answer.strip())
    print("====================================")


response = query_engine.query("Who is Sasha Yarna?")

print(response)
