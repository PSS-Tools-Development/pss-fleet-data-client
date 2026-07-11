# PSS Fleet Data API client - Contribution Guide
If you want to fix a bug or add a new feature, [fork the repository](https://github.com/Zukunftsmusik/pss-fleet-data-importer/fork) to your own github account, make the changes and [open a pull request](https://github.com/Zukunftsmusik/pss-fleet-data-importer/compare). Make sure to add tests for your changes and run all tests before opening the pull request.

# Setup your development environment
This project makes use of [uv](https://docs.astral.sh/uv/) for package dependency management and [Make](https://www.gnu.org/software/make/) for some CLI command shortcuts. If you're developing on Windows, it's recommended to install [Windows Subsystem for Linux (WSL 2)](https://learn.microsoft.com/en-us/windows/wsl/install).

An installation of Python is not required, **uv** will handle this.

## Windows
- Install [chocolatey](https://chocolatey.org/install) (a package manager).
- Run `choco install make` to install **Make**.
- Download the appropriate installer of **uv** [from their website](https://docs.astral.sh/uv/) and run it.

## Linux / Windows Subsystem for Linux (WSL 2)
- Run `sudo apt-get install make` to install **Make**.
- Follow the steps on the [uv website](https://docs.astral.sh/uv/) to install **uv**.

## Subsequent steps
- Open a terminal
- Clone the forked repository onto your machine, e.g. into the folder `~/development/`
- Navigate to the workspace folder, e.g. to `~/development/pss-fleet-data-client`
- Run `make init-dev`. This command will:
  - Update **uv** to the latest version
  - Create a virtual environment in the workspace folder and install all dependencies
  - Install pre-commit hooks that will ensure proper code formatting before committing your changes
  - Run the new pre-commit hooks

# 🥳 Now you're all set up to start coding! 🎉
