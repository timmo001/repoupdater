"""Update dependencies in your repositories."""
import requests
from alpinepkgs.packages import get_package
from github import Github
from github.GithubException import UnknownObjectException, GithubException

COMMIT_MSG = ':arrow_up: Updates {} to version {}'
REPO = "{}/{}"
NEW_BRANCH = "update-{}-{}"
PR_BODY = """
# Proposed Changes

This PR will update `{package}` to version `{version}`.

This PR was created automatically, please check the "Files changed" tab
before merging!

***

This PR was created with [repoupdater][repoupdater] :tada:

[repoupdater]: https://pypi.org/project/repoupdater/
"""


class RepoUpdater():
    """Class for repo updater."""

    def __init__(self, token, repo, apk=False, pip=False, test=False,
                 verbose=False, apk_version=3.10, docker_path=None,
                 python_req_path=None, release=None, pull_request=False):
        """Initilalize."""
        self.token = token
        self.repo = repo
        self.apk = apk
        self.pip = pip
        self.test = test
        self.verbose = verbose
        self.apk_version = apk_version
        self.docker_path = '' if not docker_path else docker_path + '/'
        self.python_req_path = (
            '' if not python_req_path else python_req_path + '/')
        self.pull_request = pull_request
        self.release = release
        self.github = Github(token)

    def update_repo(self):
        """Run through updates for an repo."""
        if self.verbose:
            print("Repository", self.repo)
            print("Docker Path", self.docker_path)
            print("Python Requirements.txt Path", self.python_req_path)

        if self.release is not None:
            self.create_release()
        else:
            print("Starting update sequence for", self.repo)

            if self.apk:
                # Update APK packages
                print('Checking for apk updates')
                self.update_apk()

            if self.pip:
                # Update PIP packages
                print('Checking for pip updates')
                self.update_pip()

    def create_release(self):
        """Create and publish a release."""
        print("Creating release for", self.repo, "with version", self.release)
        repository = self.repo
        repo = self.github.get_repo(repository)
        last_commit = list(repo.get_commits())[0].sha
        prev_tag = list(repo.get_tags())[0].name
        prev_tag_sha = list(repo.get_tags())[0].commit.sha
        body = '## Changes\n\n'
        for commit in list(repo.get_commits()):
            if commit.sha == prev_tag_sha:
                break

            body = body + '- ' + repo.get_git_commit(commit.sha).message + '\n'

        url = "https://github.com" + self.repo + \
            "/compare/" + prev_tag + "..." + self.release
        body = body + "\n\n[Changelog](" + url + ")"

        if self.verbose:
            print("Version", self.release)
            print("Body")
            print(body)
            print("Last commit", last_commit)

        if not self.test:
            repo.create_git_tag_and_release(self.release,
                                            '',
                                            self.release,
                                            body,
                                            last_commit,
                                            '')
        else:
            print("Test was enabled, skipping release")

    def update_apk(self):
        """Get APK packages in use with updates."""
        legacy_target = round(self.apk_version - 0.1, 1)
        file = "{}Dockerfile".format(self.docker_path)
        try:
            remote_file = self.get_file_obj(file)
        except UnknownObjectException:
            print("Dockerfile not found in", file)
            return
        masterfile = self.get_file_content(remote_file)
        run = masterfile.split('RUN')[1].split('LABEL')[0]
        packages = []
        updates = []
        if 'apk' in run:
            cmds = run.split('&&')
            for cmd in cmds:
                if 'apk add' in cmd:
                    all_apk_lines = cmd.replace(' ', '').split('\\\n')
                    for pkg in all_apk_lines:
                        pkg = pkg.split('\n')[0]
                        if '=' in pkg:
                            if '@legacy' in pkg:
                                package = pkg.split('@')[0]
                                branch = 'v{}'.format(legacy_target)
                            elif '@edge' in pkg:
                                package = pkg.split('@')[0]
                                branch = 'edge'
                            else:
                                package = pkg.split('=')[0]
                                branch = 'v{}'.format(self.apk_version)
                            version = pkg.split('=')[1].split()[0]

                            this = {'package': package,
                                    'branch': branch,
                                    'version': version,
                                    'search_string': pkg}
                            packages.append(this)

        for pkg in packages:
            if 'apkadd--no-cache' in str(pkg['package']):
                pack = str(pkg['package']).replace('apkadd--no-cache', "")
                pkg['search_string'] = pkg['search_string'].replace(
                    'apkadd--no-cache', "")
            else:
                pack = pkg['package']
            if self.verbose:
                print("Checking versions for", pack)
            data = get_package(pack, pkg['branch'])
            package = data['package']
            if len(data['versions']) == 1:
                version = data['versions'][0]
            else:
                version = data['x86_64']['version']  # Fallback to x86_64
            if self.verbose:
                print("Current version", pkg['version'])
                print("Available version", version.split()[0])
            if version.split()[0] != pkg['version'].split()[0]:
                this = {'package': package,
                        'version': version,
                        'search_string': pkg['search_string']}
                updates.append(this)
            else:
                print(pack, "Already have the newest version", version)
        if updates:
            for package in updates:
                msg = COMMIT_MSG.format(package['package'], package['version'])

                file = "{}Dockerfile".format(self.docker_path)
                remote_file = self.get_file_obj(file)
                if 'apkadd--no-cache' in package['search_string']:
                    string = package['search_string']
                    string = string.replace('apkadd--no-cache', "")
                    package['search_string'] = string
                search_string = package['search_string'].split('=')
                replace_string = search_string[0] + '=' + package['version']
                find_string = package['search_string'].split()[0]

                if self.verbose:
                    print("Find string '" + find_string + "'")
                    print("Replace with '" + replace_string + "'")

                new_content = self.get_file_content(remote_file)
                new_content = new_content.replace(find_string, replace_string)
                self.commit(file, msg, new_content, remote_file.sha)

    def update_pip(self):
        """Get APK packages in use with updates."""
        file = "{}requirements.txt".format(self.python_req_path)
        packages = []
        updates = []
        try:
            repo = self.github.get_repo(self.repo)
            repo.get_contents(file)
            has_requirements = True
        except UnknownObjectException:
            has_requirements = False
        if has_requirements:
            if self.verbose:
                print("This repo has a requirements.txt file")
            remote_file = self.get_file_obj(file)
            masterfile = self.get_file_content(remote_file)
            lines = masterfile.split('\n')
            if self.verbose:
                print("Lines", lines)
            for line in lines:
                if line != '':
                    if self.verbose:
                        print("Line", line)
                    package = line.split('==')[0]
                    version = line.split('==')[1]
                    this = {'package': package,
                            'version': version,
                            'search_string': line}
                    packages.append(this)
        else:
            file = "{}Dockerfile".format(self.docker_path)
            remote_file = self.get_file_obj(file)
            masterfile = self.get_file_content(remote_file)
            run = masterfile.split('RUN')[1].split('LABEL')[0]
            if 'pip' in run or 'pip3' in run:
                cmds = run.split('&&')
                for cmd in cmds:
                    if 'pip install' in cmd or 'pip3 install' in cmd:
                        all_apk_lines = cmd.replace(' ', '').split('\\\n')
                        for pkg in all_apk_lines:
                            if '==' in pkg:
                                package = pkg.split('==')[0]
                                version = pkg.split('==')[1]

                                this = {'package': package,
                                        'version': version,
                                        'search_string': pkg}
                                packages.append(this)

        for pkg in packages:
            if 'pip3install--upgrade' in pkg['package']:
                pack = pkg['package'].replace('pip3install--upgrade', "")
                pkg['search_string'] = pkg['search_string'].replace(
                    'pip3install--upgrade', "")
            elif 'pipinstall--upgrade' in pkg['package']:
                pack = pkg['package'].replace('pipinstall--upgrade', "")
                pkg['search_string'] = pkg['search_string'].replace(
                    'pipinstall--upgrade', "")
            elif 'pip3install' in pkg['package']:
                pack = pkg['package'].replace('pip3install', "")
                pkg['search_string'] = pkg['search_string'].replace(
                    'pip3install', "")
            elif 'pipinstall' in pkg['package']:
                pack = pkg['package'].replace('pipinstall', "")
                pkg['search_string'] = pkg['search_string'].replace(
                    'pipinstall', "")
            else:
                pack = pkg['package']
            if self.verbose:
                print("Checking versions for", pack)
            url = "https://pypi.org/pypi/{}/json".format(pack)
            data = requests.get(url).json()
            version = data['info']['version']
            if self.verbose:
                print("Current version", pkg['version'])
                print("Available version", version.split()[0])
            if version.split()[0] != pkg['version'].split()[0]:
                this = {'package': pack,
                        'version': version,
                        'search_string': pkg['search_string']}
                updates.append(this)
            else:
                print(pack, "Already have the newest version", version)
        if updates:
            for package in updates:
                msg = COMMIT_MSG.format(package['package'], package['version'])
                remote_file = self.get_file_obj(file)

                search_string = package['search_string'].split('==')
                find_string = package['search_string'].split()[0]
                replace_string = search_string[0] + '==' + package['version']

                if self.verbose:
                    print("Find string '" + find_string + "'")
                    print("Replace with '" + replace_string + "'")

                new_content = self.get_file_content(remote_file)
                new_content = new_content.replace(find_string, replace_string)
                self.commit(file, msg, new_content, remote_file.sha)

    def commit(self, path, msg, content, sha):
        """Commit changes."""
        print(msg)
        if not self.test:
            repository = self.repo
            ghrepo = self.github.get_repo(repository)
            if self.pull_request:
                print("Creating new PR for", self.repo)
                info = msg.split()
                package = info[2]
                version = info[-1]
                title = msg[11:]
                body = PR_BODY.format(package=package, version=version)
                branch = NEW_BRANCH.format(package, version)
                source = ghrepo.get_branch('master')
                ref = "refs/heads/{}".format(branch)
                if self.verbose:
                    print("Repository", repository)
                    print("Msg", msg)
                    print("Branch", branch)
                    print("Ref", ref)
                try:
                    print(ghrepo.create_git_ref(ref=ref,
                                                sha=source.commit.sha))
                except GithubException:
                    print("Ref already exist, skipping")
                    return
                print(ghrepo.update_file(path, msg, content, sha, branch))
                print(ghrepo.create_pull(title, body, 'master', branch))
            else:
                if self.verbose:
                    print("Repository", repository)
                    print("Path", path)
                    print("Msg", msg)
                    print("Sha", sha)
                print("Creating new commit in master for", self.repo)
                print(ghrepo.update_file(path, msg, content, sha))
        else:
            print("Test was enabled, skipping PR/commit")

    def get_file_obj(self, file):
        """Return the file object."""
        repository = self.repo
        ghrepo = self.github.get_repo(repository)
        obj = ghrepo.get_contents(file)
        return obj

    def get_file_content(self, obj):
        """Return the content of the file."""
        return obj.decoded_content.decode()
