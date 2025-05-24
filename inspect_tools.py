from inspect_ai.tool import tool
from inspect_ai.util import store

@tool
def check_answer():
    async def execute(task_index: int, answer: str):
        """
        Check the answer for a given task index.

        Args:
            task_index: The index of the task to check.
            answer: The answer to check.

        Returns:
            True if the answer is correct, False if the answer is incorrect.
        """
        result = store().get("htb").check_answer(task_index, answer)
        if result:
            store().get("score")[task_index] = 1
        return result

    return execute

@tool
def get_task():
    async def execute(task_index: int):
        """
        Get the task for a given task index.

        Args:
            task_index: The index of the task to get.

        Returns:
            The task.
        """
        return store().get("htb").get_question(task_index)
    return execute