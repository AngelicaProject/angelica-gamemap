"""Call a tool of a running ReVa server from the command line, without
registering it as an MCP server; the standard library only.

    python tools/reva/call.py --list
    python tools/reva/call.py get-decompilation programPath=ffxiv_dx11.exe functionNameOrAddress=camera.camera.set_distance

Arguments are name=value; a value that parses as JSON (a number, true,
false, a list) is passed as that, anything else as text. `programPath` is
the program's path in the project; the leading `/` may be left out, which
keeps shells such as Git Bash from turning it into a Windows path. Prints the tool's
text result, or its error, and exits with 1 on an error.
"""
import argparse
import json
import sys
import urllib.request

URL = "http://127.0.0.1:8080/mcp/message"


def post(message: dict, session: str | None) -> tuple[dict | None, str | None]:
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if session:
        headers["Mcp-Session-Id"] = session
    request = urllib.request.Request(URL, json.dumps(message).encode(), headers)
    with urllib.request.urlopen(request, timeout=600) as response:
        session = response.headers.get("Mcp-Session-Id", session)
        body = response.read().decode("utf-8", "replace")
    if not body.strip():
        return None, session
    # A streamable HTTP answer is JSON, or server-sent events whose data
    # lines hold the JSON.
    if body.lstrip().startswith("{"):
        return json.loads(body), session
    data = [line[5:].strip() for line in body.splitlines() if line.startswith("data:")]
    return (json.loads(data[-1]) if data else None), session


def value(text: str):
    try:
        return json.loads(text)
    except ValueError:
        return text


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tool", nargs="?", help="the tool's name")
    parser.add_argument("arguments", nargs="*", help="name=value")
    parser.add_argument("--list", action="store_true", help="list the tools and their arguments")
    args = parser.parse_args()

    started, session = post(
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                    "clientInfo": {"name": "angelica-gamemap", "version": "1"}}},
        None,
    )
    if not started or "result" not in started:
        print(f"ReVa did not start a session: {started}", file=sys.stderr)
        return 1
    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, session)

    if args.list or not args.tool:
        listed, _ = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, session)
        for tool in listed["result"]["tools"]:
            schema = tool.get("inputSchema", {})
            required = set(schema.get("required", []))
            names = [f"{name}{'' if name in required else '?'}" for name in schema.get("properties", {})]
            print(f"{tool['name']}({', '.join(names)}): {tool.get('description', '').splitlines()[0] if tool.get('description') else ''}")
        return 0

    arguments = {}
    for pair in args.arguments:
        name, separator, text = pair.partition("=")
        if not separator:
            print(f"`{pair}` is not name=value", file=sys.stderr)
            return 2
        arguments[name] = value(text)
    if isinstance(arguments.get("programPath"), str) and not arguments["programPath"].startswith("/"):
        arguments["programPath"] = "/" + arguments["programPath"]
    answer, _ = post(
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": args.tool, "arguments": arguments}},
        session,
    )
    if answer is None or "error" in answer:
        print(json.dumps(answer.get("error") if answer else "no answer"), file=sys.stderr)
        return 1
    result = answer["result"]
    for part in result.get("content", []):
        print(part.get("text", json.dumps(part)))
    return 1 if result.get("isError") else 0


if __name__ == "__main__":
    sys.exit(main())
