"""Exercise QEMU NAND MMIO/DMA and fresh-process persistence; no camera or kernel driver."""
import pathlib,subprocess,socket,time,struct,json,os,hashlib,sys
ROOT=pathlib.Path.cwd();RUN=pathlib.Path(__file__).resolve().parent;OUT=ROOT/'.local/compat-lab/storage-android'
name=sys.argv[1];resultdir=RUN/name;resultdir.mkdir()
media=OUT/(name+'.raw');SIZE=4*1024*1024
with media.open('wb') as f:f.write(b'\xff'*(SIZE+SIZE//4096*8))
BIN=ROOT/'.local/compat-lab/qemu-build/build-arm/arm-softmmu/qemu-system-arm'
results=[]
class Q:
 def __init__(self,n):
  self.path=pathlib.Path('/tmp')/('cv-nand-'+str(os.getpid())+'-'+n+'.sock')
  self.log=(resultdir/(n+'.stderr')).open('w')
  args=[str(BIN),'-machine','cxd90014','-display','none','-monitor','none','-serial','null','-nic','none','-S','-drive','file='+str(media)+',if=mtd,format=raw,cache=writethrough','-qtest','unix:'+str(self.path)+',server=on,wait=off','-qtest-log','/dev/null']
  # Both boot console and UART must share a multiplexed backend.
  args[args.index('-serial')+1]='chardev:ser';args+=['-chardev','null,id=ser,mux=on']
  fixture=json.loads((OUT/'fixture.json').read_text());args+=['-kernel',fixture['kernel'],'-initrd',fixture['root']]
  self.p=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=self.log);self.s=socket.socket(socket.AF_UNIX);self.s.settimeout(5)
  for _ in range(100):
   if self.path.exists():break
   if self.p.poll() is not None:raise RuntimeError('QEMU startup failed')
   time.sleep(.05)
  self.s.connect(str(self.path));self.f=self.s.makefile('rb')
 def cmd(self,c):
  self.s.sendall((c+'\n').encode())
  while True:
   r=self.f.readline().decode().strip()
   if r.startswith('IRQ'):continue
   if not r.startswith('OK'):raise RuntimeError(r)
   return r.split(' ',1)[1] if ' ' in r else ''
 def w(self,a,v):self.cmd('writel %#x %#x'%(a,v))
 def read(self,a,n):return bytes.fromhex(self.cmd('read %#x %#x'%(a,n)).removeprefix('0x'))
 def write(self,a,b):self.cmd('write %#x %#x 0x%s'%(a,len(b),b.hex()))
 def dma(self,page,write=False,data=None,spare=None,sector=None):
  mode=0x31400000 if sector is None else 0x51400000
  count=1 if sector is None else ((sector<<4)|1)
  if write:self.write(0x81001000,data);self.write(0x81003000,spare)
  vals=[0]*16;vals[2]=0x08000000|page;vals[4]=mode|((0x21 if write else 0x20)<<8)|count;vals[6]=0x81001000;vals[14]=0x81003000
  self.write(0x81000000,struct.pack('<16I',*vals));self.w(0x20700,1)
  for v in [0x80,0x81000000,0]:self.w(0x10000010,v)
  assert struct.unpack('<I',self.read(0x81000020,4))[0]==0x8000
  return self.read(0x81001000,4096 if sector is None else 512),self.read(0x81003000,8)
 def erase(self,page):
  self.w(0x20150,64);self.w(0x20700,0);self.w(0x10000000,0x08000000|page);self.w(0x10000010,1)
 def close(self):
  self.s.close();self.p.terminate();self.p.wait(timeout=5);self.log.close()
  if self.path.exists():self.path.unlink()
pattern=bytes(range(256))*16;spare=b'CVG08tag';q=None
try:
 q=Q('writer');q.dma(64,True,pattern,spare);q.close();q=None
 # New process, no saved VM state. Read through emulated controller again.
 q=Q('reader');data,extra=q.dma(64);assert (data,extra)==(pattern,spare),'Write completion did not persist full page/spare across new process';results.append('full page and spare survived fresh QEMU process')
 q.dma(65,True,b'\xaa'*512,b'\xff'*8,sector=3);q.close();q=None
 q=Q('sector-reader');data,extra=q.dma(65);assert data==b'\xff'*1536+b'\xaa'*512+b'\xff'*2048;results.append('sector write preserved untouched bytes')
 q.dma(128,True,pattern,spare);q.erase(64);q.close();q=None
 q=Q('erase-reader');data,extra=q.dma(64);assert data==b'\xff'*4096 and extra==b'\xff'*8
 data,_=q.dma(65);assert data==b'\xff'*4096
 assert q.dma(128)==(pattern,spare);results.append('erase persisted and preserved adjacent block');q.close();q=None
 outcome={'passed':True,'checks':results}
except Exception as e:outcome={'passed':False,'checks':results,'error':repr(e)}
finally:
 if q:q.close()
 outcome.update({'binary_sha256':hashlib.sha256(BIN.read_bytes()).hexdigest(),'media':str(media),'media_sha256':hashlib.sha256(media.read_bytes()).hexdigest(),'scope':'QEMU NAND MMIO controller only; not Linux filesystem or Sony FTL'})
 (resultdir/'result.json').write_text(json.dumps(outcome,indent=2));print(json.dumps(outcome))
raise SystemExit(0 if outcome['passed'] else 1)
