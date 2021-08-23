#!/usr/bin/python3

import argparse
import gitflow

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Git wrapper to simplify Gitflow.')

    parser.add_argument('-i', '--init', action='store_true',
                        help='creates the basic gitflow structure within a repository')

    parser.add_argument('-n', '--new', metavar=('B', 'N'), nargs=2, dest='new_item',
                        help='creates a new branch of type B with name N')

    parser.add_argument('-m', '--merge', action='store_true',
                        help='Merges the current branch in to the correct upstream branch')

    parser.add_argument('-c', '--commit', metavar='M', dest='commit',
                        help='commits changes to the current branch with commit message M, and merges where needed')

    args = parser.parse_args()

    if args.init:
        gitflow.init_repo()
    elif args.new_item:
        gitflow.create(args.new_item)
    elif args.merge:
        gitflow.merge()
    elif args.commit:
        gitflow.commit(args.commit)
