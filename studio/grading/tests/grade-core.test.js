/* SPDX-License-Identifier: MIT */
const test=require('node:test'),assert=require('node:assert/strict');
const G=require('../grade-core.js');
const meta={id:'TEST01',name:'自制颜色',size:33,baseline:'sRGB JPEG; same camera baseline'};
function roundtrip(l){const text=G.cube(l);const rows=text.trim().split('\n').filter(x=>/^[-+\d.]/.test(x));return {size:l.size,values:new Float32Array(rows.flatMap(x=>x.split(/\s+/).map(Number)))};}
let state=123456;function rand(){state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296;}
for(const size of [17,33])test('identity '+size+'^3: 16384 random RGBA, exact byte equality',()=>{
 const p=new Uint8ClampedArray(16384*4);for(let i=0;i<p.length;i++)p[i]=Math.floor(rand()*256);
 assert.deepEqual(G.apply(G.buildLut(G.parameters(),size),p),p);
});
test('export preserves every Float32 LUT entry',()=>{const p=G.parameters();p.exposure=.35;p.saturation=-21;p.temperature=37;p.shadowTint=-19;
 const l=G.buildLut(p);assert.deepEqual(roundtrip(l).values,l.values);});
test('preview and serialized LUT produce identical 32768 RGBA pixels',()=>{
 const p=G.parameters();p.hue=[12,3,-19,20,-5,8];p.chroma=[20,-12,7,4,11,-28];p.contrast=18;p.curve=[.02,.2,.47,.8,.97];
 const l=G.buildLut(p),data=new Uint8ClampedArray(32768*4);for(let i=0;i<data.length;i++)data[i]=Math.floor(rand()*256);
 assert.deepEqual(G.apply(l,data),G.apply(roundtrip(l),data));});
test('cube red-fastest ordering',()=>{const l=G.buildLut(G.parameters(),17);assert.deepEqual(Array.from(l.values.slice(0,9)),[0,0,0,1/16,0,0,2/16,0,0]);assert.equal(l.values[3*17+1],1/16);assert.equal(l.values[3*17*17+2],1/16);});
test('exposure changes real pixel values',()=>{const p=G.parameters();p.exposure=1;const l=G.buildLut(p);const o=G.apply(l,new Uint8ClampedArray([100,100,100,255]));assert(o[0]>100);assert.equal(o[0],o[1]);assert.equal(o[1],o[2]);});
test('saturation -100 gives grayscale',()=>{const p=G.parameters();p.saturation=-100;const o=G.apply(G.buildLut(p),new Uint8ClampedArray([150,40,90,255]));assert.equal(o[0],o[1]);assert.equal(o[1],o[2]);});
test('source is never modified',()=>{const a=new Uint8ClampedArray([1,30,160,200]),b=a.slice();const p=G.parameters();p.contrast=70;G.apply(G.buildLut(p),a);assert.deepEqual(a,b);});
test('alpha is preserved',()=>{const p=G.parameters();p.temperature=77;const o=G.apply(G.buildLut(p),new Uint8ClampedArray([240,20,20,17]));assert.equal(o[3],17);});
test('all scalar extremes remain bounded',()=>{for(const f of G.fields)for(const value of [f.min,f.max]){const p=G.parameters();p[f.key]=value;const l=G.buildLut(p,17);assert.equal(G.checkLut(l),l);}});
test('100 random looks remain bounded',()=>{for(let i=0;i<100;i++){const p=G.parameters();G.fields.forEach(f=>p[f.key]=f.min+rand()*(f.max-f.min));p.hue=p.hue.map(()=>rand()*60-30);p.chroma=p.chroma.map(()=>rand()*200-100);G.checkLut(G.buildLut(p,17));}});
for(const x of [NaN,Infinity,-Infinity,'0',null])test('reject nonnumeric exposure '+x,()=>{const p=G.parameters();p.exposure=x;assert.throws(()=>G.validate(p));});
test('reject nonmonotonic curves',()=>{const p=G.parameters();p.curve=[0,.7,.2,.8,1];assert.throws(()=>G.validate(p));});
test('reject unsupported LUT sizes',()=>{for(const n of [2,32,65,0,100000])assert.throws(()=>G.buildLut(G.parameters(),n));});
test('strict filenames prevent path traversal and cube-header injection',()=>{for(const id of ['../X','X\nTITLE','中文','ABCDEFGHI',''])assert.throws(()=>G.cube(G.buildLut(G.parameters(),17),id));});
test('empty/unbounded LUT rejected',()=>{assert.throws(()=>G.checkLut({size:33,values:new Float32Array(0)}));const l=G.buildLut(G.parameters());l.values[0]=NaN;assert.throws(()=>G.checkLut(l));});
test('project roundtrip',()=>{const p=G.project(G.parameters(),meta);assert.deepEqual(G.parseProject(JSON.stringify(p)),p);});
test('reject future/false camera-verified project',()=>{const p=G.project(G.parameters(),meta);p.camera_status='verified';assert.throws(()=>G.parseProject(JSON.stringify(p)));p.camera_status='unverified';p.algorithm='future';assert.throws(()=>G.parseProject(JSON.stringify(p)));});
test('reject unknown fields',()=>{const p=G.project(G.parameters(),meta);p.script='x';assert.throws(()=>G.parseProject(JSON.stringify(p)));});
test('reject large project file',()=>assert.throws(()=>G.parseProject(' '.repeat(65537))));
test('camera package needs declared baseline',()=>{assert.throws(()=>G.makePackage(G.parameters(),{...meta,baseline:''},G.buildLut(G.parameters())));});
test('camera package retains exact visible LUT; no images',()=>{const p=G.parameters();p.temperature=35;const l=G.buildLut(p),pack=G.makePackage(p,meta,l);assert.equal(pack.payload.text,G.cube(l,meta.id));assert.equal(pack.status,'draft-camera-importer-not-implemented');assert(!('samples' in pack));});
test('malformed RGBA rejected',()=>assert.throws(()=>G.apply(G.buildLut(G.parameters()),new Uint8Array(3))));
