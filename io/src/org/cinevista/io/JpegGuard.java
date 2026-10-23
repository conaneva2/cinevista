package org.cinevista.io;

import java.io.*;
/** Conservative preflight, not a general EXIF/ICC editor. Rejects ICC, non-1
 * orientation and non-sRGB EXIF. Unlabelled JPEG requires an explicit assumption.
 * Header parsing is bounded; pixels are validated by the actual decoder later.
 */
public final class JpegGuard {
    public static final class Info {
        public int width, height, orientation=1;
        public Integer colorSpace;
        public boolean icc, adobe;
        public void requireSupported(boolean assumeSrgb) throws IOException {
            if(width<2||height<2) throw new IOException("Missing/invalid JPEG dimensions");
            if(orientation!=1) throw new IOException("EXIF orientation "+orientation+" not supported; original unchanged");
            if(icc||adobe) throw new IOException("ICC/Adobe marker needs a validated color pipeline");
            if(colorSpace!=null&&colorSpace.intValue()!=1) throw new IOException("EXIF is not labelled sRGB");
            if(colorSpace==null&&!assumeSrgb) throw new IOException("No reliable color label; explicitly choose --assume-srgb for a known sRGB test JPEG");
        }
    }
    private JpegGuard() {}
    public static Info read(File f) throws IOException {
        InputStream in=new BufferedInputStream(new FileInputStream(f));
        try { return read(in); } finally { in.close(); }
    }
    public static Info read(InputStream source) throws IOException {
        DataInputStream in=new DataInputStream(source); Info out=new Info();
        if(in.readUnsignedShort()!=0xffd8) throw new IOException("Not JPEG");
        long total=2; boolean exifSeen=false;
        for(int segments=0;segments<4096&&total<16*1024*1024;segments++) {
            if(in.readUnsignedByte()!=255) throw new IOException("Bad JPEG marker"); total++;
            int marker; do { marker=in.readUnsignedByte(); total++; } while(marker==255&&total<16*1024*1024);
            if(marker==0xda||marker==0xd9) return out;
            if(marker==0||marker==0xd8||(marker>=0xd0&&marker<=0xd7)) throw new IOException("Unexpected marker");
            if(marker==1) continue;
            int len=in.readUnsignedShort(); total+=2;
            if(len<2) throw new IOException("Bad JPEG segment length");
            byte[] data=new byte[len-2]; in.readFully(data); total+=data.length;
            if(marker>=0xc0&&marker<=0xcf&&marker!=0xc4&&marker!=0xc8&&marker!=0xcc) {
                if(data.length<6) throw new IOException("Bad SOF");
                if(out.width!=0) throw new IOException("Multiple SOF unsupported");
                out.height=((data[1]&255)<<8)|(data[2]&255); out.width=((data[3]&255)<<8)|(data[4]&255);
                if((data[0]&255)!=8 || (data[5]&255)!=3) throw new IOException("Only 8-bit three-component JPEG supported");
            }
            if(marker==0xe2&&starts(data,"ICC_PROFILE")) out.icc=true;
            if(marker==0xee&&starts(data,"Adobe")) out.adobe=true;
            if(marker==0xe1&&data.length>=6&&starts(data,"Exif\000\000")) {
                if(exifSeen) throw new IOException("Multiple EXIF blocks unsupported");
                exifSeen=true; parseExif(data,out);
            }
        }
        throw new IOException("JPEG header limit exceeded");
    }
    private static boolean starts(byte[] b,String s) {
        if(b.length<s.length()) return false;
        for(int i=0;i<s.length();i++) if((b[i]&255)!=(int)s.charAt(i)) return false;
        return true;
    }
    private static int u16(byte[] b,int p,boolean le) throws IOException {
        if(p<0||p+2>b.length) throw new IOException("Truncated EXIF");
        return le ? (b[p]&255)|((b[p+1]&255)<<8):((b[p]&255)<<8)|(b[p+1]&255);
    }
    private static long u32(byte[] b,int p,boolean le) throws IOException {
        long a=u16(b,p,le),c=u16(b,p+2,le); return le?a|(c<<16):(a<<16)|c;
    }
    private static void parseExif(byte[] b,Info out) throws IOException {
        boolean le=b.length>8&&b[6]=='I'&&b[7]=='I';
        if(!le&&!(b.length>8&&b[6]=='M'&&b[7]=='M')) throw new IOException("Invalid EXIF endian");
        if(u16(b,8,le)!=42) throw new IOException("Invalid EXIF TIFF header");
        parseIfd(b,u32(b,10,le),le,out,false);
    }
    private static void parseIfd(byte[] b,long offset,boolean le,Info out,boolean sub) throws IOException {
        if(offset<8||offset>b.length-8) throw new IOException("Invalid EXIF offset");
        int p=6+(int)offset,n=u16(b,p,le);
        if(n>1024||(long)p+2+12L*n+4>b.length) throw new IOException("Invalid EXIF IFD");
        Long child=null; boolean orientationSeen=false,colorSeen=false;
        for(int i=0;i<n;i++) {
            int e=p+2+12*i, tag=u16(b,e,le),type=u16(b,e+2,le); long count=u32(b,e+4,le);
            if(tag==0x112&&!sub) {
                if(orientationSeen) throw new IOException("Duplicate orientation tag"); orientationSeen=true;
                if(type!=3||count!=1) throw new IOException("Invalid orientation tag");
                out.orientation=u16(b,e+8,le);
            }
            if(tag==0xa001&&sub) {
                if(colorSeen) throw new IOException("Duplicate color-space tag"); colorSeen=true;
                if(type!=3||count!=1) throw new IOException("Invalid color-space tag");
                out.colorSpace=Integer.valueOf(u16(b,e+8,le));
            }
            if(tag==0x8769&&!sub) {
                if(type!=4||count!=1) throw new IOException("Invalid EXIF subIFD");
                if(child!=null) throw new IOException("Duplicate EXIF subIFD");
                child=Long.valueOf(u32(b,e+8,le));
            }
        }
        if(child!=null) parseIfd(b,child.longValue(),le,out,true);
    }
}
