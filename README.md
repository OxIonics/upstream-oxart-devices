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

The Lady Jessica bot looks for repositories that has a in their pyproject.toml
section like:

```toml
[tool.lady_jessica]
parent_branch = "master"
```

And makes pull requests to those repositories every time the selected
branch in the repo is pushed to merging that branch in to the default
branch of that repo.


