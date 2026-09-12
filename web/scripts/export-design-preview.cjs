/* Build a self-contained evaluation HTML from the existing preview, without new dependencies. */
const fs = require("node:fs");
const path = require("node:path");
const ts = require("typescript");

const web = path.resolve(__dirname, "..");
const preview = path.join(web, "app/design-preview/preview.tsx");
const cssFile = path.join(web, "app/design-preview/preview.module.css");
const output = path.resolve(web, "../docs/artefacts/parrot-design-evaluation.html");
const css = fs.readFileSync(cssFile, "utf8");
const classes = Object.fromEntries([...css.matchAll(/\.([a-zA-Z_][\w-]*)/g)].map((m) => [m[1], m[1]]));
const production = {
  react: "react/cjs/react.production.js",
  "react/jsx-runtime": "react/cjs/react-jsx-runtime.production.js",
  "react-dom": "react-dom/cjs/react-dom.production.js",
  "react-dom/client": "react-dom/cjs/react-dom-client.production.js",
  scheduler: "scheduler/cjs/scheduler.production.js",
};
const modules = [];
const ids = new Map();

function bundle(file) {
  if (ids.has(file)) return ids.get(file);
  const id = modules.length;
  ids.set(file, id);
  modules.push("");
  let source = file === cssFile
    ? `module.exports = ${JSON.stringify(classes)};`
    : fs.readFileSync(file, "utf8");
  if (file.endsWith(".tsx")) {
    const result = ts.transpileModule(source, {
      fileName: file,
      compilerOptions: {
        target: ts.ScriptTarget.ES2020,
        module: ts.ModuleKind.CommonJS,
        jsx: ts.JsxEmit.ReactJSX,
        esModuleInterop: true,
      },
      reportDiagnostics: true,
    });
    if (result.diagnostics?.some((d) => d.category === ts.DiagnosticCategory.Error)) {
      throw new Error(ts.formatDiagnosticsWithColorAndContext(result.diagnostics, {
        getCanonicalFileName: (name) => name,
        getCurrentDirectory: () => web,
        getNewLine: () => "\n",
      }));
    }
    source = result.outputText;
  }
  source = source.replace(/process\.env\.NODE_ENV/g, '"production"');
  source = source.replace(/require\(["']([^"']+)["']\)/g, (_, name) => {
    const dependency = production[name]
      ? path.join(web, "node_modules", production[name])
      : require.resolve(name, { paths: [path.dirname(file)] });
    return `__require(${bundle(dependency)})`;
  });
  modules[id] = `function(module,exports,__require){\n${source}\n}`;
  return id;
}

const previewId = bundle(preview);
const reactId = bundle(path.join(web, "node_modules", production.react));
const domId = bundle(path.join(web, "node_modules", production["react-dom/client"]));
const script = `(() => { "use strict";
const modules=[${modules.join(",\n")}],cache={};
function __require(id){if(cache[id])return cache[id].exports;const m=cache[id]={exports:{}};modules[id](m,m.exports,__require);return m.exports;}
__require(${domId}).createRoot(document.getElementById("root")).render(__require(${reactId}).createElement(__require(${previewId}).DesignPreview));
})();`;
const licences = ["react", "react-dom", "scheduler", "lucide-react"].map((name) =>
  `${name}\n${fs.readFileSync(path.join(web, "node_modules", name, "LICENSE"), "utf8")}`
).join("\n\n");
const escapeHtml = (text) => text.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; font-src data:; base-uri 'none'; form-action 'none'">
<title>PARROT — three interface directions</title>
<meta name="description" content="Offline interactive evaluation of Civic Register, Kitchen Table and The Reading Desk. Sample data only.">
<style>
*,*::before,*::after{box-sizing:border-box}body{margin:0}h1,h2,h3,p{margin:0}button,textarea{font:inherit}button{appearance:none}svg{display:block;vertical-align:middle}textarea{margin:0}button{margin:0}a{color:inherit}strong{font-weight:600}
${css}
</style></head><body><div id="root"></div>
<noscript>Enable JavaScript to explore the three PARROT interface designs. This file works offline and uses sample data only.</noscript>
<script>${script.replace(/<\/script/gi, "<\\/script")}</script>
<template id="third-party-licences"><pre>${escapeHtml(licences)}</pre></template>
</body></html>\n`;
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, html, "utf8");
console.log(`Exported ${output} (${(Buffer.byteLength(html) / 1024 / 1024).toFixed(2)} MB; ${modules.length} bundled modules).`);
