from inspect_ai import Task, task
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import use_tools, generate
from inspect_ai.tool import bash, python

from inspect_dataset import htb_machines_dataset

CMD_TIMEOUT = 180

@task
def htb_machines_task():
    return Task(
        dataset=htb_machines_dataset,
        solver=[use_tools([bash(CMD_TIMEOUT),
                           python(CMD_TIMEOUT)]),
                generate()],
        scorer=model_graded_fact(),
        sandbox="docker"
    )