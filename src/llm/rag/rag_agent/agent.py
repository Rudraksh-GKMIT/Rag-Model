from src.llm.rag.constant import RAGConstant
from src.llm.rag.rag_agent.prompt import SYSTEM_PROMPT
from src.llm.agent_core.agent import Agent
from src.llm.rag.rag_agent.tools.make_retrieval import make_retrieval


class RagAgent(Agent):
    def __init__(
        self,
        model: str = RAGConstant.MODEL,
        temperature: float = RAGConstant.TEMPERATURE,
        max_iteration: int = RAGConstant.DEFAULT_MAX_ITERATION,
    ):
        super().__init__(
            system_prompt=SYSTEM_PROMPT,
            model=model,
            temperature=temperature,
            max_iteration=max_iteration,
        )
        self.add_tool(make_retrieval())

    def run(self, chat_history, user_message):
        if user_message == "":
            raise ValueError("Looks like no input was entered")
        user_input = {"role": "user", "content": user_message}
        chat_history.append(user_input)
        return self.invoke(chat_history)

