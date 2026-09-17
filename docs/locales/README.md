# UI translations

The maintained languages are Japanese (`ja`), English (`en`) and Simplified
Chinese (`zh`). They cover the project home, assembly activity, four-step
operation guide and cursor demo. The mathematical guide and geometric viewer
remain in English, as their entry links explain.

Only JSON files directly in this directory are loaded by `build-locales.cjs`.
They determine the language menu, embedded translations, required message
coverage and browser checks. When changing a UI message, update these three
catalogs together.

## Inactive translations

`inactive/` preserves the Arabic (`ar`), German (`de`), Spanish (`es`), French
(`fr`) and Russian (`ru`) catalogs. They are not shipped in generated HTML,
shown in the language menu, or checked by the normal build and browser tests.
They may fall behind the interface; updating them is not required for routine
changes. Existing URLs or saved preferences naming an inactive language use
the normal supported-language fallback described below.

Reactivate a language when there is a concrete user need and someone can help
review its wording. Move its JSON file back here, reconcile its message keys
and placeholders with `en.json`, review the translation, then rebuild and run
the checks below. A new language starts as a copy of `en.json`. Set `code` to
its BCP 47 tag, `name` to its native name and `dir` to `ltr` or `rtl`.

## Building and checking

From the repository root:

```sh
node docs/build-assembly.cjs
node docs/build-site.mjs
node docs/assembly/verify-locales.cjs
node docs/verify-pages.cjs '' docs/site_preview_verification.json
```

Language options are generated automatically. Build failures identify missing
keys or mismatched placeholders. See the assembly README for browser setup.

Keep `en.json` as the fallback catalog. Translate message values, preserving
keys and placeholders such as `{count}`. Home keys are English source messages;
assembly keys retain the Japanese source messages used by the app. Use named
placeholders for dynamic values rather than assembling translated sentence
fragments. Translations are text, not HTML. Maintained translations are embedded
in the generated HTML and work offline without a translation service.

Language selection uses a supported URL language, then a supported saved
preference, then the browser's languages (exact tag before base language), then
English. The `zh` catalog is Simplified Chinese, including when selected as a
fallback for a Chinese region tag. A future Traditional Chinese catalog should
use `zh-Hant` and script-aware negotiation rather than treating the two scripts
as interchangeable.

The shared layout retains support for right-to-left prose. Spatial diagrams,
face pairs, view controls and piece rotations keep their physical left/right
meaning. The inactive Arabic catalog includes Unicode LRI/PDI isolates for
mathematical expressions such as `n × U` and `{count}/8`; preserve them if
reactivating it and recheck the RTL interface.

Automated checks cover completeness, layout, offline playback, preserved
assembly state and unchanged geometric arrows. They do not establish idiomatic
wording. Simplified Chinese and the inactive translations have not received
native-speaker review.
