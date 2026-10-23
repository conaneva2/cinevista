/* SPDX-License-Identifier: MIT — in-memory Worker; latest-result selection is owned by UI. */
let source=null;
self.onmessage=function(e){
  const m=e.data;
  try{
    if(m.type==='image'){source=m.pixels?new Uint8ClampedArray(m.pixels):null;return;}
    if(m.type!=='render')throw Error('Unknown worker message');
    const start=performance.now(),lut=CineVistaGrade.buildLut(m.parameters,m.size);
    const pixels=source?CineVistaGrade.apply(lut,source):null;
    self.postMessage({type:'render',id:m.id,size:lut.size,lut:lut.values.buffer,
      pixels:pixels?pixels.buffer:null,ms:performance.now()-start},pixels?[lut.values.buffer,pixels.buffer]:[lut.values.buffer]);
  }catch(err){self.postMessage({type:'error',id:m.id,message:String(err.message||err)});}
};
