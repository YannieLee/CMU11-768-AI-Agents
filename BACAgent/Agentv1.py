## miniAgent: 读取文件 tests/unit/Service/BoardServiceTest.php 从中找到 authorization invariant

import os
import json
import subprocess
from openai import OpenAI, DefaultHttpxClient

class Agent:
    def __init__(
        self,
        model: str | None = None,
        path: str | None = None
        ):
        self.model = model or "deepseek-flash"
        self.path = path or "./deck/tests/unit/Service/BoardServiceTest.php"
        self.messages = []
        proxy_url = os.environ.get("DEEPSEEK_PROXY_URL")
        if not proxy_url:
            # WSL NAT 的默认网关是 Windows 地址；当前代理端口为 7800。
            route = subprocess.check_output(
                ["ip", "-4", "route", "show", "default"], text=True
            )
            windows_host = route.split()[2]
            proxy_url = f"http://{windows_host}:7800"
        self.client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com",
            http_client=DefaultHttpxClient(proxy=proxy_url),
        )

    
    def build_prompt(self):
         self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a security analysis agent. "
                    "Use the available tools to inspect unit tests."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Read {self.path} and identify authorization-related "
                    "candidate invariants supported by the tests. "
                    "For each invariant, provide evidence from the test."
                )
            }
        ]

    def run(self):
        self.build_prompt()

        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=tools
            )

            message = response.choices[0].message

            # LLM 没有调用 tool，说明它准备给最终答案了
            if not message.tool_calls:
                print(message.content)
                break

            # 保存 assistant 的 tool call
            self.messages.append(message)

             # 执行 tool
            for tool_call in message.tool_calls:
                if tool_call.function.name == "read_file":

                    args = json.loads(tool_call.function.arguments)
                    result = self.read_file(args["path"])

                    # 把 observation 放回 state
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
            

    def read_file(self, path:str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the content of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to read"
                    }
                },
                "required": ["path"]
            }
        }
    }
]

if __name__ == "__main__":
    agent = Agent()
    agent.run()
