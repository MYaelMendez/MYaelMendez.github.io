const fs=require("fs"),path=require("path");
const core=fs.readFileSync(path.join(__dirname,"core.js"),"utf8");
const tpl=fs.readFileSync(path.join(__dirname,"index.tpl.html"),"utf8");
if(!tpl.includes("/*CORE*/"))throw new Error("no CORE slot");
const out=tpl.replace("/*CORE*/",()=>core);
fs.writeFileSync(path.join(__dirname,"..","index.html"),out);
const js=out.match(/<script>([\s\S]*?)<\/script>/g).map(s=>s.replace(/<\/?script>/g,"")).join("\n;\n");
fs.writeFileSync("/tmp/face-check.js",js);
console.log("index.html",out.length,"bytes; script",js.length);
