# Engage v1

This site is about stakeholders who want to collaborate with a certain project. 

## Get started

### Clone the repo

```shell
git clone https://gitlab.fdmci.hva.nl/se-ewa-2020-2021/engage-4.git
cd engage-4
```

### Install npm packages

Install the `npm` packages described in the `package.json` and verify that it works:

```shell
npm install
start
```

The `start` command builds (compiles TypeScript and copies assets) the application into `dist/`, watches for changes to the source files, and runs `engage` on port `4200`.

Shut it down manually with `Ctrl-C`.

#### npm scripts

These are the most useful commands defined in `package.json`:

* `start` - runs node server.js.
* `build` - runs the TypeScript compiler and builds the project with the Environment configuration.
* `ng lint` - Runs linting tools on Angular app code in a given project folder.

These are the test-related scripts:

* `npm test` - Run ng test to execute the unit tests via Karma.
* `npm e2e`- Run ng e2e to execute the end-to-end tests via Protractor

