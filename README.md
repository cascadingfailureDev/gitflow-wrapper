# gitflow-wrapper
A lightweight Git wrapper to enforce gitflow in all its glory

## What is Gitflow?
Gitflow is a complex, branching strategy which uses feature branches, hotfix branches, release branches, and a develop branch in an attempt to keep a clean trunk. The difficulty with Gitflow is simple, it was not a fully fleshed out system, and is incompatible with modern (read continuous integration) development pattern, and the amount of effort required to maintain all those long lived branches needs a full time manager. This complexity is also its success, if you have multiple different versions of your software running in production (not different versions in pre-prod) Gitflow is likely to be your least-worst option.

## Why make the wrapper?
This wrapper is not meant for use. It has been created to provide the limited functionality needed to implement gitflow and it will error out each time you have a merge conflict (a regular occurrence with multiple long-live branches without liberal and time consuming use of rebase). 
