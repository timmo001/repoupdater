# repoupdater

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
[![License][license-shield]](LICENSE.md)

[![Build Status][travis-shield]][travis]
![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

Update dependencies in your repositories.

*This application was heavily based on [addonupdater] by
 [Ludeeus]. Big props to him for probably 90%+ of this project!*

## Install

To install, just run:

> **Requires Python version 3.5.3+**

```bash
pip install repoupdater
```

## Example

The following example will not commit anything since `--test` is enabled. This
 is good for testing you have the right repo and confirming before you commit.

```bash
repoupdater --token AAAAAAAAAAAAAAAAAAAAA --repo sqlite-web --test
```

```bash
```

## CLI options

param | alias | description
-- | -- | --
`--token` | `-T` | An GitHub Access token with `repo` permissions.
`--repo` | `-R` | Name of the repo for the repository. eg. `myorg/myrepo`
`--apk` | `-a` | Check for apk updates.
`--pip` | `-p` | Check for pip updates.
`--test` | `None` | If this flag is used commits will be omitted.
`--verbose` | `None` | Print more stuff to the console.
`--docker_path` | `-D` | Path to your `Dockerfile`. Leave this blank for the root directory.
`--python_req_path` | `-P` | Path to your python `requirements.txt`. Leave this blank for the root directory.
`--release` | `None` | Creates a new release this argument require release version eg. `v1.0.3`.
`--fork` | `None` | Create a fork before creating a pull request, useful if you don't have access to the repo.
`-pull_request` | `-PR` | Create a PR instead of pushing directly to master.

***

## Links

[Contribution Guidelines][CONTRIBUTING]

[Code of Conduct][CODE_OF_CONDUCT]

## License

MIT License

Copyright (c) 2019 Timmo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[addonupdater]: https://github.com/ludeeus/addonupdater
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/timmo
[CODE_OF_CONDUCT]: https://github.com/timmo001/repoupdater/blob/master/.github/CODE_OF_CONDUCT.md
[commits-shield]: https://img.shields.io/github/commit-activity/y/timmo001/repoupdater.svg
[commits]: https://github.com/timmo001/repoupdater/commits/master
[CONTRIBUTING]: https://github.com/timmo001/repoupdater/blob/master/.github/CONTRIBUTING.md
[gitlabci-shield]: https://gitlab.com/timmo/repoupdater/badges/master/pipeline.svg
[gitlabci]: https://gitlab.com/timmo/repoupdater/pipelines
[hass]: https://www.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/timmo001/repoupdater.svg
[ludeeus]: https://github.com/ludeeus
[maintenance-shield]: https://img.shields.io/maintenance/yes/2019.svg
[microbadger]: https://microbadger.com/images/timmo001/repoupdater
[midnight-theme]: https://raw.githubusercontent.com/timmo001/repoupdater/master/docs/resources/midnight-theme.png
[more-info-dark]: https://raw.githubusercontent.com/timmo001/repoupdater/master/docs/resources/more-info-dark.png
[more-info-light]: https://raw.githubusercontent.com/timmo001/repoupdater/master/docs/resources/more-info-light.png
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-orange.svg
[pulls-shield]: https://img.shields.io/docker/pulls/timmo001/repoupdater.svg
[releases-shield]: https://img.shields.io/github/release/timmo001/repoupdater.svg
[releases]: https://github.com/timmo001/repoupdater/releases
[travis-shield]: https://travis-ci.com/timmo001/repoupdater.svg?branch=master
[travis]: https://travis-ci.com/timmo001/repoupdater
[version-shield]: https://images.microbadger.com/badges/version/timmo001/repoupdater.svg
