# hatch-properdocs

**[Hatch] plugin to integrate [ProperDocs] and infer dependencies into an env**

[![PyPI](https://img.shields.io/pypi/v/hatch-properdocs)](https://pypi.org/project/hatch-properdocs/)
[![License](https://img.shields.io/github/license/properdocs/hatch-properdocs)](https://github.com/ProperDocs/hatch-properdocs/blob/master/LICENSE.md)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ProperDocs/hatch-properdocs/ci.yml.svg)](https://github.com/ProperDocs/hatch-properdocs/actions?query=event%3Apush+branch%3Amaster)

This plugin populates [Hatch] environments with `dependencies` on the fly based on a [`properdocs.yml`] file.

This is intended to effortlessly manage dependencies for a ProperDocs site.

You just need to add this minimal config to Hatch, along with any existing ProperDocs config:

<table><tr><th><code>hatch.toml</code></th><th><code>properdocs.yml</code></th></tr>
<tr><td>

```toml
[env]
requires = [
    "hatch-properdocs",
]

[env.collectors.properdocs.docs]
path = "properdocs.yml"
```

</td><td>

```yaml
site_name: ProperDocs example

plugins:
  - autorefs

markdown_extensions:
  - callouts
  - pymdownx.superfences
```

</td></tr></table>

<details><summary>This gets you the following implied Hatch configuration: (click to expand)</summary>

<table><tr><th><code>hatch.toml</code></th></tr>
<tr><td>

```toml
[envs.docs]
detached = true
dependencies = [
    "markdown-callouts",
    "mkdocs-autorefs",
    "properdocs",
    "pymdown-extensions",
]

[envs.docs.scripts]
build = "properdocs build -f properdocs.yml {args}"
serve = "properdocs serve -f properdocs.yml {args}"
gh-deploy = "properdocs gh-deploy -f properdocs.yml {args}"
```

</td></tr></table>

(this is just for posterity, no such config is actually written to a file)

</details>

With this:

* You don't need to specify the PyPI dependencies, they get inferred on the fly just from [`properdocs.yml`] by doing a reverse lookup of ProperDocs plugins in the [catalog], using [`properdocs get-deps`]. (See more details there)

* An automatically managed virtual environment with pre-defined ProperDocs commands is at your fingertips.

You can check this yourself:

<details><summary><code>hatch env show docs</code></summary>

```
                    Standalone                     
┌──────┬─────────┬────────────────────┬───────────┐
│ Name │ Type    │ Dependencies       │ Scripts   │
├──────┼─────────┼────────────────────┼───────────┤
│ docs │ virtual │ markdown-callouts  │ build     │
│      │         │ mkdocs-autorefs    │ gh-deploy │
│      │         │ properdocs         │ serve     │
│      │         │ pymdown-extensions │           │
└──────┴─────────┴────────────────────┴───────────┘
```

</details>

The dependencies get resolved and installed into a virtual environment as part of a Hatch invocation. So, you can directly run:

<details><summary><code>hatch run docs:build</code></summary>

```
Creating environment: docs
Checking dependencies
Syncing dependencies
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: site
INFO    -  Documentation built in 0.03 seconds
```

</details>

(If you've been using virtualenvs directly, this single command replaces creating an environment, installing dependencies into it, as well as running `properdocs` in it, optionally with arguments)

Furthermore, whenever the set of dependencies changes (i.e. you select new ProperDocs plugins), these Hatch commands will re-install dependencies as necessary.  
Otherwise, the environment is just reused; the installation happens only on the first invocation.

If at any point you want to make sure the dependencies are re-installed anew, you can just remove the environment:

<details><summary><code>hatch env remove docs</code></summary>

```
Removing environment: docs
```

</details>


## Installation

Just [install Hatch]. Ideally in an isolated way with **`pipx install hatch`** (after [installing `pipx`]), or just `pip install hatch` as a more well-known way.

</details>

If you declare `hatch-properdocs` as a dependency in your Hatch config (`pyproject.toml` or `hatch.toml`) as shown above, Hatch will automatically install it on first use.

Alternatively you can install it manually: `pipx inject hatch hatch-properdocs` or just `pip install hatch-properdocs`.

And do *not* install ProperDocs - it's unnecessary, only the sub-environments will have it.

## Configuration

Note that although Hatch is typically associated with managing entire Python projects and applications, you *can* use it purely for environment management for a ProperDocs site - through this plugin, or even without it.

Hatch can be configured through one of two files - `hatch.toml` or `pyproject.toml`. Configs in the latter are equivalent but will always need a `[tool.hatch...]` prefix; it can be used if you have an existing Python project and you don't want to add another config file.

So, add the following into one of the files:

<table><tr><th><code>hatch.toml</code></th><th><code>pyproject.toml</code></th></tr>
<tr><td>

```toml
[env]
requires = [
    "hatch-properdocs",
]

[env.collectors.properdocs.ENV_NAME]
path = "path/to/properdocs.yml"

[envs.ENV_NAME]
...
```

</td><td>

```toml
[tool.hatch.env]
requires = [
    "hatch-properdocs"
]

[tool.hatch.env.collectors.properdocs.ENV_NAME]
path = "path/to/properdocs.yml"

[tool.hatch.envs.ENV_NAME]
...
```

</td></tr></table>

Here, `[env.collectors.properdocs.ENV_NAME]` means: please populate an environment named "ENV_NAME" based on an ProperDocs config. In that section, `path` is the path to `properdocs.yml`.

At the moment that is the entire configurability of this plugin.

In the first example we used "docs" as the environment name, you can use "properdocs" as well if you like, or anything else. Further, if you use "default" as the name (which you might do if documentation building is all that you'll ever use Hatch for) then you can skip the environment prefix (`docs:` in the above example).

Multiple separate environments with their own configs and dependencies can be populated as well.

Inside `[envs.ENV_NAME]` (which is an ordinary construct in Hatch) you can proceed to further customize the environment (though normally it shouldn't be necessary, and the section can be omitted from the text config): you can add extra [`dependencies`] or [`scripts`], or any other environment config. You could also set [`detached`] back to `false` if the documentation actually relies on the project itself being installed, such as in the case of [mkdocstrings].


[ProperDocs]: https://github.com/ProperDocs/properdocs
[`properdocs.yml`]: https://properdocs.org/user-guide/configuration/
[`properdocs get-deps`]: https://github.com/ProperDocs/get-deps
[catalog]: https://github.com/ProperDocs/catalog
[Hatch]: https://hatch.pypa.io/
[install Hatch]: https://hatch.pypa.io/latest/install/#pip
[installing `pipx`]: https://pypa.github.io/pipx/installation/
[`dependencies`]: https://hatch.pypa.io/latest/config/environment/overview/#dependencies
[`scripts`]: https://hatch.pypa.io/latest/config/environment/overview/#scripts
[`detached`]: https://hatch.pypa.io/latest/config/environment/overview/#detached-environments
[mkdocstrings]: https://github.com/mkdocstrings/mkdocstrings
