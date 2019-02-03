"""Enable CLI."""
import click


@click.command()
@click.option("--token", "-T", help="GitHub access_token.")
@click.option("--repo", "-R", default=None, help="Repository path"
              "`myorg/myrepo`.")
@click.option("--apk", "-a", is_flag=True, help="Check for apk updates.")
@click.option('--pip', "-p", is_flag=True, help="Check for pip updates.")
@click.option("--test", is_flag=True, help="Test run, will not commit.")
@click.option("--verbose", is_flag=True, help="Print more stuff.")
@click.option(
    "--apk_version", type=float, default=3.9,
    help="Default target APK version.")
@click.option("--docker_path", "-D", default=None, help="Dockerfile path.")
@click.option("--python_req_path", "-P", default=None, help="Python"
              "requirements.txt path.")
@click.option("--release", default=None, help="Publish a release.")
@click.option("--pull_request", "-PR", is_flag=True, help="Create a PR instead"
              "of commiting to master.")
def cli(token, repo, apk, pip, test, verbose, apk_version, docker_path,
        python_req_path, release, pull_request):
    """CLI for this package."""
    from repoupdater.updater import RepoUpdater
    updater = RepoUpdater(token, repo, apk, pip, test, verbose, apk_version,
                          docker_path, python_req_path, release, pull_request)
    updater.update_repo()


cli()  # pylint: disable=E1120
