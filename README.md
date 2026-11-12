# Namakam

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 19.2.21.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.

## Mantra summaries and word meanings

`src/mantra-meanings.json` stores original English summary translations and simple word glosses for all 164 current mantra routes. Keys use `anuvakamId_mantraId`; each entry has `summary` and an ordered `words` array of `{ word, meaning }`. Repeated words are listed once, sandhi is separated for reading, and meaningful compounds are retained. Sanskrit word forms follow the detail page’s script selector.

The summaries interpret the Sanskrit using the repository’s Sāyaṇa and Bhaṭṭa Bhāskara commentary transcriptions in `src/assets/rudradhyaya/page-*-en.txt`. They are concise study aids, not verbatim quotations from a named translator; traditional interpretations sometimes differ. The brief definitions in the tables remain independent of the legacy dictionary IDs, some of which contain misaligned meanings. Hovering, focusing or clicking a table word opens the same existing detailed dictionary analysis used in pada patha; those source analyses are not rewritten by this feature.

Keep entries aligned with the passage displayed at each existing route when editing or renumbering mantras. In particular, the current website’s `10_12` contains the earth-Rudras verse; this differs from the corrected section boundary in `src/namakam.json`.

Validate coverage and key translation regressions with:

```bash
node --test scripts/mantra-meanings.test.js
npm test -- --watch=false --browsers=ChromeHeadless
```

Table word interactions match exact Sanskrit forms, with explicit spelling and split-verb links in `src/app/mantra-detail/word-meaning-links.json`. They do not infer matches from table position. `सर्वाः` (1.6) and `योः` (10.4) have no matching detailed entry; the UI shows their brief definition with an availability note. Clicking opens and scrolls to the shared detail panel; keyboard focus opens the tooltip, Enter/Space activates the button, and Escape dismisses word details.
