# Base project

Base project that can be merged in other projects to provide common config.
Merge it in to the project with:
```
git remote add base git@github.com:OxIonics/base_project.git
git fetch base
git merge --allow-unrelated-histories base/master
```

You'll normally encounter some conflicts the first time you do this. For the 
README.md, you probably want to discard this read me, with: 
`git restore --ours README.md`. Other conflicts represent divergence of your 
project from the norms and you'll have to decide whether to conform or whether
your project is special. Deviation from the norms is perfectly acceptable but
merging in this project allows it to be explict.

## Lady Jessica 

### Child projects

The Lady Jessica bot looks for repositories that has a in their pyproject.toml
section like:

```toml
[tool.lady_jessica]
parent_branch = "parent_python"
```

And makes pull requests to those repositories every time the selected
branch in the repo is pushed to merging that branch in to the default
branch of that repo.

### Project types

With in `base_project` there are several branches of the form `parent(_[a-z])*`
these represent the different types of project that we have and Lady Jessica 
will also help propagate changes between these branches by opening PRs to merge
changes to a branch in to all branches that it's name matches up to the last
underscore. E.g. Lady Jessica
will try to merge changes to `parent_python` in to `parent_python_third-party`
and `parent_python_experiments`, but not to `parent_python_unusual_type`. 

