import gitflow
import git
import pytest
import os
main_testing_git = 'git/gitflow-wrapper-test'
missing_master_git = 'git/missing_master'

@pytest.fixture(autouse=True)
def run_before_and_after_tests(request):
    # Setup
    if not os.path.exists('git'):
        os.makedirs('git')
    if not os.path.exists(main_testing_git):
        git.Git('git/').clone('git@github.com:cascadingfailureDev/gitflow-wrapper-test.git')
    if not os.path.exists(missing_master_git):
        os.makedirs(missing_master_git)
        git.Repo.init(missing_master_git)

    main = git.Repo(main_testing_git)
    main.git.checkout('master')
    branch_names = [b.name for b in main.branches]
    for b in branch_names:
        if b != 'master':
            main.delete_head(b)

    missing = git.Repo(missing_master_git)
    branch_names = [b.name for b in missing.branches]
    for b in branch_names:
        if b != 'master':
            missing.delete_head(b)

    yield

    # Teardown
    os.chdir(request.config.invocation_dir)


class TestInit:
    def test_master_exists(self, request):
        # Setup
        os.chdir(main_testing_git)
        repository = git.Repo()

        # Test
        gitflow.init_repo()
        branch_names = [b.name for b in repository.branches]
        current_branch = repository.active_branch.name

        # Result
        assert 'develop' in branch_names and current_branch == 'develop'

    def test_master_missing(self, request):
        # Setup
        os.chdir(missing_master_git)

        # Test
        with pytest.raises(AssertionError):
            gitflow.init_repo()

    def test_develop_exists(self, request):
        # Setup
        os.chdir(main_testing_git)
        repository = git.Repo()
        repository.git.checkout('-b', 'develop')
        repository.git.checkout('master')

        # Test
        gitflow.init_repo()
        branch_names = [b.name for b in repository.branches]
        current_branch = repository.active_branch.name

        # Result
        assert 'develop' in branch_names and current_branch == 'develop'


class TestCreate:
    # Need to add file to prove new branch created from develop and nowhere else
    @pytest.mark.parametrize("test_input", [
        {'starting_branch': 'master', 'branch_name': 'myfeature', 'branch_type': 'feature'},
        {'starting_branch': 'develop', 'branch_name': 'hotfix-1', 'branch_type': 'hotfix'},
        {'starting_branch': 'master', 'branch_name': 'release-1', 'branch_type': 'release'},
        {'starting_branch': 'master', 'branch_name': 'hotfix-2', 'branch_type': 'hotfix'},
        {'starting_branch': 'master', 'branch_name': 'release-2', 'branch_type': 'release'}])
    def test_feature_creation_with_develop(self, request, test_input):
        # Setup
        os.chdir(main_testing_git)
        repository = git.Repo()
        repository.git.checkout('-b', 'develop')
        starting_branches = [b.name for b in repository.branches]
        if test_input['starting_branch'] not in starting_branches:
            repository.git.checkout('-b', test_input['starting_branch'])
        else:
            repository.git.checkout(test_input['starting_branch'])

        # Test
        gitflow.create([test_input['branch_type'], test_input['branch_name']])
        current_branch = repository.active_branch.name

        # Result
        assert current_branch == test_input['branch_name']

    @pytest.mark.parametrize("test_input", [
        {'starting_branch': 'master', 'branch_name': 'myfeature', 'branch_type': 'hotfix'},
        {'starting_branch': 'develop', 'branch_name': 'myfeature', 'branch_type': 'release'},
        {'starting_branch': 'master', 'branch_name': 'hotfix-1', 'branch_type': 'release'},
        {'starting_branch': 'master', 'branch_name': 'release-1', 'branch_type': 'hotfix'},
        {'starting_branch': 'master', 'branch_name': 'develop', 'branch_type': 'feature'},
        {'starting_branch': 'master', 'branch_name': 'master', 'branch_type': 'feature'}])
    def test_feature_creation_with_bad_name_or_branch(self, request, test_input):
        # Setup
        os.chdir(main_testing_git)
        repository = git.Repo()
        repository.git.checkout('-b', 'develop')
        starting_branches = [b.name for b in repository.branches]
        if test_input['starting_branch'] not in starting_branches:
            repository.git.checkout('-b', test_input['starting_branch'])
        else:
            repository.git.checkout(test_input['starting_branch'])

        # Test
        with pytest.raises(AssertionError):
            gitflow.create([test_input['branch_type'], test_input['branch_name']])

    @pytest.mark.parametrize("test_input", [
        {'branch_name': 'myfeature', 'branch_type': 'feature'},
        {'branch_name': 'hotfix-1', 'branch_type': 'hotfix'},
        {'branch_name': 'release-1', 'branch_type': 'release'}])
    def test_creation_with_existing(self, request, test_input):
        # Setup
        os.chdir(main_testing_git)
        repository = git.Repo()
        repository.git.checkout('-b', 'develop')
        repository.git.checkout('-b', test_input['branch_name'])
        repository.git.checkout('develop')

        # Test
        with pytest.raises(AssertionError):
            gitflow.create([test_input['branch_type'], test_input['branch_name']])

    def test_creation_without_develop(self, request):
        # Setup
        os.chdir(main_testing_git)

        # Test
        with pytest.raises(AssertionError):
            gitflow.create(['feature', 'myfeature'])

    def test_creation_without_master(self, request):
        # Setup
        os.chdir(missing_master_git)

        # Test
        with pytest.raises(AssertionError):
            gitflow.create(['feature', 'myfeature'])


class TestMerge:
    def test_merge_feature(self):
        assert True

    def test_merge_feature_no_develop(self):
        assert True

    def test_merge_hotfix_no_feature(self):
        assert True

    def test_merge_hotfix_feature(self):
        assert True

    def test_merge_hotfix_no_develop(self):
        assert True

    def test_merge_release(self):
        assert True

    def test_merge_release_no_develop(self):
        assert True


class TestCommit:
    def test_commit_release(self):
        assert True

    def test_commit_not_release(self):
        assert True
