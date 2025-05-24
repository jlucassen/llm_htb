from inspect_ai import Task, task
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import solver, use_tools, generate
from inspect_ai.tool import bash, python

from inspect_dataset import htb_machines_dataset
from htb import HTBMachine
from inspect_tools import check_answer
CMD_TIMEOUT = 180

@solver
def setup(machine_name: str): 
    async def solve(state, _generate):
        # some commands can't be run in Dockerfile, so we need to run them after container start
        await bash(CMD_TIMEOUT)("./setup.sh")
        # create a webdriver to interface with the htb machine and put it in the Store for tools to call
        htb = HTBMachine(machine_name)
        state.store.set("htb", htb)
        return state
    return solve

@task
def htb_machines_task(machine_name: str):
    return Task(
        dataset=htb_machines_dataset,
        solver=[use_tools([bash(CMD_TIMEOUT),
                           python(CMD_TIMEOUT),
                           check_answer()]),
                generate()],
        scorer=model_graded_fact(),
        sandbox="docker",
        setup=setup(machine_name)
    )