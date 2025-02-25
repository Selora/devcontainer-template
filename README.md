# Devcontainer Template Project

This project template is a template for developing a new project using Devcontainers AND also a Python skeleton app using a modern toolchain.

[DevContainers](https://containers.dev/) & [DevPod.sh](https://devpod.sh):

- Setup a remote & isolated development environment, self-contained with all the dependencies required for your project
- Everything in `.devcontainer/` can be taken and adapted to a new project right away. It uses a `docker-compose`-based workflow to mimic a complex dev environment
- To only use the base python skeleton, remove the `.devcontainer` file

Python skeleton app:

- Dependency Management with [uv](https://github.com/astral-sh/uv) and [pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-pyproject-toml):
  - Setup [ruff](https://github.com/astral-sh/ruff) and the project linter and formatter
  - Setup [basedpyright](https://docs.basedpyright.com/latest/) as the python Language Server (LSP)
- [Just](https://just.systems/man/en/) skeleton to provide a modern alternative to Makefile
- [Pre-Commit](https://pre-commit.com/) hooks with a base setup that invokes the linter & formatter on commit
- [Direnv](https://direnv.net/) to automatically apply `.env.*`  and auto-activate & deactivate the python virtualenv

Happy coding!

## Installation

### DevPod & DevContainer

**Note**: Skip this section if only using the Python skeleton app

1. Install [DevPod.sh](https://devpod.sh/docs/getting-started/install)
2. Create an `ssh` provider (any host with docker installed will do)
3. Spin up the containers. The following will install a set of custom dotfiles and pull this repository:

  ```bash
  devpod up --recreate --debug --provider ssh --ide none --gpg-agent-forwarding --dotfiles git@github.com:Selora/dotfiles.git git@github.com:Selora/devcontainer-template.git@main
  ```

  This command will:

- Recreate and start the dev environment with detailed debugging.
- Use SSH as the provider.
- Not launch an IDE, this is the default for Neovim. (set to `vscode` if that's the IDE you'll use!)
- Forward the GPG Agent.  All SSH keys in this agent will be accessible to the remote container.
- Set up your dotfiles from the provided repository.
- Pull the devcontainer-template project

***Important***: bugs bugs bugs...

- **NeoVim users**: The DevPod agent somehow interact with Nvim in a nasty way that leaves plenty of drawing artifacts. This is only noticeable with Nvim. The easiest workaround is to `docker exec` your way into the dev environment. Ex:
  - Either set a remote [docker context](https://docs.docker.com/engine/manage-resources/contexts/) or ssh into the docker host **without** using the DevPod agent (i.e. not an alias in `~/.ssh/config`)
  - `docker ps` -> Note the image of the current dev containers
  - `docker exec -it -e "TERM=wezterm" -u vscode -w /workspaces/ <img_short_id> /usr/bin/env bash`
- **DevPod providers**: When using the `docker` provider with DevPod **AND** docker-compose, DevPod doesn't mount the workspace in the containers. Using the `ssh` provider solves this issue. Remote machines (i.e. aws, gcp, azure) have not been tested.

### Python Skeleton app only, NO DevContainers

**IF not using DevContainers**, the following needs to be done manually:

1. Install the dependencies: `pipx install uv && uv sync --dev --all-extras && uv run just install`
2. Install `direnv`: <https://direnv.net/docs/installation.html#from-binary-builds>

Following the steps of the next section to get started

### Python Skeleton app

- Test the demo application:
  - Run `just run`
- Enable `direnv`:
  1. Navigate in the workspace and `direnv allow`
  2. Copy the API keys and secrets to the `.env` file. This file is not version-tracked.
  3. edit `.envrc` so that every `.env` files is properly loaded.
- Edit `pyproject.toml`:
  - Edit the project name, python version, version, description, etc.
  - Setup the linter, formatter & LSP options
  - Remove unneeded dependencies & 'dev' dependencies
  - Add new dependencies with `uv add <pypi pkg>` or `uv add --dev <pypi pkg>` for dev-only dependency (ex: linters & LSPs are no needed for release)
- Edit the `.pre-commit-config.yaml` to add/remove commit hooks
- Edit the `justfile` to add/remove "make" commands as you wish. Ex:
  - `just test` spins up pytest
  - `just deploy` packages the project into release

## Notes on Selora's Dotfiles & DevContainers

### Nix Dotfiles

The package manager [Nix](https://nixos.org/) is used to install a separate environment containing a set of nice-to-have executables (ex: cat -> bat, cd -> zoxide, fzf, fish, tmux, etc. )

These dotfiles also push a NeoVim config that is ready to go for python development. These packages, alongside with their dependencies, are ***not*** installed by the OS and are stored in `/nix/store/<derivation_id>`.

***Pros of using Nix***:

- Reproducible same packages on practically any Unix hosts, be it MacOS, a semi-old Ubuntu LTS, Alpine, etc. If you can install nix, you're good to go.
- Easy to deploy the latest NeoVim & dependencies on any container image.
- Easy to rollback. Each upgrades creates a reversible deviation that can be rolled back to, like a git commit or a snapshot
- Does not pollute the OS
- [Wide range of packages available](https://search.nixos.org/packages)
- A few simple `Nix flake` are easy to manage and AI-friendly to produce.

***Cons of using Nix:***

- Can generate conflicts with the host:
  ex: NeoVim requires python, python is installed by `nix` on top of the OS python.  
  Solution: Use `pyproject.toml` & similar to specify exactly the dependencies of your project
- It's a bit slow
- It pulls a whole set of base GNU binary in its base deviation.
- If you're using VSCode you probably don't care about any of that
- The Nix language is ***very*** unintuitive and hard to master.

TL;DR, if not interested in these dotfiles, remove  `"ghcr.io/devcontainers/features/nix:1": {}` from `.devcontainer/devcontainer.json` and [pass your own dotfiles do DevPod](https://devpod.sh/docs/developing-in-workspaces/dotfiles-in-a-workspace).
