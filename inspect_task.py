from inspect_ai import Task, task
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import solver, use_tools, generate
from inspect_ai.tool import bash, python
from inspect_ai.scorer import scorer, accuracy, Score

from inspect_dataset import htb_machines_dataset
from htb import HTBMachine
from inspect_tools import check_answer, get_task

CMD_TIMEOUT = 180

@solver
def setup(machine_name: str): 
    async def solve(state, _generate):
        # some commands can't be run in Dockerfile, so we need to run them after container start
        await bash(CMD_TIMEOUT)("./setup.sh")
        # create a webdriver to interface with the htb machine and put it in the Store for tools to call
        htb = HTBMachine(machine_name)
        state.store.set("htb", htb)
        # initialize the score counter
        state.store.set("score", [0] * htb.num_questions())
        return state
    return solve

@solver
def cleanup():
    async def cleanup(state, _generate):
        state.store.get("htb").stop_machine()
        return state
    return cleanup

@scorer(metrics=[accuracy()])
def guided_scorer():
    async def score(state, _generate):
        completions = state.store.get("score")
        return Score(value=sum(completions)/len(completions))
    return score

@task
def htb_machines_task(machine_name: str):
    return Task(
        dataset=htb_machines_dataset,
        solver=[use_tools([bash(CMD_TIMEOUT),
                           python(CMD_TIMEOUT),
                           check_answer(),
                           get_task()]),
                generate()],
        scorer=guided_scorer(),
        sandbox="docker",
        setup=setup(machine_name),
        message_limit=100,
        cleanup=cleanup
    )