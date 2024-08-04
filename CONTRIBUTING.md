# Contributing to ModLink

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Feedback is tracked with Github's [issues](https://github.com/picret/modlink/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/picret/modlink/issues/new); it's that easy!

## Development

Install ModLink and run the example.

```bash
conda create -n modlink python=3.10
conda activate modlink
pip install -e .python
examples/example_agent.py
```

Format the code with `black`.

```bash
black .
```

## Releases

We use [SemVer](https://semver.org/) for versioning. For the versions available, see the tags on this repository or go to the [releases page](https://github.com/picret/modlink/releases).

To generate a new release, you simply need to generate a tag.

1. Go to https://github.com/picret/modlink/releases/new
2. Set tag to `X.Y.Z`
3. Set title to `X.Y.Z`
4. Click the `Generate release notes`
5. Add a title to the description `X.Y.Z (YYYY-MM-DD)`
6. Check the `This is a pre-release` if it is a pre-release
7. Click `Publish release`
8. Verify release runs successfully https://github.com/picret/modlink/actions/workflows/release.yml
9. Verify release is available on PyPI https://pypi.org/project/modlink
