package org.cinevista.probe;
import android.content.Context;
import android.os.SystemClock;
import java.io.*;
import java.util.*;
import org.cinevista.io.Filesafe;

/** No serial, GPS, picture data, settings dump, network or full photo paths. */
final class ProbeLog {
    private static final LinkedList<String> lines=new LinkedList<String>();
    private static File sessionDir;
    private static long started;
    static synchronized void init(Context c) {
        if(sessionDir!=null)return;
        started=SystemClock.elapsedRealtime();
        try { sessionDir=Filesafe.reserveJob(new File(c.getFilesDir(),"sessions")); }
        catch(IOException e) { sessionDir=null; }
        event("session","v0.4; device behavior NOT VERIFIED; app build status must be supplied separately");
    }
    static synchronized void event(String key,String value) {
        String line=(SystemClock.elapsedRealtime()-started)+"ms "+key+" "+value.replace('\n',' ').replace('\r',' ');
        lines.add(line);while(lines.size()>180)lines.removeFirst();
        if(sessionDir!=null)try{
            File f=new File(sessionDir,"events.txt");
            if(f.length()<512000){FileOutputStream o=new FileOutputStream(f,true);try{o.write((line+"\n").getBytes("UTF-8"));o.flush();}finally{o.close();}}
        }catch(IOException ignored){} // Screen still displays the last events; never report export success here.
    }
    static synchronized String recent(){StringBuilder s=new StringBuilder();for(String line:lines)s.append(line).append('\n');return s.toString();}
    static synchronized File export(Context c,String device) throws IOException {
        File root=new File(android.os.Environment.getExternalStorageDirectory(),"CINEVISTA_PROBE");
        File dir=Filesafe.reserveJob(root);
        Filesafe.writeUtf8New(new File(dir,"device.txt"),device);
        Filesafe.writeUtf8New(new File(dir,"events.txt"),recent());
        Filesafe.writeUtf8New(new File(dir,"status.txt"),"Observed runtime declarations/events only. No automatic VERIFIED results.\n"
            +"Storage root is Environment.getExternalStorageDirectory(); removable-card visibility unverified.\n"
            +"Camera model/firmware and each manual test outcome must be recorded by the tester.\n");
        return dir;
    }
    static String error(Throwable e) {
        if(e instanceof java.lang.reflect.InvocationTargetException&&((java.lang.reflect.InvocationTargetException)e).getTargetException()!=null)
            e=((java.lang.reflect.InvocationTargetException)e).getTargetException();
        return e.getClass().getSimpleName(); // Avoid accidentally logging personal file paths from exception messages.
    }
}
