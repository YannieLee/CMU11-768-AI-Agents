# CMU11-768-AI-Agents

Coursework and a minimal agent for reading authorization-related unit tests.

Clone with `git clone --recurse-submodules` to download Deck and the chess app.
For an existing checkout, run `git submodule update --init --recursive`.

`assignment/assignment-1` contains a source snapshot of the course starter and
local work in progress. Some exercise implementations are intentionally unfinished.

To run the mini agent in the current WSL setup:

```bash
cd BACAgent
python3 -m venv BACAgent
source BACAgent/bin/activate
python -m pip install openai
export DEEPSEEK_API_KEY="your-api-key"
python Agentv1.py
```

The agent defaults to the Windows host's proxy on port 7800 in WSL NAT mode.
Set `DEEPSEEK_PROXY_URL` to override the proxy URL. The Windows proxy must be
running and reachable from WSL. Virtual environments and local secrets are ignored.
