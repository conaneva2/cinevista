package org.cinevista.io;

import java.io.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.UUID;

/** Own job directories only; no source writes, no DCIM indexing, no overwrite retries. */
public final class Filesafe {
    private Filesafe() {}
    public static File reserveJob(File root) throws IOException {
        if(!root.isDirectory()&&!root.mkdirs()) throw new IOException("Cannot create output root");
        for(int n=0;n<8;n++) {
            File p=new File(root,"cv-"+UUID.randomUUID().toString());
            if(p.mkdir()) return p.getCanonicalFile();
        }
        throw new IOException("Cannot reserve a unique job directory");
    }
    public static File child(File directory,String name) throws IOException {
        if(name==null||name.length()==0||name.indexOf('/')>=0||name.indexOf('\\')>=0||name.equals(".")||name.equals(".."))
            throw new IOException("Not a local filename");
        File f=new File(directory,name).getCanonicalFile();
        if(!directory.getCanonicalFile().equals(f.getParentFile())) throw new IOException("Path escape");
        return f;
    }
    public static FileOutputStream createNew(File f) throws IOException {
        if(!f.createNewFile()) throw new IOException("Refusing to overwrite "+f.getName());
        return new FileOutputStream(f);
    }
    public static void publish(File tmp,File dest) throws IOException {
        if(!tmp.getCanonicalFile().getParentFile().equals(dest.getCanonicalFile().getParentFile()))
            throw new IOException("Must publish inside same owned directory");
        if(!tmp.isFile()||tmp.length()==0||dest.exists()) throw new IOException("Invalid commit/overwrite");
        if(!tmp.renameTo(dest)) throw new IOException("Rename failed; temporary file retained");
    }
    public static String sha256(File file) throws IOException {
        try {
            MessageDigest m=MessageDigest.getInstance("SHA-256");
            InputStream in=new BufferedInputStream(new FileInputStream(file));
            try { byte[] b=new byte[65536]; int n; while((n=in.read(b))!=-1) m.update(b,0,n); }
            finally { in.close(); }
            StringBuilder out=new StringBuilder();
            for(byte b:m.digest()) { int v=b&255; if(v<16) out.append('0'); out.append(Integer.toHexString(v)); }
            return out.toString();
        } catch(NoSuchAlgorithmException e) { throw new IOException("SHA-256 unavailable",e); }
    }
    public static void writeUtf8New(File f,String text) throws IOException {
        FileOutputStream out=createNew(f);
        try { out.write(text.getBytes("UTF-8")); out.getFD().sync(); } finally { out.close(); }
    }
}
