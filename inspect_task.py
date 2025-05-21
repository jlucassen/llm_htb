from inspect_ai import Task, task
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import solver, use_tools, generate
from inspect_ai.tool import bash, python

from inspect_dataset import htb_machines_dataset

CMD_TIMEOUT = 180

@solver
def connect_vpn(): # some commands can't be run in Dockerfile, so we need to run them after container start
    async def solve(state, _generate):
        await bash(CMD_TIMEOUT)("./setup.sh")
        return state
    return solve

@task
def htb_machines_task():
    return Task(
        dataset=htb_machines_dataset,
        solver=[use_tools([bash(CMD_TIMEOUT),
                           python(CMD_TIMEOUT)]),
                generate()],
        scorer=model_graded_fact(),
        sandbox="docker",
        setup=connect_vpn()
    )