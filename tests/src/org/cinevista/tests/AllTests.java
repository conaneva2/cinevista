package org.cinevista.tests;
import org.cinevista.io.*;
import org.cinevista.core.*;
import org.cinevista.host.*;
import java.io.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.nio.file.Files;
import java.util.*;
import javax.imageio.ImageIO;

public final class AllTests {
    private static int passed;
    private interface Test { void run() throws Exception; }
    private static void test(String name,Test t) throws Exception { t.run(); passed++; System.out.println("PASS "+name); }
    private static void ok(boolean b) { if(!b) throw new AssertionError("condition failed"); }
    private static void near(double a,double b,double eps) { if(Math.abs(a-b)>eps) throw new AssertionError(a+" != "+b); }
    private static void rejects(Test t) throws Exception { try { t.run(); } catch(IllegalArgumentException e) { return; } catch(IllegalStateException e) { return; } catch(IOException e) { return; } throw new AssertionError("expected rejection"); }
    private static Geometry.Plan plan(int w,int h,double s,Double a) { return Geometry.plan(w,h,s,a,0,0,false,null,1); }
    public static void main(String[] args) throws Exception {
        final File temp=Files.createTempDirectory("cinevista-host-tests-").toFile();
        test("65:24 differs from 2.70",new Test(){public void run(){ok(Geometry.XPAN!=2.70);near(Geometry.XPAN,65.0/24,0);}});
        test("A7RII nominal JPEG crop",new Test(){public void run(){Geometry.Plan p=plan(7952,5304,1,Geometry.XPAN);ok(p.outputWidth==7952&&p.outputHeight==2936);}});
        test("1.8 natural is 2.7",new Test(){public void run(){near(plan(6000,4000,1.8,null).aspect,2.7,1e-12);}});
        test("lens ratio independent of frame",new Test(){public void run(){Geometry.Plan p=plan(6000,4000,1.5,Geometry.XPAN);near(p.squeeze,1.5,0);ok(p.retainedFraction<1);}});
        test("2x fixed frame crops sides",new Test(){public void run(){Geometry.Plan p=plan(6000,4000,2,2.39);near(p.crop.height(),4000,1e-8);ok(p.crop.width()<6000);}});
        test("compact keeps horizontal samples",new Test(){public void run(){Geometry.Plan p=plan(6000,4000,1.8,null);ok(p.outputWidth==6000&&p.outputHeight==2222);}});
        test("expanded is explicit interpolation",new Test(){public void run(){Geometry.Plan p=Geometry.plan(6000,4000,1.8,null,0,0,true,null,1);ok(p.outputWidth==10800&&p.outputHeight==4000);}});
        test("width cap cannot upscale",new Test(){public void run(){ok(Geometry.plan(6000,4000,1.8,null,0,0,false,9999,1).outputWidth==6000);}});
        test("width cap reduces output",new Test(){public void run(){ok(Geometry.plan(6000,4000,1.8,null,0,0,false,3000,1).outputWidth==3000);}});
        test("move frame top edge",new Test(){public void run(){near(Geometry.plan(6000,4000,1,Geometry.XPAN,0,-1,false,null,1).crop.top,0,0);}});
        test("move frame bottom edge",new Test(){public void run(){near(Geometry.plan(6000,4000,1,Geometry.XPAN,0,1,false,null,1).crop.bottom,4000,1e-8);}});
        test("non-square display pixels",new Test(){public void run(){Geometry.Rect r=Geometry.fit(Geometry.XPAN,640,480,1.125);near(r.width()/r.height()*1.125,Geometry.XPAN,1e-12);}});
        test("display fit never fills by cropping",new Test(){public void run(){Geometry.Rect r=Geometry.fit(3,640,480,1);near(r.width(),640,0);ok(r.height()<480);}});
        test("invalid width",new Test(){public void run()throws Exception{rejects(new Test(){public void run(){plan(1,400,1,null);}});}});
        test("invalid squeeze below one",new Test(){public void run()throws Exception{rejects(new Test(){public void run(){plan(600,400,.8,null);}});}});
        test("NaN rejected",new Test(){public void run()throws Exception{rejects(new Test(){public void run(){plan(600,400,Double.NaN,null);}});}});
        test("infinity rejected",new Test(){public void run()throws Exception{rejects(new Test(){public void run(){plan(600,400,1,Double.POSITIVE_INFINITY);}});}});
        test("out-of-range shift rejected",new Test(){public void run()throws Exception{rejects(new Test(){public void run(){Geometry.plan(600,400,1,2.39,2,0,false,null,1);}});}});
        test("EXIF 2-8 explicitly rejected",new Test(){public void run()throws Exception{for(int n=2;n<=8;n++){final int o=n;rejects(new Test(){public void run(){Geometry.plan(600,400,1,null,0,0,false,null,o);}});}}});
        test("overflow rejected",new Test(){public void run()throws Exception{rejects(new Test(){public void run(){Geometry.plan(600,400,Double.MAX_VALUE,null,0,0,true,null,1);}});}});
        test("10000 randomized geometry and round trips",new Test(){public void run(){Random r=new Random(20260918L);for(int i=0;i<10000;i++){
            int w=256+r.nextInt(10000),h=256+r.nextInt(8000);double s=1+r.nextDouble(),a=1.5+r.nextDouble()*2;
            Geometry.Plan p=Geometry.plan(w,h,s,a,2*r.nextDouble()-1,2*r.nextDouble()-1,false,null,1);
            ok(p.crop.left>=-1e-8&&p.crop.top>=-1e-8&&p.crop.right<=w+1e-8&&p.crop.bottom<=h+1e-8);
            near(p.crop.width()*s/p.crop.height(),a,1e-8);ok(p.retainedFraction>0&&p.retainedFraction<=1.000000001);
            ok(Math.abs(p.crop.width()-w)<1e-7||Math.abs(p.crop.height()-h)<1e-7);
            Geometry.Rect dst=Geometry.fit(a,640,480,1.125);double x=p.crop.left+r.nextDouble()*p.crop.width(),y=p.crop.top+r.nextDouble()*p.crop.height();
            double[] d=Geometry.sourceToDisplay(p.crop,dst,x,y),back=Geometry.displayToSource(p.crop,dst,d[0],d[1]);near(x,back[0],1e-8);near(y,back[1],1e-8);
        }}});
        test("shutter ignores repeat",new Test(){public void run(){CaptureSession c=new CaptureSession();ok(!c.press(true,new CaptureSession.Intent("a",0,1,null)));ok(c.state()==CaptureSession.State.READY);}});
        test("only one capture per session",new Test(){public void run(){CaptureSession c=new CaptureSession();ok(c.press(false,new CaptureSession.Intent("a",0,1,null)));c.releaseKey();ok(!c.press(false,new CaptureSession.Intent("b",0,2,null)));}});
        test("callback does not imply saved",new Test(){public void run(){CaptureSession c=new CaptureSession();c.press(false,new CaptureSession.Intent("a",0,1,null));c.callback(0);ok(c.state()==CaptureSession.State.CALLBACK_RECEIVED);ok(c.sourceToken()==null);}});
        test("unmatched media ID rejected",new Test(){public void run()throws Exception{final CaptureSession c=new CaptureSession();c.press(false,new CaptureSession.Intent("a",0,1,null));c.callback(0);rejects(new Test(){public void run(){c.confirmSource("other","token");}});}});
        test("capture settings immutable",new Test(){public void run(){CaptureSession c=new CaptureSession();double value=1.8;c.press(false,new CaptureSession.Intent("a",0,value,2.39));value=2;near(c.intent().squeeze,1.8,0);}});
        test("interrupt does not infer source",new Test(){public void run(){CaptureSession c=new CaptureSession();c.press(false,new CaptureSession.Intent("a",0,1,null));c.interrupt();c.callback(0);ok(c.state()==CaptureSession.State.INTERRUPTED_UNKNOWN);}});
        test("source requires explicit matching proof",new Test(){public void run(){CaptureSession c=new CaptureSession();c.press(false,new CaptureSession.Intent("a",0,1,null));c.callback(0);c.confirmSource("a","validated-media-token");ok(c.state()==CaptureSession.State.SOURCE_CONFIRMED);}});
        test("unique job directories",new Test(){public void run()throws Exception{ok(!Filesafe.reserveJob(temp).equals(Filesafe.reserveJob(temp)));}});
        test("path traversal blocked",new Test(){public void run()throws Exception{rejects(new Test(){public void run()throws Exception{Filesafe.child(temp,"../photo.jpg");}});}});
        test("new write refuses overwrite",new Test(){public void run()throws Exception{final File f=new File(temp,"exists.txt");Filesafe.writeUtf8New(f,"original");rejects(new Test(){public void run()throws Exception{Filesafe.writeUtf8New(f,"new");}});ok(new String(Files.readAllBytes(f.toPath()),"UTF-8").equals("original"));}});
        test("publish refuses overwrite",new Test(){public void run()throws Exception{final File job=Filesafe.reserveJob(temp),a=new File(job,"a"),b=new File(job,"b");Filesafe.writeUtf8New(a,"one");Filesafe.writeUtf8New(b,"two");rejects(new Test(){public void run()throws Exception{Filesafe.publish(a,b);}});}});
        test("empty staging file not published",new Test(){public void run()throws Exception{final File job=Filesafe.reserveJob(temp),a=new File(job,"a"),b=new File(job,"b");ok(a.createNewFile());rejects(new Test(){public void run()throws Exception{Filesafe.publish(a,b);}});}});
        final File src=new File(temp,"test-source.jpg");BufferedImage target=Target.make(1200,800);ImageExporter.writeJpegNew(target,src,.97f);target.flush();
        test("JPEG dimensions read",new Test(){public void run()throws Exception{JpegGuard.Info i=JpegGuard.read(src);ok(i.width==1200&&i.height==800);}});
        test("unlabelled color requires explicit choice",new Test(){public void run()throws Exception{rejects(new Test(){public void run()throws Exception{JpegGuard.read(src).requireSupported(false);}});JpegGuard.read(src).requireSupported(true);}});
        test("invalid magic rejected",new Test(){public void run()throws Exception{rejects(new Test(){public void run()throws Exception{JpegGuard.read(new ByteArrayInputStream(new byte[]{1,2,3,4}));}});}});
        test("truncated segment rejected",new Test(){public void run()throws Exception{rejects(new Test(){public void run()throws Exception{JpegGuard.read(new ByteArrayInputStream(new byte[]{(byte)255,(byte)216,(byte)255,(byte)225,0,10,0}));}});}});
        test("EXIF endian handling and all eight orientations",new Test(){public void run()throws Exception{for(int o=1;o<=8;o++)for(boolean le:new boolean[]{true,false}){File f=inject(src,temp,225,exif(o,le));final JpegGuard.Info i=JpegGuard.read(f);ok(i.orientation==o);if(o!=1)rejects(new Test(){public void run()throws Exception{i.requireSupported(true);}});}}});
        test("ICC profile rejected even with assume flag",new Test(){public void run()throws Exception{final File f=inject(src,temp,226,"ICC_PROFILE\000test".getBytes("US-ASCII"));rejects(new Test(){public void run()throws Exception{JpegGuard.read(f).requireSupported(true);}});}});
        test("Adobe marker conservatively rejected",new Test(){public void run()throws Exception{final File f=inject(src,temp,238,"Adobe\000test".getBytes("US-ASCII"));rejects(new Test(){public void run()throws Exception{JpegGuard.read(f).requireSupported(true);}});}});
        test("pixel render uses planned crop",new Test(){public void run(){BufferedImage in=new BufferedImage(600,400,BufferedImage.TYPE_INT_RGB);Graphics2D g=in.createGraphics();g.setColor(Color.WHITE);g.fillRect(0,0,600,400);g.setColor(Color.RED);g.fillRect(0,0,600,90);g.dispose();BufferedImage out=ImageExporter.render(in,plan(600,400,1,3.0));ok((out.getRGB(300,0)&0xffffff)==0xffffff);out.flush();in.flush();}});
        test("synthetic 2x squeeze restores square geometry",new Test(){public void run(){BufferedImage raw=new BufferedImage(600,800,BufferedImage.TYPE_INT_RGB);Graphics2D g=raw.createGraphics();g.setColor(Color.WHITE);g.fillRect(0,0,600,800);g.setColor(Color.BLACK);g.fillRect(250,300,100,200);g.dispose();BufferedImage out=ImageExporter.render(raw,plan(600,800,2,null));ok(out.getWidth()==600&&out.getHeight()==400);int minX=9999,maxX=-1,minY=9999,maxY=-1;for(int y=0;y<400;y++)for(int x=0;x<600;x++)if((out.getRGB(x,y)&255)<30){minX=Math.min(minX,x);maxX=Math.max(maxX,x);minY=Math.min(minY,y);maxY=Math.max(maxY,y);}ok(Math.abs((maxX-minX)-(maxY-minY))<=1);out.flush();raw.flush();}});
        test("JPEG export validates output and retains original bytes",new Test(){public void run()throws Exception{String before=Filesafe.sha256(src);ImageExporter.Result r=ImageExporter.export(src,new File(temp,"exports"),1,Geometry.XPAN,0,0,false,null,true);ok(r.image.isFile()&&r.manifest.isFile());near((double)JpegGuard.read(r.image).width/JpegGuard.read(r.image).height,Geometry.XPAN,.004);ok(before.equals(Filesafe.sha256(src)));}});
        test("repeat export never replaces first output",new Test(){public void run()throws Exception{File root=new File(temp,"exports");ImageExporter.Result a=ImageExporter.export(src,root,1,Geometry.XPAN,0,0,false,null,true);String hash=Filesafe.sha256(a.image);ImageExporter.Result b=ImageExporter.export(src,root,1.8,null,0,0,false,null,true);ok(!a.image.equals(b.image));ok(hash.equals(Filesafe.sha256(a.image)));}});
        System.out.println("TOTAL "+passed+" tests passed. Includes 10000 randomized geometry cases. No Android/camera tests executed.");
        remove(temp);
    }
    private static byte[] exif(int orientation,boolean le) throws Exception {
        ByteArrayOutputStream b=new ByteArrayOutputStream();b.write("Exif\000\000".getBytes("US-ASCII"));
        b.write(le?'I':'M');b.write(le?'I':'M');u16(b,42,le);u32(b,8,le);u16(b,1,le);u16(b,0x112,le);u16(b,3,le);u32(b,1,le);u16(b,orientation,le);u16(b,0,le);u32(b,0,le);return b.toByteArray();
    }
    private static void u16(ByteArrayOutputStream o,int v,boolean le){o.write(le?v&255:(v>>>8)&255);o.write(le?(v>>>8)&255:v&255);}
    private static void u32(ByteArrayOutputStream o,int v,boolean le){if(le){u16(o,v&65535,true);u16(o,(v>>>16)&65535,true);}else{u16(o,(v>>>16)&65535,false);u16(o,v&65535,false);}}
    private static File inject(File source,File root,int marker,byte[] data)throws Exception {
        File f=new File(root,UUID.randomUUID().toString()+".jpg");byte[] old=Files.readAllBytes(source.toPath());DataOutputStream o=new DataOutputStream(Filesafe.createNew(f));try{o.write(old,0,2);o.writeByte(255);o.writeByte(marker);o.writeShort(data.length+2);o.write(data);o.write(old,2,old.length-2);}finally{o.close();}return f;
    }
    private static void remove(File f){File[] c=f.listFiles();if(c!=null)for(File x:c)remove(x);if(!f.delete())f.deleteOnExit();}
}
