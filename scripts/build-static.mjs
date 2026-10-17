import {mkdir,copyFile,cp,readdir} from 'node:fs/promises';
await mkdir('dist',{recursive:true});
for(const file of (await readdir('.')).filter(file=>file.endsWith('.html'))) await copyFile(file,`dist/${file}`);
for(const dir of ['assets','books']) await cp(dir,`dist/${dir}`,{recursive:true});
console.log('Static site built: homepage, study desk, 66 books and assets.');
