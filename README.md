[github_release]: https://img.shields.io/github/release/picret/modlink.svg?logo=github&logoColor=white
[pypi_version]: https://img.shields.io/pypi/v/modlink.svg?logo=python&logoColor=white
[python_versions]: https://img.shields.io/pypi/pyversions/modlink.svg?logo=python&logoColor=white
[github_license]: https://img.shields.io/github/license/picret/modlink.svg?logo=github&logoColor=white
[github_action]: https://github.com/picret/modlink/actions/workflows/tests.yml/badge.svg

[![GitHub Release][github_release]](https://github.com/picret/modlink/releases/)
[![PyPI Version][pypi_version]](https://pypi.org/project/modlink/)
[![Python Versions][python_versions]](https://pypi.org/project/modlink/)
[![License][github_license]](https://github.com/picret/modlink/blob/main/LICENSE)
<br>
[![Tests][github_action]](https://github.com/picret/modlink/actions/workflows/tests.yml)

# ModLink

ModLink is a library designed to give agents a means to communicate.

See the [PATTERN.md](PATTERN.md) for more information on the pattern used in ModLink.

## Installation

You can install ModLink using pip
```sh
pip install modlink
```

Or, if you're using Poetry
```sh
poetry add modlink
```

## Usage

For more detailed usage and examples, see the [examples](examples/README.md) directory. After defining your agents, you can link them with additional tools. For instance, you can use [AgentArgParser](modlink/tools/agent_arg_parser.py) to enable command-line interaction with your agents.

## Contributing

We welcome contributions! If you'd like to contribute, please see our [CONTRIBUTING.md](CONTRIBUTING.md) for more information. 

## License

ModLink is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.
