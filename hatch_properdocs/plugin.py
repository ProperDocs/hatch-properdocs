from hatch.env.collectors.plugin.interface import EnvironmentCollectorInterface
from properdocs.commands.get_deps import get_deps


class MkDocsEnvironmentCollector(EnvironmentCollectorInterface):
    PLUGIN_NAME = "properdocs"

    def finalize_config(self, config: dict[str, dict]) -> None:
        for env_name, plugin_env_entry in self.config.items():
            path = plugin_env_entry.get("path", "properdocs.yml")

            deps = get_deps(config_file=self.root / path)
            env = config.setdefault(env_name, {})

            env["dependencies"] = [*deps, *env.get("dependencies", ())]

            env.setdefault("detached", True)

            scripts_config = env.setdefault("scripts", {})
            scripts_config.setdefault("build", f"properdocs build -f {path} {{args}}")
            scripts_config.setdefault("serve", f"properdocs serve -f {path} {{args}}")
            scripts_config.setdefault("gh-deploy", f"properdocs gh-deploy -f {path} {{args}}")
