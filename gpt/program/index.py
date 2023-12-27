from llama_index import ComposableGraph, GPTTreeIndex
from llama_index.indices.query.query_transform import DecomposeQueryTransform
from llama import client, logger
from llama_index.tools.query_engine import QueryEngineTool
from llama_index.query_engine.router_query_engine import RouterQueryEngine
from llama_index.selectors.llm_selectors import LLMSingleSelector


client = client.LlamaClient()

logger.enable()

llm_predictor = client.create_llm_predictor(
    temperature=0.6, model="gpt-3.5-turbo", max_tokens=256)

prompt_helper = client.create_prompt_helper(
    context_window=4096,
    num_output=256,
    chunk_overlap_ratio=0.1,
    chunk_size_limit=None)

text_splitter = client.create_sentence_splitter(
    chunk_size=1024, chunk_overlap=201)

service_context = client.create_service_context(
    llm_predictor, text_splitter, prompt_helper)

vector_indices = {}
index_summaries = {}

file_index = client.load_json_file("file_index.json")

vectore_indexs, index_summaries = client.create_vector_store_indeces(
    file_index, vector_indices, service_context, index_summaries)

graph = ComposableGraph.from_indices(
    root_index_cls=GPTTreeIndex,
    children_indices=[index for _, index in vector_indices.items()],
    index_summaries=[summary for _, summary in index_summaries.items()],
    max_keywords_per_chunk=50,
)

decompose_transform = DecomposeQueryTransform(llm_predictor, verbose=True)

custom_query_engines = (
    vector_indices, decompose_transform, service_context, graph)

graph_query_engine = graph.as_query_engine()

query_engine_tools = []

for index_summary in index_summaries:
    index = vector_indices[index_summary]
    summary = index_summaries[index_summary]

    query_engine = index.as_query_engine(service_context=service_context)
    vector_tool = QueryEngineTool.from_defaults(
        query_engine, description=summary)
    query_engine_tools.append(vector_tool)

graph_description = "This tool contains information about a fictional Dungeons and Dragons 5E universe called Kazar, including characters, locations, events and lore."
graph_tool = QueryEngineTool.from_defaults(
    graph_query_engine, description=graph_description
)
query_engine_tools.append(graph_tool)

router_query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(
        service_context=service_context,
    ),
    query_engine_tools=query_engine_tools,
)

print("ok")
# intents = discord.Intents.default()
# intents.messages = True
# intents.guilds = True
# intents.message_content = True
# intents.typing = True
# intents.presences = False
# bot = commands.Bot(command_prefix=lambda _, __: [], intents=intents)

# bot.remove_command("help")


# async def ask(message, question: str):
#     question = f"You are mysterious, pedantic and old. Your are the world seer. Answer well, and end your answers by making a context-relevant joke or fun comment. Do not answer questions about the real world. Here's the question: {
#         question}"

#     async def keep_typing():
#         while True:
#             await message.channel.trigger_typing()
#             await asyncio.sleep(5)

#     typing_task = asyncio.create_task(keep_typing())

#     loop = asyncio.get_event_loop()

#     try:
#         # Use loop.run_in_executor() to run blocking operation in a separate thread
#         response = await loop.run_in_executor(None, router_query_engine.query, question)
#         responseString = response.response
#         typing_task.cancel()

#         responseString = (
#             responseString[3:] if responseString.startswith(
#                 "A: ") else responseString
#         )

#         await message.reply(responseString)
#     except ValueError as e:
#         typing_task.cancel()
#         print(f"Caught an error: {e}")
#         default_response = (
#             "I'm sorry, there is no answer to that question in my knowledge base..."
#         )
#         print("Responding with: " + default_response)
#         await message.reply(default_response)


# @bot.event
# async def on_message(message):
#     if message.author.bot:
#         return
#     if bot.user in message.mentions:
#         async with message.channel.typing():
#             question = message.content.replace(
#                 f"<@!{bot.user.id}>", "").strip()
#             print("Answering question: ", question)
#             await ask(message, question)
#     else:
#         await bot.process_commands(message)


# bot.run(DISCORD_TOKEN)
