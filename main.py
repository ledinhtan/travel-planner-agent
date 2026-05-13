import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from starlette.responses import JSONResponse
from pathlib import Path 
from utils.save_to_document import save_travel_plan 
from exception.exceptionhandling import CustomException
from logger.logging import logging

logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("Create the folder to store workflow graph")
docs_dir = Path("./docs")
docs_dir.mkdir(parents=True, exist_ok=True)
logger.info(f"✅ Workflow graph will be saved to: {docs_dir.absolute()}")

logger.info("Create the folder to store travel plans")
travel_plan_dir = Path("./travel_plans")
travel_plan_dir.mkdir(parents=True, exist_ok=True)
logger.info(f"✅ Travel plans will be saved to: {travel_plan_dir.absolute()}")

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open(docs_dir / "my_graph.png", "wb") as f:
            f.write(png_graph)
        logger.info(f"✅ Graph saved as 'workflow_graph.png' in {docs_dir}")

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        messages={"messages": [query.query]}

        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)

        # Save travel plans
        saved_path = save_travel_plan(final_output, directory=str(travel_plan_dir))
        if saved_path:
            logger.info(f"✅ Travel plan saved to: {saved_path}")
        else:
            logger.warning(f"⚠️ Failed to save travel plan")
        
        return {"answer": final_output}
    except Exception as e:
        logger.error(CustomException(e, sys))
        return JSONResponse(status_code=500, content={"error": str(e)}) 