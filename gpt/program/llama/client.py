from llama_index.text_splitter import SentenceSplitter
import json
from dotenv import load_dotenv
from llama_index import (
    VectorStoreIndex,
    LLMPredictor,
    OpenAIEmbedding,
    PromptHelper,
    StorageContext,
    download_loader,
    ServiceContext,
)

from llama_index.logger import LlamaLogger
from llama_index.callbacks import CallbackManager

from langchain.chat_models import ChatOpenAI
from pathlib import Path
import os
load_dotenv()


ingestation_path = Path("../data")


class LlamaClient:

    def __init__(self):
        self.OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
        self.THREAD_COUNT = os.getenv("NUMEXPR_MAX_THREADS", "16")

    def create_llm_predictor(self, temperature, model, max_tokens):
        kind = ChatOpenAI(temperature=temperature,
                          model=model, max_tokens=max_tokens)
        return LLMPredictor(kind)

    def print_file_names(self):
        for md_file in Path(ingestation_path).glob("**/*.md"):
            print(md_file)

    def create_sentence_splitter(self, chunk_size, chunk_overlap):
        return SentenceSplitter(chunk_size, chunk_overlap)

    def create_prompt_helper(
        self, context_window, num_output, chunk_overlap_ratio, chunk_size_limit
    ):
        return PromptHelper(
            context_window,
            num_output,
            chunk_overlap_ratio,
            chunk_size_limit
        )

    def create_service_context(
        self, llm_predictor, text_splitter, prompt_helper
    ):
        # embed = OpenAIEmbedding()
        # logger = LlamaLogger()
        # callback = CallbackManager()
        # return ServiceContext(
        #     llm_predictor,
        #     embed,
        #     text_splitter,
        #     prompt_helper,
        #     logger,
        #     callback
        # )

        # Fix this initialization!

        return ServiceContext.from_defaults()

    def load_json_file(self, file_name):
        with open(file_name) as file:
            return json.load(file)

    def create_vector_store_indeces(
        self, file_index, vector_indices, service_context, index_summaries
    ):
        try:
            MarkdownReader = download_loader("MarkdownReader")
            loader = MarkdownReader()

            documents = {}

            for md_file in Path(ingestation_path).glob("**/*.md"):
                file_name = md_file.stem
                metadata = file_index.get(file_name)
                if metadata is not None:

                    documents[file_name] = loader.load_data(file=md_file)

                    storage_context = StorageContext.from_defaults()

                    vector_indices[file_name] = VectorStoreIndex.from_documents(
                        documents[file_name],
                        storage_context=storage_context,
                        service_context=service_context
                    )

                    vector_indices[file_name].set_index_id(file_name)

                    storage_context.persist(
                        persist_dir=f"../storage/{file_name}")

                    index_summaries[file_name] = (
                        "This index contains information about " +
                        metadata["description"]
                    )

            return vector_indices, index_summaries

        except Exception as e:
            print("Error while creating vector store indeces: ", e)


def create_custom_query_engines(vector_indices, decompose_transform, serviceContext, graph):
    custom_query_engines = {}

    for index in vector_indices.values():
        query_engine = index.as_query_engine(service_context=serviceContext)
        query_engine = TransformQueryEngine(
            query_engine,
            query_transform=decompose_transform,
            transform_extra_info={"index_summary": index.index_struct.summary},
        )
        custom_query_engines[index.index_id] = query_engine

    custom_query_engines[graph.root_id] = graph.root_index.as_query_engine(
        response_mode="tree_summarize",
        service_context=serviceContext,
        verbose=True,
    )

    return custom_query_engines
