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
    def spin(self, user_skills: str) -> str:
        def pick_task() -> str:
            prompt = (
                f"You are a GenLayer community task advisor. "
                f"Given this user's skills and background: '{user_skills}', "
                f"from this task list: {list(self.tasks)}, "
                f"choose the ONE task that is most suitable and challenging for this user. "
                f"Return only the task name, nothing else."
            )
            return gl.exec_prompt(prompt)

        result = gl.eq_principle.prompt_comparative(
            pick_task,
            principle="The result must be one of the tasks from the list, chosen based on the user's skills"
        )
        self.last_result = result
        self.spin_history.append(result)
        return result

    @gl.public.write
    def validate_completion(self, task: str, proof: str) -> str:
        def check() -> str:
            prompt = (
                f"A user claims to have completed this GenLayer community task: '{task}'. "
                f"Their submitted proof or description: '{proof}'. "
                f"Based on the proof, did they genuinely complete the task? "
                f"Answer only YES or NO, followed by one sentence of reasoning."
            )
            return gl.exec_prompt(prompt)

        result = gl.eq_principle.prompt_comparative(
            check,
            principle="Answer must start with YES or NO based on whether the proof demonstrates task completion"
        )
        self.spin_history.append(f"Validation for '{task}': {result}")
        return result

    @gl.public.view
    def get_last_result(self) -> str:
        return
