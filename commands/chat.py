import discord
from llama_index import VectorStoreIndex, SimpleDirectoryReader


async def chat(interaction: discord.Interaction, question: str):
    documents = SimpleDirectoryReader(
        "resources/a_brief_history_of_kazar.txt").load_data()
    index = VectorStoreIndex.from_documents(documents)

    query_engine = index.as_query_engine()
    response = query_engine.query(question)

    await interaction.response.send_message(response)
