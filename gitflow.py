import git

missing_master = 'master branch does not exist, please initialize your repository then rerun gitflow init'
missing_develop = 'develop branch does not exist, please run gitflow init, or refactor your repository...'
new_branch = 'you are on the {} branch'


def merge_branches(repo, merge_from, merge_to):
    print('checking out {} branch...'.format(merge_to))
    repo.git.checkout(merge_to)
    print('ensuring {} branch is up to date...'.format(merge_to))
    repo.git.pull('origin', merge_to)
    print('attempting merge to {} branch...'.format(merge_to))
    repo.git.merge(merge_from, no_ff=True)
    print('attempting push to remote {} branch...'.format(merge_to))
    remote_branch = repo.heads[merge_to]
    repo.git.push('origin', remote_branch)
    if merge_from.startswith('release-') and merge_to == 'master':
        merge_name = merge_from[len('release-'):]
        print('tagging master with release name {}...'.format(merge_name))
        repo.create_tag(merge_name)
        print('pushing tag to remote...')
        repo.git.push('origin', merge_name)
    if merge_from.startswith('hotfix-') and merge_to == 'master':
        merge_name = merge_from[len('hotfix-'):]
        print('tagging master with hotfix name {}...'.format(merge_name))
        repo.create_tag(merge_name)
        print('pushing tag to remote...')
        repo.git.push('origin', merge_name)
    print('merge successful...')


def commit_branch(repo, branch, message):
    print('attempting commit...')
    repo.git.add('.')
    repo.git.commit('-m', message)
    print('attempting push to remote...')
    repo.git.push('origin', branch)
    print('commit successful')


def init_repo():
    repo = git.Repo()
    branch_names = [b.name for b in repo.branches]

    assert 'master' in branch_names, missing_master

    if 'develop' not in branch_names:
        repo.git.checkout('-b', 'develop')
        print('develop branch created...')
        print('switching to develop branch')
        repo.git.push('origin', 'develop')
    else:
        repo.git.checkout('develop')
        print('develop branch already created...')
        print('switching to develop branch')


def create(new_item):
    repo = git.Repo()
    new_item_type = new_item[0].lower()
    new_item_name = new_item[1]
    current_branch = repo.active_branch.name
    branch_names = [b.name for b in repo.branches]

    assert 'master' in branch_names, missing_master

    assert 'develop' in branch_names, missing_develop

    assert new_item_type in {'feature', 'release', 'hotfix'}, 'branch type {} not allowed'.format(new_item_type[0])

    assert new_item_name not in branch_names, \
        'a branch named {} already exists, remaining on branch {}...'.format(new_item_name, current_branch)

    if new_item_type == 'feature':
        assert not (new_item_name.startswith('release-') or
                    new_item_name.startswith('hotfix-') or
                    new_item_name == 'master' or
                    new_item_name == 'develop'), \
            'feature branches cannot be named master, develop, or begin with release-, or hotfix-'
        repo.git.checkout('develop')
        repo.git.checkout('-b', new_item_name)
        print('{} branch {} created...'.format(new_item_type, new_item_name))
        print('switching to {} branch {}...'.format(new_item_type, new_item_name))

    else:
        if new_item_type == 'hotfix':
            assert new_item_name.startswith('hotfix-'), 'hotfix branch names must begin with hotfix-'
        else:
            assert new_item_name.startswith('release-'), 'hotfix branch names must begin with release-'

        create_from = 'master' if new_item_type == 'hotfix' else 'develop'
        repo.git.checkout(create_from)
        repo.git.checkout('-b', new_item_name)
        print('{} branch {} created...'.format(new_item_type, new_item_name))
        print('switching to {} branch {}...'.format(new_item_type, new_item_name))


def merge():
    repo = git.Repo()
    current_branch = repo.active_branch.name
    branch_names = [b.name for b in repo.branches]

    assert 'master' in branch_names, missing_master

    assert 'develop' in branch_names, missing_develop

    if not (current_branch.startswith('develop') or
            current_branch.startswith('master') or
            current_branch.startswith('release-') or
            current_branch.startswith('hotfix-')):
        merge_branches(repo, current_branch, 'develop')
        print('attempting to delete feature branch {}...'.format(current_branch))
        repo.git.push('--delete', 'origin', current_branch)
        repo.delete_head(current_branch)
        print(new_branch.format(repo.active_branch))

    elif current_branch.startswith('release-'):
        merge_branches(repo, current_branch, 'master')
        merge_branches(repo, current_branch, 'develop')
        print('attempting to delete release branch {}'.format(current_branch))
        repo.delete_head(current_branch)
        repo.git.push('--delete', 'origin', current_branch)
        print(new_branch.format(repo.active_branch))

    elif current_branch.startswith('hotfix-'):
        merge_branches(repo, current_branch, 'master')
        print('checking for release branches...')
        release_branches = []
        for b in branch_names:
            if b.startswith('hotfix-'):
                release_branches.append(b)
        if release_branches:
            print('{} release branches found...'.format(len(release_branches)))
            for idx, val in enumerate(release_branches):
                print('attempting to update release branch {} of {}...'.format(idx + 1, len(release_branches)))
                merge_branches(repo, current_branch, val)
                merge_branches(repo, current_branch, 'develop')
        else:
            print('no release branches found, merging to develop')
            merge_branches(repo, current_branch, 'develop')
        print('attempting to delete hotfix branch {}...'.format(current_branch))
        repo.delete_head(current_branch)
        repo.git.push('--delete', 'origin', current_branch)
        print(new_branch.format(repo.active_branch))


def commit(message):
    repo = git.Repo()
    current_branch = repo.active_branch.name
    branch_names = [b.name for b in repo.branches]

    assert 'master' in branch_names, missing_master

    assert 'develop' in branch_names, missing_develop

    assert current_branch != 'develop', \
        'committing directly to develop is not allowed, please create a feature branch'

    assert current_branch != 'master', \
        'committing directly to master is not allowed, please create a release or hotfix branch'

    if current_branch.startswith('release-'):
        commit_branch(repo, current_branch, message)
        merge_branches(repo, current_branch, 'develop')
        repo.git.checkout(current_branch)

    else:
        commit_branch(repo, current_branch, message)
