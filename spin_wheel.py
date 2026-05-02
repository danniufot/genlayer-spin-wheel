# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class SpinWheel(gl.Contract):
    tasks: DynArray[str]
    spin_history: DynArray[str]
    last_result: str

    def __init__(self, tasks: list):
        self.tasks = tasks
        self.spin_history = []
        self.last_result = ""

    @gl.public.write
    def spin(self) -> str:
        def pick_task() -> str:
            prompt = (
                f"You are a random task selector. "
                f"From this list: {list(self.tasks)}, "
                f"pick exactly ONE task at random and return only that task name, nothing else."
            )
            return gl.exec_prompt(prompt)

        result = gl.eq_principle.prompt_comparative(
            pick_task,
            principle="The result must be one of the tasks from the list"
        )
        self.last_result = result
        self.spin_history.append(result)
        return result

    @gl.public.view
    def get_last_result(self) -> str:
        return self.last_result

    @gl.public.view
    def get_history(self) -> list:
        return list(self.spin_history)

    @gl.public.view
    def get_tasks(self) -> list:
        return list(self.tasks)
