# daschland-scripts

## Local setup

Before cloning the repo, you need to install [Git LFS](https://git-lfs.com/).
This is because this repo contains files that are too big to be stored regularly in Git.

```bash
brew install git-lfs
git lfs install
```

We use [uv](https://docs.astral.sh/uv/) to set up Python and the virtual environment.
Install uv with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then you can get started with:

```bash
uv sync
```

This will select an appropriate Python interpreter
(or install it, if no suitable installation can be found).
Then it will create a virtual environment, and install the dependencies.
