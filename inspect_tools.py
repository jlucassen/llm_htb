from inspect_ai.tool import tool
from inspect_ai.util import store

@tool
def check_answer():
    async def execute(question_index: int, answer: str):
        """
            Check the answer for a question.

        Args:
            question_index: The index of the question to check.
            answer: The answer to check.

        Returns:
            The result of the check.
        """
        return store().get("htb").check_answer(question_index, answer)

    return execute