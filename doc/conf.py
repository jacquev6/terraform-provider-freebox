# coding: utf8

# Copyright 2020 Vincent Jacques <vincent@vincent-jacques.net>


project = "terraform-provider-freebox"
author = '<a href="http://vincent-jacques.net/">Vincent Jacques</a>'
copyright = f'2020 {author}<script src="https://jacquev6.net/ribbon.2.js" data-project="{project}"></script>'


master_doc = "index"
extensions = []


nitpicky = True

# https://github.com/bitprophet/alabaster
html_sidebars = {
    "**": ["about.html", "navigation.html", "searchbox.html"],
}
html_theme_options = {
    "github_user": "jacquev6",
    "github_repo": project,
}


# http://sphinx-doc.org/ext/githubpages.html
extensions.append("sphinx.ext.githubpages")
