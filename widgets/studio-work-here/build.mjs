import {readFileSync,writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const source=readFileSync(new URL('./widget.html',import.meta.url),'utf8');
const page='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Work here · æ Studio</title>\n<style>body{margin:0;background:light-dark(#f4f5ef,#0b100d);color-scheme:light dark}</style>\n</head>\n<body>\n'+source+'\n</body>\n</html>\n';
writeFileSync(new URL('./index.html',import.meta.url),page);
console.log('Built '+fileURLToPath(new URL('./index.html',import.meta.url)));
