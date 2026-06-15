"""Windows desktop guide for human-led agentic GitHub workflows.

The app is intentionally conservative: it can launch trusted tools and copy
commands for the user, but every operating-system action is initiated by an
explicit button press. It does not read secrets, credential stores, SSH keys, or
private environment files, and it does not merge pull requests automatically.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
import shutil
import subprocess
import sys
import webbrowser


@dataclass(frozen=True)
class WorkflowStep:
    """A single guided step in the Windows onboarding workflow."""

    title: str
    goal: str
    human_action: str
    llm_action: str
    task_guidance: tuple[str, ...]
    screenshot_caption: str
    popup_title: str
    popup_message: str
    command: str | None = None
    url: str | None = None


WORKFLOW_STEPS: tuple[WorkflowStep, ...] = (
    WorkflowStep(
        title="1. Install GitHub access tools",
        goal="Prepare a Windows developer workstation with Git, GitHub CLI, and authenticated repository access so the user can safely clone, inspect, and contribute to company code.",
        human_action="Choose the organization-approved installers, complete the browser-based GitHub sign-in, and confirm the terminal shows the expected account before continuing.",
        llm_action="Explain why each tool is needed, translate installer prompts into plain language, and help the user verify that no tokens or secrets are pasted into the guide.",
        task_guidance=(
            "Copy/paste approach: copy the command template, run it in PowerShell, and complete the GitHub browser authentication prompt.",
            "Trainer-led demo: the trainer opens the GitHub CLI download page, narrates the installer choices, and demonstrates the login flow with a training account.",
            "Confirm access by running `gh auth status` and asking the LLM to explain any warning before moving to the next lesson.",
        ),
        screenshot_caption="a PowerShell window shows `gh auth login --web --git-protocol https`, with a browser sign-in prompt beside it.",
        popup_title="Mock action: Open GitHub CLI setup",
        popup_message="This simulated pop-up would open the GitHub CLI documentation and copy the login command. The user still completes installation and authentication manually.",
        command="gh auth login --web --git-protocol https",
        url="https://cli.github.com/",
    ),
    WorkflowStep(
        title="2. Clone or open the target repository",
        goal="Place the target repository in a known local workspace and create a clearly named branch for a bounded guided change.",
        human_action="Select the correct repository, choose a local folder, edit the OWNER/REPO placeholder, and verify the active branch before any code changes are made.",
        llm_action="Recommend a branch name, identify the initial repo health checks, and remind the user to stop if the working tree is not clean.",
        task_guidance=(
            "Copy/paste approach: replace OWNER/REPO and REPO in the template, then run the edited command from the folder where work repositories are stored.",
            "Trainer-led demo: the trainer clones a sample repository, points out the branch indicator, and shows where `git status` confirms a clean start.",
            "Ask the LLM to summarize the repository purpose from README files before selecting a first task.",
        ),
        screenshot_caption="File Explorer is open to the workspace while the terminal shows a new `llm/workflow-change` branch and clean status.",
        popup_title="Mock action: Prepare clone command",
        popup_message="This simulated pop-up would copy an editable clone-and-branch template. It would not clone code until the user reviews and runs the command.",
        command="gh repo clone OWNER/REPO && cd REPO && git checkout -b llm/workflow-change",
    ),
    WorkflowStep(
        title="3. Install Claude CLI",
        goal="Make an approved command-line coding assistant available in the developer terminal without exposing credentials in logs, prompts, or screenshots.",
        human_action="Install Claude CLI through the approved path, run the version check, and confirm any authentication steps follow company policy.",
        llm_action="Help interpret installer output, explain expected CLI behavior, and suggest safe redactions if the user shares terminal output for troubleshooting.",
        task_guidance=(
            "Copy/paste approach: open the documentation, follow the approved install path, and run the version-check command after installation.",
            "Trainer-led demo: the trainer shows a successful version check and a failed command example, then demonstrates how to ask for help without sharing secrets.",
            "Record the installed CLI version in the training notes so later lessons use the same command expectations.",
        ),
        screenshot_caption="a terminal displays `claude --version` and a training note reminds users not to paste API keys into chat.",
        popup_title="Mock action: Open Claude CLI docs",
        popup_message="This simulated pop-up would open the Claude Code documentation and copy a harmless version-check command for the user to run.",
        command="claude --version",
        url="https://docs.anthropic.com/en/docs/claude-code/overview",
    ),
    WorkflowStep(
        title="4. Open Visual Studio IDE",
        goal="Bring the repository into Visual Studio so the user can inspect files, review source-control changes, and run local tests from a familiar interface.",
        human_action="Open the solution or folder, confirm the expected branch is active, and keep the Git Changes and test panels visible during the lesson.",
        llm_action="Suggest the smallest safe file set to inspect, identify likely tests, and explain how to compare proposed changes before accepting them.",
        task_guidance=(
            "Copy/paste approach: run the command template from the repository root if `devenv` is available on PATH.",
            "Trainer-led demo: the trainer opens the folder, pins Solution Explorer and Git Changes, and shows how to discard an unwanted local edit.",
            "Before editing, ask the LLM to list the files it expects to touch and compare that list with the IDE source-control panel.",
        ),
        screenshot_caption="Visual Studio shows Solution Explorer, Git Changes, and a terminal pane docked under the editor.",
        popup_title="Mock action: Launch Visual Studio",
        popup_message="This simulated pop-up would attempt to open Visual Studio for the current folder, or open the folder if Visual Studio is not on PATH.",
        command="devenv .",
    ),
    WorkflowStep(
        title="5. Run an agentic coding loop",
        goal="Use an LLM to propose, implement, test, and self-review one bounded code change while the human remains the decision maker at every checkpoint.",
        human_action="Approve the specific task, inspect the diff, run the recommended checks, decide whether to revise or stop, and reject any unrelated edits.",
        llm_action="Draft an implementation plan, make the patch, run checks when authorized, summarize risks, and perform a self-review focused on the requested scope.",
        task_guidance=(
            "Copy/paste approach: run the status-and-diff command, start the CLI assistant, and paste a task prompt that includes scope, files, and acceptance checks.",
            "Trainer-led demo: the trainer asks for a tiny documentation or test change, pauses at the diff, and shows how to request a narrower patch.",
            "Repeat the loop only when the working tree and test results are understood; otherwise ask the LLM for a rollback or cleanup plan.",
        ),
        screenshot_caption="a split terminal shows `git diff --stat`, the LLM task prompt, and a checklist for human approval.",
        popup_title="Mock action: Stage coding-loop prompt",
        popup_message="This simulated pop-up would copy a status command and bounded task prompt. It would not edit files or run checks without the user starting the CLI assistant.",
        command="git status && git diff --stat && claude",
    ),
    WorkflowStep(
        title="6. Create, review, and merge the pull request",
        goal="Turn the completed local change into a pull request with clear reviewer context, passing checks, and an explicit human-controlled merge decision.",
        human_action="Read the PR, validate checks, request or perform review, resolve comments, and approve merge only when the authorized reviewer is satisfied.",
        llm_action="Draft the PR title and body, summarize the final diff, note residual risks, and produce a review comment that is clearly separate from human approval.",
        task_guidance=(
            "Copy/paste approach: run the PR command after reviewing the final diff, then watch checks and paste the LLM review comment only if it is accurate.",
            "Trainer-led demo: the trainer creates a sample PR, points out required checks and reviewers, and demonstrates that merge is a separate human action.",
            "Ask the LLM to compare the PR description against the actual diff before requesting human review.",
        ),
        screenshot_caption="a browser PR page shows summary, checks, reviewers, and a highlighted reminder that merge requires human approval.",
        popup_title="Mock action: Prepare PR commands",
        popup_message="This simulated pop-up would copy PR creation and review commands. It would not push code, approve checks, or merge the pull request.",
        command="gh pr create --fill && gh pr checks --watch && gh pr review --comment --body \"LLM review completed; human approval still required.\"",
    ),
)


def build_workflow_summary() -> str:
    """Return a plain-text workflow summary for CLI and tests."""

    lines: list[str] = ["Windows Agentic Coding Guide", ""]
    for step in WORKFLOW_STEPS:
        lines.extend(
            [
                step.title,
                f"Goal: {step.goal}",
                f"Human: {step.human_action}",
                f"LLM: {step.llm_action}",
                "Task guidance:",
                *(f"- {item}" for item in step.task_guidance),
                f"Example screenshot: {step.screenshot_caption}",
                f"Mock pop-up: {step.popup_title} — {step.popup_message}",
            ]
        )
        if step.command:
            lines.append(f"Command: {step.command}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _launch_visual_studio() -> str:
    devenv = shutil.which("devenv")
    if devenv:
        subprocess.Popen([devenv, os.getcwd()])  # noqa: S603 - user-triggered local IDE launch
        return "Launched Visual Studio with the current folder."
    if sys.platform.startswith("win"):
        os.startfile(os.getcwd())  # type: ignore[attr-defined]  # noqa: S606 - user-triggered folder open
        return "Visual Studio was not on PATH; opened the current folder instead."
    return "Visual Studio launch is only available on Windows."


def run_app() -> int:
    """Start the Tkinter Windows guide."""

    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.title("Factory Fit Profiler - Windows Agentic Coding Guide")
    root.geometry("980x720")

    selected = tk.IntVar(value=0)
    title = tk.StringVar()
    goal = tk.StringVar()
    human = tk.StringVar()
    llm = tk.StringVar()
    guidance = tk.StringVar()
    screenshot = tk.StringVar()
    command = tk.StringVar()

    def draw_mock_screenshot(step: WorkflowStep) -> None:
        mock_canvas.delete("all")
        mock_canvas.create_rectangle(8, 8, 638, 174, fill="#f7f7f7", outline="#9a9a9a")
        mock_canvas.create_rectangle(8, 8, 638, 34, fill="#5b7f47", outline="#5b7f47")
        mock_canvas.create_text(22, 21, text=step.title, anchor="w", fill="white", font=("Segoe UI", 9, "bold"))
        mock_canvas.create_rectangle(26, 52, 310, 150, fill="#1e1e1e", outline="#444")
        mock_canvas.create_text(38, 70, text="> " + (step.command or "review checklist"), anchor="w", fill="#dcdcaa", font=("Consolas", 8), width=255)
        mock_canvas.create_rectangle(334, 52, 616, 150, fill="white", outline="#b0b0b0")
        mock_canvas.create_text(348, 70, text=step.screenshot_caption, anchor="nw", fill="#222", font=("Segoe UI", 8), width=250)

    def render() -> None:
        step = WORKFLOW_STEPS[selected.get()]
        title.set(step.title)
        goal.set(f"Goal: {step.goal}")
        human.set(f"Human action: {step.human_action}")
        llm.set(f"LLM action: {step.llm_action}")
        guidance.set("Task guidance:\n" + "\n".join(f"{idx}. {item}" for idx, item in enumerate(step.task_guidance, 1)))
        screenshot.set(step.screenshot_caption)
        command.set(step.command or "")
        draw_mock_screenshot(step)

    def copy_command() -> None:
        root.clipboard_clear()
        root.clipboard_append(command.get())
        messagebox.showinfo("Command copied", "The command template was copied to the clipboard.")

    def open_url() -> None:
        step = WORKFLOW_STEPS[selected.get()]
        if step.url:
            webbrowser.open(step.url)
        else:
            messagebox.showinfo("No URL", "This step does not have a URL to open.")

    def run_safe_action() -> None:
        step = WORKFLOW_STEPS[selected.get()]
        messagebox.showinfo(step.popup_title, step.popup_message)
        if "Visual Studio" in step.title:
            messagebox.showinfo("Safe action", _launch_visual_studio())
        elif step.url:
            webbrowser.open(step.url)
            copy_command()
        else:
            copy_command()

    sidebar = tk.Frame(root, padx=10, pady=10)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    for idx, step in enumerate(WORKFLOW_STEPS):
        tk.Radiobutton(sidebar, text=step.title, variable=selected, value=idx, command=render, anchor="w", justify="left").pack(fill=tk.X)

    content = tk.Frame(root, padx=16, pady=16)
    content.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
    tk.Label(content, textvariable=title, font=("Segoe UI", 16, "bold"), anchor="w").pack(fill=tk.X)
    for variable in (goal, human, llm, guidance):
        tk.Message(content, textvariable=variable, width=700, font=("Segoe UI", 10), anchor="w").pack(fill=tk.X, pady=4)
    tk.Label(content, text="Example screenshot", anchor="w", font=("Segoe UI", 10, "bold")).pack(fill=tk.X, pady=(12, 2))
    mock_canvas = tk.Canvas(content, width=650, height=182, bg="white", highlightthickness=0)
    mock_canvas.pack(fill=tk.X)
    tk.Message(content, textvariable=screenshot, width=700, font=("Segoe UI", 9, "italic")).pack(fill=tk.X, pady=4)
    tk.Label(content, text="Command template", anchor="w", font=("Segoe UI", 10, "bold")).pack(fill=tk.X, pady=(8, 0))
    tk.Entry(content, textvariable=command).pack(fill=tk.X, pady=6)
    buttons = tk.Frame(content)
    buttons.pack(fill=tk.X, pady=8)
    tk.Button(buttons, text="Copy command", command=copy_command).pack(side=tk.LEFT, padx=4)
    tk.Button(buttons, text="Open documentation", command=open_url).pack(side=tk.LEFT, padx=4)
    tk.Button(buttons, text="Show mock pop-up / run user action", command=run_safe_action).pack(side=tk.LEFT, padx=4)
    tk.Message(
        content,
        width=700,
        text="Safety: this guide only performs user-triggered OS actions. It never reads secrets, pushes code, merges PRs, or controls the desktop without an explicit click.",
        fg="darkred",
    ).pack(fill=tk.X, pady=16)

    render()
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(run_app())
