package org.cinevista.host;
import org.cinevista.core.*;
import java.io.*;
import java.awt.image.BufferedImage;
import java.util.*;

public final class Main {
    public static void main(String[] args) {
        try { run(args); }
        catch(Exception e) { System.err.println("CineVista: "+e.getMessage()); System.exit(2); }
    }
    private static void run(String[] args) throws Exception {
        if(args.length==0||args[0].equals("--help")) {
            System.out.println("CineVista 0.2 desktop reference - NOT a camera APK\n"
                +"target OUT.jpg\n"
                +"plan --width 7952 --height 5304 --squeeze 1.8 --aspect 65:24 [--expanded] [--cap 6000]\n"
                +"export --input IN.jpg --out-dir OUTPUT --squeeze 1.8 --aspect auto [--assume-srgb] [--expanded] [--cap 6000]\n"
                +"Optional: --offset-x -1..1 --offset-y -1..1. EXIF 1 only. Outputs never overwrite inputs."); return;
        }
        if(args[0].equals("target")) {
            if(args.length!=2) throw new IllegalArgumentException("target requires an output filename");
            BufferedImage im=Target.make(1200,800);
            try { ImageExporter.writeJpegNew(im,new File(args[1]),0.97f); } finally { im.flush(); }
            System.out.println("Synthetic target written. NOT camera evidence."); return;
        }
        Set<String> known=new HashSet<String>(Arrays.asList("width","height","squeeze","aspect","offset-x","offset-y","expanded","cap","input","out-dir","assume-srgb"));
        Map<String,String> m=new HashMap<String,String>();
        for(int i=1;i<args.length;i++) {
            if(!args[i].startsWith("--")) throw new IllegalArgumentException("Expected a --named option");
            String key=args[i].substring(2); if(!known.contains(key)||m.containsKey(key)) throw new IllegalArgumentException("Unknown/duplicate option: "+key);
            if(key.equals("expanded")||key.equals("assume-srgb")) m.put(key,"true");
            else { if(i+1==args.length) throw new IllegalArgumentException("Missing value for "+key); m.put(key,args[++i]); }
        }
        double s=Double.parseDouble(get(m,"squeeze","1")),ox=Double.parseDouble(get(m,"offset-x","0")),oy=Double.parseDouble(get(m,"offset-y","0"));
        String a=get(m,"aspect","65:24"); Double aspect;
        if(a.equals("auto")) aspect=null;
        else if(a.equals("65:24")) aspect=Double.valueOf(Geometry.XPAN);
        else aspect=Double.valueOf(a);
        boolean exp=m.containsKey("expanded"); Integer cap=m.containsKey("cap")?Integer.valueOf(m.get("cap")):null;
        if(args[0].equals("plan")) {
            System.out.println(Geometry.plan(Integer.parseInt(get(m,"width","7952")),Integer.parseInt(get(m,"height","5304")),s,aspect,ox,oy,exp,cap,1).toJson());
        } else if(args[0].equals("export")) {
            if(!m.containsKey("input")||!m.containsKey("out-dir")) throw new IllegalArgumentException("--input and --out-dir required");
            ImageExporter.Result r=ImageExporter.export(new File(m.get("input")),new File(m.get("out-dir")),s,aspect,ox,oy,exp,cap,m.containsKey("assume-srgb"));
            System.out.println(r.image.getAbsolutePath()); System.out.println(r.plan.toJson());
        } else throw new IllegalArgumentException("Unknown command: "+args[0]);
    }
    private static String get(Map<String,String> m,String k,String d) { return m.containsKey(k)?m.get(k):d; }
}
