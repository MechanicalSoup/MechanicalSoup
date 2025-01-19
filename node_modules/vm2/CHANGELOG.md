v3.9.19 (2023-05-16)
--------------------
[fix] Fix resolver issue.

v3.9.18 (2023-05-15)
--------------------
[fix] Multiple security fixes.
[new] Add resolver API to create a shared resolver for multiple `NodeVM` instances allowing to cache scripts and increase sandbox startup times.
[new] Allow to pass a function to `require.context` which is called with the filename allowing to specify the context pre file.

v3.9.17 (2023-04-17)
--------------------
[fix] Multiple security fixes.

v3.9.16 (2023-04-11)
--------------------
[fix] Security fix (see https://github.com/patriksimek/vm2/issues/516).

v3.9.15 (2023-04-06)
--------------------
[fix] Security fix (see https://github.com/patriksimek/vm2/issues/515).

v3.9.14 (2023-02-05)
--------------------
[new] Support conditional export resolution with custom resolver. (nick-klaviyo)  

v3.9.13 (2022-12-08)
--------------------
[fix] Fix typescript errors in index.d.ts  

v3.9.12 (2022-11-29)
--------------------
[new] Add file system API.  
[fix] Fix parsing error with object pattern in catch clause.  

v3.9.11 (2022-08-28)
--------------------
[new] Add option `require.strict` to allow to load required modules in non strict mode.  
[fix] Security fix.  

v3.9.10 (2022-07-05)
-------------------
[new] Add uptime to process.  
[fix] Security fix.  
[fix] Fix inspection with showProxy.

v3.9.9 (2022-02-24)
-------------------
[fix] Bump parser ECMA version to 2022.  

v3.9.8 (2022-02-16)
-------------------
[fix] Add function type check for arguments, caller, and callee property check (GeoffRen)  
[fix] Fix find best extension handler  

v3.9.7 (2022-02-10)
-------------------
[fix] Allow relative require from base script  
[fix] Fix issue with modules with exports clause in package JSON  
[fix] Added missing whitelist check before custom require  
[fix] Revert plain object toString behavior  
[fix] Root path check improved  

v3.9.6 (2022-02-08)
-------------------
[fix] Security fixes (XmiliaH)  

v3.9.5 (2021-10-17)
-------------------
[new] Editor config (aubelsb2)  
[fix] Fix for Promise.then breaking  
[fix] Fix for missing properties on CallSite  

v3.9.4 (2021-10-12)
-------------------
[new] Added strict option  
[fix] Security fixes (XmiliaH)  
[fix] Fixed bound function causes TypeError (XmiliaH)  
[fix] Allow extending of frozen objects  

v3.9.3 (2020-04-07)
-------------------
[fix] Security fixes  
[fix] Fixed problems when Promise object is deleted (XmiliaH)  
[fix] Fixed oversight that write ability can change on non configurable properties (XmiliaH)  
[fix] Support shebang as node does (XmiliaH)  
[fix] Property typos (Shigma)


v3.9.2 (2020-04-29)
-------------------
[new] Added NodeVM options to pass argv & env to process object (XmiliaH)  
[fix] Fixed breakouts in NodeVM (XmiliaH)  
[fix] Made async check more robust (XmiliaH)  

v3.9.1 (2020-03-29)
-------------------
[fix] Require helpers statically in main (XmiliaH)  
[fix] Fix for non-configurable property access (XmiliaH)  

v3.9.0 (2020-03-21)
-------------------
[new] Added vm.Script `lineOffset` and `columnOffset` options (azu)  
[new] Allow to specify a compiler per VMScript (XmiliaH)  
[new] Add option to disable async (XmiliaH)  
[new] Added allot of jsdoc (XmiliaH)  
[fix] Fix access to frozen or unconfigurable properties (XmiliaH)  
[fix] Double wrap Objects to prevent breakout via inspect (XmiliaH)  
[fix] Compile now compiles VM code (XmiliaH)  

v3.8.4 (2019-09-13)
-------------------
[fix] Do not allow precompiling VMScript (XmiliaH)  
[fix] Security fixes (XmiliaH)  

v3.8.3 (2019-07-31)
-------------------
[fix] Security fixes  

v3.8.2 (2019-06-13)
-------------------
[fix] toString() on builtin objects  

v3.8.1 (2019-05-02)
-------------------
[fix] Module resolver fixes  
[fix] require('events') works correctly in Node 12  
[fix] SyntaxError not being instanceOf Error  

v3.8.0 (2019-04-21)
-------------------
[new] Allow prohibiting access to eval/wasm in sandbox context  
[new] Allow transitive external dependencies in sandbox context (Idan Attias)  
[new] Allow using wildcards in module-names passed using the external attribute (Harel Moshe)  
[fix] Default to index.js when specified "main" does not exist (Harel Moshe)  
[fix] Security fixes  

v3.7.0 (2019-04-15)
-------------------
[new] Add require.resolve (Idan Attias)  
[new] Support multiple root paths (Idan Attias)  

v3.6.11 (2019-04-08)
-------------------
[fix] Contextification of EvalError and URIError  
[fix] Security fixes  

v3.6.10 (2019-01-28)
-------------------
[fix] Add missing console.debug function in NodeVM  
[fix] Security fixes  

v3.6.9 (2019-01-26)
-------------------
[fix] Security fixes  

v3.6.8 (2019-01-26)
-------------------
[fix] Security fixes  

v3.6.7 (2019-01-26)
-------------------
[fix] Security fixes  

v3.6.6 (2019-01-01)
-------------------
[fix] Security fixes  

v3.6.5 (2018-12-31)
-------------------
[fix] Security fixes  

v3.6.4 (2018-10-17)
-------------------
[fix] Added new to vmwerror when trying to load coffeescipt but can't (dotconnor)  
[fix] Add arguments to process.nextTick proxy (Patrick Engström)  

v3.6.3 (2018-08-06)
-------------------
[fix] Security fixes  

v3.6.2 (2018-07-05)
-------------------
[fix] Security fixes  

v3.6.1 (2018-06-27)
-------------------
[fix] Security fixes  

v3.6.0 (2018-05-11)
-------------------
[new] Support for custom source extensions  
[new] WIP support for disallowing Promise  
[fix] Prevent slow unsafe alloc for Buffers  
[fix] Refactors around defaults  
[fix] Types definition update  

v3.5.2 (2017-10-04)
-------------------
[fix] Prevent slow unsafe alloc for Buffers  

v3.5.1 (2017-10-04)
-------------------
[fix] Prevent unsafe alloc for Buffers  

v3.5.0 (2017-08-31)
-------------------
[new] Allow a custom compiler to receive the filetype (Orta Therox)  
[new] Allow in-sandbox requires to also get called through the compiler (Orta Therox)  
[new] Support whitelisting modules inside a VM (Orta Therox)  
[new] Add TypeScript definition (Orta Therox)  

v3.4.0 (2017-03-28)
-------------------
[new] Added experimental VM.protect method  

v3.3.1 (2017-03-27)
-------------------
[new] Added VM.freeze method  

v3.2.0 (2017-02-10)
-------------------
[new] Added support for pre-compiled scripts via VMScript  

v3.1.0 (2016-09-03)
-------------------
[new] Added option wrapper (Alizain Feerasta)  

v3.0.1 (2016-07-20)
-------------------
Initial release  
