# Automatic update for github docs page for EEA packages

## Installation

Clone the repository

    $ git clone https://github.com/eea/eea.docker.githubdocs
    $ cd eea.docker.githubdocs

During the first time deployement, create and edit the .gitconfig and the id_rsa files

## Add or update the readme for a package:

    $ docker-compose run --rm app https://github.com/collective/<package name>

## Add or update the readme for more packages:

    $ docker-compose run --rm app https://github.com/collective/<package name1> https://github.com/collective/<package name2>

## Add or update all packages specified in the whitelist file:

    $ docker-compose run --rm app `cat whitelist`

## Available environment variables:

<table>
    <th>
        <tr>
            <td>
                Variable
            </td>
            <td>
                Description
            </td>
            <td>
                Default value
            </td>
        </tr>
    </th>
    <tbody>
        <tr>
            <td>
                MENU_FILE
            </td>
            <td>
                File which contains the specification of the right menu
            </td>
            <td>
                _data/menu.yml
            </td>
        </tr>
        <tr>
            <td>
                LANDING_FILE
            </td>
            <td>
                The readme where the list of available packages is displayed
            </td>
            <td>
                IT-systems/index.md
            </td>
        </tr>
        <tr>
            <td>
                DOCS_LOCATION
            </td>
            <td>
                The folder where the readme files for packages will be added
            </td>
            <td>
                IT-systems
            </td>
        </tr>
        <tr>
            <td>
                MENU_BASE
            </td>
            <td>
                The prefix what we should add to the links to the readme files
            </td>
            <td>
                /IT-systems/
            </td>
        </tr>
        <tr>
            <td>
                MENU_BASE_NAME
            </td>
            <td>
                The name of the menu item in the menu.yml which should contain the subitems for the packages
            </td>
            <td>
                IT-systems
            </td>
        </tr>
        <tr>
            <td>
                PLACEHOLDER_START
            </td>
            <td>
                After this marker we add the list of the packages
            </td>
            <td>
                &lt;div style="display:none" class="generated_start"&gt;</div&gt;
            </td>
        </tr>
        <tr>
            <td>
                PLACEHOLDER_END
            </td>
            <td>
                Before this marker we add the list of the packages
            </td>
            <td>
                &lt;div style="display:none" class="generated_end"&gt;&lt;/div&gt;
            </td>
        </tr>
        <tr>
            <td>
                PACKAGE_FOLDER_NAME
            </td>
            <td>
                The location where to clone the gir repo of the github docs
            </td>
            <td>
                docs
            </td>
        </tr>
        <tr>
            <td>
                PACKAGE_GIT_URL
            </td>
            <td>
                The git link to the github docs
            </td>
            <td>
                git@github.com:eea/docs.git
            </td>
        </tr>
        <tr>
            <td>
                PACKAGE_GIT_BRANCH
            </td>
            <td>
                The branch where we want to make the commit
            </td>
            <td>
                gh-pages
            </td>
        </tr>
    </tbody>
</table>

## Copyright and license

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The Original Code is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

## Funding

[European Environment Agency (EU)](http://eea.europa.eu)
