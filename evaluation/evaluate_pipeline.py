import json
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset
from services.retrieval.hybrid_engine import HybridQueryEngine

load_dotenv()

# 1. Setup Azure Judges
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_GPT4OMINI_DEPLOYMENT"),
    openai_api_version=os.getenv("AZURE_OPENAI_GPT4OMINI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_GPT4OMINI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_GPT4OMINI_API_KEY")
)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT"),
    openai_api_version=os.getenv("AZURE_OPENAI_EMB_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_EMB_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_EMB_API_KEY")
)

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "test_questions.json")

# 2. Prepare Data for RAGAS
def run_evaluation():
    engine = HybridQueryEngine()
    with open(json_path, "r") as f:
        test_set = json.load(f)

    data = {"question": [], "answer": [], "contexts": [], "ground_truth": []}

    for item in test_set:
        print(f"Testing: {item['question']}")
        result = engine.query(item['question'])
        
        data["question"].append(item["question"])
        data["answer"].append(result["answer"])
        # Combined vector and graph chunks
        data["contexts"].append(result["vector_chunks"] + result["graph_chunks"])
        data["ground_truth"].append(item["ground_truth"])

    # 3. Evaluate
    dataset = Dataset.from_dict(data)
    results = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness(),      # Added () to initialize
            answer_relevancy(),  # Added ()
            context_precision(), # Added ()
            context_recall()     # Added ()
        ],
        llm=llm,
        embeddings=embeddings
    )
    
    print(results)
    results.to_pandas().to_csv("rag_evaluation_results.csv")
    engine.close()

if __name__ == "__main__":
    run_evaluation()