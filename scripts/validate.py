#!/usr/bin/env python3
"""Validate the repository against the skill contract in docs/architecture.md.

Usage: python scripts/validate.py
Requires: PyYAML.
Exit code 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"
README = ROOT / "README.md"

CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_MANIFESTS = (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "plugin.json")
AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AGENT_PLUGINS_KEYS = {
    "$schema", "name", "version", "description", "author",
    "homepage", "repository", "license", "keywords", "extensions",
}

SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
# Host extensions that other hosts ignore. Each one is documented in docs/architecture.md.
HOST_KEYS = {"disable-model-invocation"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SKILL_PREFIX = "krci-"
ROUTER_SKILL = "krci-overview"
ACCESS_VALUES = {"read-only", "mutating"}
ROLE_VALUES = {"ba", "po", "pm", "dev", "qa", "devops"}
STAGE_VALUES = {"plan", "code", "build", "test", "deploy", "operate"}
ALL = "all"
MAX_BODY_LINES = 500
MAX_DESCRIPTION = 400
MAX_ROUTER_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_AGENT_LINES = 40

FENCE_RE = re.compile(r"^```[^\n]*\n(.*?)^```", re.S | re.M)
LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")

# Global flags between a tool and its subcommand, with or without a value: `kubectl -n prod --context c delete`.
_FLAGS = r"(?:-{1,2}[\w.-]+(?:=\S+)?\s+(?:(?!-)\S+\s+)?)*"
# A preview or help request on the same line changes nothing.
_NO_PREVIEW = r"(?![^\n]*\s(?:--dry-run|--help|-h)(?:[=\s]|$))"


def _command(tool: str, *words: str) -> str:
    return r"\b" + tool + "".join(r"\s+" + _FLAGS + word for word in words) + r"\b" + _NO_PREVIEW


# Commands that change state outside the working tree. Checked in fenced blocks and scripts of read-only skills.
MUTATING = [
    _command("kubectl", r"(?:apply|create|delete|patch|edit|replace|scale|annotate|label|exec|cp|set|debug|cordon|uncordon|drain|taint)"),
    _command("kubectl", "rollout", r"(?:restart|undo|pause|resume)"),
    _command("kubectl", "certificate", r"(?:approve|deny)"),
    _command("krci", r"(?:pipelinerun|run)", "start"),
    _command("krci", r"(?:project|proj)", "build"),
    _command("tkn", r"\S+", r"(?:start|delete|cancel)"),
    _command("helm", r"(?:install|upgrade|rollback|uninstall|delete)"),
    _command("argocd", "app", r"(?:sync|rollback|delete|set|patch|terminate-op)"),
    _command("git", "push"),
    _command("gh", "pr", r"(?:create|merge|close|edit|review)"),
    _command("gh", "release", r"(?:create|delete|edit|upload)"),
    _command("gh", "workflow", "run"),
    _command("glab", "mr", r"(?:create|merge|close|update|approve)"),
    _command("glab", "release", r"(?:create|delete)"),
]
# Commands that print secret values. Checked in fenced blocks and scripts of every skill.
SECRET_DUMP = [
    r"\bkubectl\b[^\n|]*\bget\s+secrets?\b[^\n|]*(?:-o|--output)[=\s]*(?:yaml|json)\b(?![^\n]*\|\s*jq[^\n]*\bkeys\b)",
    r"\bkubectl\b[^\n|]*\bget\s+secrets?\b[^\n|]*(?:-o|--output)[=\s]*(?:go-template|template|custom-columns)\S*",
    r"\bkubectl\b[^\n|]*\bget\s+secrets?\b[^\n|]*--template\b",
    r"\bkubectl\b[^\n|]*\bget\s+secrets?\b[^\n]*jsonpath=[^\n]*\.data\b(?![^\n]*\|\s*jq[^\n]*\bkeys\b)",
    r"\bkubectl\s+view-secret\b",
    r"\bbase64\s+(?:-d|--decode|-D)\b(?![^\n]*\|\s*jq[^\n]*\bkeys\b)",
]

errors: list[str] = []


@dataclass
class Skill:
    name: str
    path: Path
    description: str
    roles: set[str] = field(default_factory=set)
    user_invoked: bool = False


@dataclass
class Plugin:
    path: Path
    version: str | None = None
    skills: dict[str, Skill] = field(default_factory=dict)


def fail(path: Path | str, message: str) -> None:
    location = path.relative_to(ROOT).as_posix() if isinstance(path, Path) else path
    errors.append(f"{location}: {message}")


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        fail(path, "file is missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(path, f"invalid JSON: {exc}")
        return None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def split_frontmatter(path: Path) -> tuple[dict | None, str]:
    text = read_text(path)
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not match:
        fail(path, "missing YAML frontmatter")
        return None, text
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(path, f"invalid YAML frontmatter: {exc}")
        return None, match.group(2)
    if not isinstance(meta, dict):
        fail(path, "frontmatter is not a mapping")
        return None, match.group(2)
    return meta, match.group(2)


def join_continuations(code: str) -> str:
    return re.sub(r"\\\n\s*", " ", code)


def find_mutating(code: str) -> list[str]:
    code = join_continuations(code)
    return [m.group(0).strip() for pattern in MUTATING for m in re.finditer(pattern, code)]


def find_secret_dumps(code: str) -> list[str]:
    code = join_continuations(code)
    return [m.group(0).strip() for pattern in SECRET_DUMP for m in re.finditer(pattern, code)]


def parse_list(value: str, allowed: set[str]) -> tuple[set[str], list[str]]:
    """Parse a comma-separated metadata value. Returns the values and the problems found."""
    items = [item.strip() for item in value.split(",") if item.strip()]
    problems = []
    if not items:
        problems.append("is empty")
    if ALL in items and len(items) > 1:
        problems.append(f"'{ALL}' cannot be combined with other values")
    unknown = sorted(set(items) - allowed - {ALL})
    if unknown:
        problems.append(f"has unknown values {unknown}, allowed: {sorted(allowed)} or '{ALL}'")
    if len(items) != len(set(items)):
        problems.append("repeats a value")
    return set(items), problems


def check_plugin_manifests(plugin: Plugin) -> None:
    versions = {}
    for rel in PLUGIN_MANIFESTS:
        manifest = load_json(plugin.path / rel)
        if manifest is None:
            continue
        if manifest.get("name") != plugin.path.name:
            fail(plugin.path / rel, f"name must be '{plugin.path.name}'")
        version = manifest.get("version", "")
        if not SEMVER_RE.match(version):
            fail(plugin.path / rel, f"version '{version}' is not MAJOR.MINOR.PATCH")
        versions[rel] = version
        if rel == "plugin.json":
            if manifest.get("$schema") != AGENT_PLUGINS_SCHEMA:
                fail(plugin.path / rel, f"$schema must be {AGENT_PLUGINS_SCHEMA}")
            unknown = set(manifest) - AGENT_PLUGINS_KEYS
            if unknown:
                fail(plugin.path / rel, f"keys not allowed by Agent Plugins 1.0.0: {sorted(unknown)}")
        if rel == ".codex-plugin/plugin.json" and manifest.get("skills") != "./skills/":
            fail(plugin.path / rel, "skills must be './skills/'")
    if len(set(versions.values())) > 1:
        fail(plugin.path, f"manifest versions differ: {versions}")
    plugin.version = versions.get(".claude-plugin/plugin.json")


def check_bundle(entry: dict, plugins: dict[str, Plugin]) -> None:
    """A bundle installs a subset of one plugin's skills from the marketplace root."""
    name = entry.get("name", "")
    where = f"{CLAUDE_MARKETPLACE.relative_to(ROOT).as_posix()}: bundle '{name}'"
    owner = next((p for p in plugins.values() if name.startswith(f"{p.path.name}-")), None)
    if owner is None:
        fail(where, f"name must start with '<plugin>-', plugins: {sorted(plugins)}")
        return
    if entry.get("strict") is not False:
        fail(where, "must set \"strict\": false, the marketplace entry is its manifest")
    if entry.get("version") != owner.version:
        fail(where, f"version must equal the '{owner.path.name}' plugin version {owner.version}")
    prefix = f"./plugins/{owner.path.name}/skills/"
    listed = set()
    for rel in entry.get("skills") or []:
        skill_name = rel[len(prefix):].rstrip("/") if rel.startswith(prefix) else None
        if skill_name not in owner.skills:
            fail(where, f"skill path '{rel}' must be '{prefix}<skill>' of an existing skill")
            continue
        listed.add(skill_name)
    if not listed:
        fail(where, "lists no skills")
    elif ROUTER_SKILL in owner.skills and ROUTER_SKILL not in listed:
        fail(where, f"must include the router '{ROUTER_SKILL}'")


def check_marketplaces(plugins: dict[str, Plugin]) -> None:
    claude = load_json(CLAUDE_MARKETPLACE)
    codex = load_json(CODEX_MARKETPLACE)
    if claude is None or codex is None:
        return
    if claude.get("name") != codex.get("name"):
        fail(CODEX_MARKETPLACE, "marketplace name differs from .claude-plugin/marketplace.json")

    listed = {}
    for entry in claude.get("plugins", []):
        source = entry.get("source")
        if source == "./":
            check_bundle(entry, plugins)
            continue
        if entry.get("skills") is not None:
            # A plugin directory has its own manifest. A second component list fails at load time.
            fail(CLAUDE_MARKETPLACE, f"plugin '{entry.get('name')}' has a source directory and must not list skills")
        listed[entry.get("name")] = source
    codex_listed = {}
    for entry in codex.get("plugins", []):
        codex_listed[entry.get("name")] = (entry.get("source") or {}).get("path")

    for name in plugins:
        expected = f"./plugins/{name}"
        if listed.get(name) != expected:
            fail(CLAUDE_MARKETPLACE, f"plugin '{name}' must be listed with source '{expected}'")
        if codex_listed.get(name) != expected:
            fail(CODEX_MARKETPLACE, f"plugin '{name}' must be listed with path '{expected}'")
    for name in listed:
        if name not in plugins:
            fail(CLAUDE_MARKETPLACE, f"plugin '{name}' is listed but plugins/{name}/ does not exist")
    for name in codex_listed:
        if name not in plugins:
            fail(CODEX_MARKETPLACE, f"plugin '{name}' is listed but plugins/{name}/ does not exist")


def check_links(path: Path, text: str, skill_dir: Path) -> None:
    for target in LINK_RE.findall(text):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            fail(path, f"broken link: {target}")
        elif skill_dir.resolve() not in resolved.parents and resolved != skill_dir.resolve():
            fail(path, f"link leaves the skill directory: {target}")


def check_code(path: Path, code: str, read_only: bool, where: str) -> None:
    for hit in find_secret_dumps(code):
        fail(path, f"{where} prints secret values: '{hit}'")
    if read_only:
        for hit in find_mutating(code):
            fail(path, f"read-only skill has a state-changing command in {where}: '{hit}'")


def check_skill(skill_dir: Path) -> Skill | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(skill_dir, "SKILL.md is missing")
        return None
    meta, body = split_frontmatter(skill_md)
    if meta is None:
        return None

    unknown = set(meta) - SPEC_KEYS - HOST_KEYS
    if unknown:
        fail(skill_md, f"frontmatter keys outside the Agent Skills spec: {sorted(unknown)}")

    name = str(meta.get("name", ""))
    if name != skill_dir.name:
        fail(skill_md, f"name '{name}' must equal the directory name '{skill_dir.name}'")
    if not NAME_RE.match(name) or len(name) > 64:
        fail(skill_md, "name must be lowercase letters, digits, single hyphens, at most 64 characters")
    if not name.startswith(SKILL_PREFIX):
        fail(skill_md, f"name must start with '{SKILL_PREFIX}'")

    user_invoked = meta.get("disable-model-invocation") is True
    if "disable-model-invocation" in meta and not isinstance(meta["disable-model-invocation"], bool):
        fail(skill_md, "disable-model-invocation must be true or false")

    description = str(meta.get("description", "")).strip()
    limit = MAX_ROUTER_DESCRIPTION if name == ROUTER_SKILL else MAX_DESCRIPTION
    if not 1 <= len(description) <= limit:
        fail(skill_md, f"description must be 1 to {limit} characters, got {len(description)}")
    if not user_invoked and "use when" not in description.lower():
        fail(skill_md, "description must state triggers with 'Use when'")

    if meta.get("license") != "Apache-2.0":
        fail(skill_md, "license must be Apache-2.0")
    compatibility = str(meta.get("compatibility", "")).strip()
    if not 1 <= len(compatibility) <= MAX_COMPATIBILITY:
        fail(skill_md, f"compatibility is required, at most {MAX_COMPATIBILITY} characters")

    metadata = meta.get("metadata") or {}
    if not isinstance(metadata, dict) or any(not isinstance(v, str) for v in metadata.values()):
        fail(skill_md, "metadata must map strings to strings")
        metadata = {}
    access = metadata.get("access")
    if access not in ACCESS_VALUES:
        fail(skill_md, f"metadata.access must be one of {sorted(ACCESS_VALUES)}")
    roles, problems = parse_list(metadata.get("roles", ""), ROLE_VALUES)
    for problem in problems:
        fail(skill_md, f"metadata.roles {problem}")
    _, problems = parse_list(metadata.get("stage", ""), STAGE_VALUES)
    for problem in problems:
        fail(skill_md, f"metadata.stage {problem}")

    if len(body.splitlines()) > MAX_BODY_LINES:
        fail(skill_md, f"body exceeds {MAX_BODY_LINES} lines, move depth into references/")
    if name != ROUTER_SKILL and f"`{ROUTER_SKILL}`" not in body:
        fail(skill_md, f"body must name `{ROUTER_SKILL}`, the skill that carries vocabulary and the safety contract")

    references = skill_dir / "references"
    if references.is_dir():
        for child in references.iterdir():
            if child.is_dir():
                fail(child, "references/ must stay one level deep")

    read_only = access == "read-only"
    for path in sorted(skill_dir.rglob("*")):
        if path.is_symlink():
            fail(path, "symlinks are not allowed")
            continue
        if not path.is_file():
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        if path.suffix == ".md":
            check_links(path, text, skill_dir)
            check_code(path, "\n".join(FENCE_RE.findall(text)), read_only, "a fenced block")
        else:
            check_code(path, text, read_only, "a script")

    if access == "mutating" and not re.search(r"^##\s+Confirmation gate\s*$", body, re.M):
        fail(skill_md, "mutating skill must have a '## Confirmation gate' section")
    return Skill(name=name, path=skill_dir, description=description, roles=roles, user_invoked=user_invoked)


def check_evals(plugin: Plugin) -> None:
    evals = plugin.path / "evals"
    tagged: set[str] = set()
    for prompt in sorted(evals.glob("*/prompt.md")):
        case = prompt.parent
        meta, _ = split_frontmatter(prompt)
        if meta is None:
            continue
        tags = meta.get("tags") or []
        if meta.get("name") != case.name:
            fail(prompt, f"name must equal the case directory '{case.name}'")
        known = [t for t in tags if t in plugin.skills]
        for tag in set(tags) - set(known):
            fail(prompt, f"tag '{tag}' is not a skill of this plugin")
        if known and not any(case.name.startswith(f"{t.removeprefix(SKILL_PREFIX)}-") for t in known):
            fail(case, f"case name must start with the tagged skill name without '{SKILL_PREFIX}', for example '{known[0].removeprefix(SKILL_PREFIX)}-'")
        tagged.update(known)
        if not any((case / "graders").glob("*.md")):
            fail(case, "eval case has no graders")
    for name in plugin.skills:
        if name not in tagged:
            fail(evals, f"no eval case is tagged with '{name}'")


def check_router(plugin: Plugin) -> None:
    router = plugin.path / "skills" / ROUTER_SKILL / "SKILL.md"
    if not router.is_file():
        return
    text = read_text(router)
    for name, skill in plugin.skills.items():
        if name != ROUTER_SKILL and not skill.user_invoked and f"`{name}`" not in text:
            fail(router, f"router does not mention sibling skill `{name}`")


def check_readme(plugins: dict[str, Plugin]) -> None:
    if not README.is_file():
        fail(README, "file is missing")
        return
    text = read_text(README)
    for plugin in plugins.values():
        for name, skill in plugin.skills.items():
            link = f"[`{name}`]({(skill.path / 'SKILL.md').relative_to(ROOT).as_posix()})"
            if link not in text:
                fail(README, f"skills table does not list {link}")


def check_agents(plugin: Plugin) -> None:
    for agent in sorted((plugin.path / "agents").glob("*.md")):
        meta, body = split_frontmatter(agent)
        if meta is None:
            continue
        preloaded = meta.get("skills") or []
        if not preloaded:
            fail(agent, "agents are thin adapters and must preload skills with 'skills:'")
        for name in preloaded:
            if name not in plugin.skills:
                fail(agent, f"preloads unknown skill '{name}'")
        if len(body.strip().splitlines()) > MAX_AGENT_LINES:
            fail(agent, f"agent body exceeds {MAX_AGENT_LINES} lines, move knowledge into a skill")


def main() -> int:
    dirs = sorted(p for p in PLUGINS_DIR.iterdir() if p.is_dir()) if PLUGINS_DIR.is_dir() else []
    if not dirs:
        fail("plugins/", "no plugins found")
    plugins = {p.name: Plugin(path=p) for p in dirs}

    seen: dict[str, Path] = {}
    for plugin in plugins.values():
        check_plugin_manifests(plugin)
        skills_dir = plugin.path / "skills"
        skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
        if not skill_dirs:
            fail(plugin.path, "plugin has no skills")
        for skill_dir in skill_dirs:
            skill = check_skill(skill_dir)
            if skill is None:
                continue
            if skill.name in seen:
                fail(skill_dir, f"skill name '{skill.name}' is already used in {seen[skill.name].relative_to(ROOT).as_posix()}")
            seen[skill.name] = skill_dir
            plugin.skills[skill.name] = skill
        check_evals(plugin)
        check_router(plugin)
        check_agents(plugin)
    check_marketplaces(plugins)
    check_readme(plugins)

    for line in errors:
        print(f"ERROR {line}")
    for plugin in plugins.values():
        routed = [s for s in plugin.skills.values() if not s.user_invoked]
        chars = sum(len(s.description) for s in routed)
        print(f"{plugin.path.name}: {len(plugin.skills)} skill(s), {len(routed)} model-invoked, {chars} description characters always in context")
    print(f"{len(plugins)} plugin(s), {len(seen)} skill(s), {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
