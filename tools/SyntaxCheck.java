import java.io.*;
import java.util.*;
import javax.tools.*;
import com.sun.source.util.JavacTask;
/** PARSE ONLY: does not resolve Android types and is not an SDK build. */
public final class SyntaxCheck {
    public static void main(String[] args)throws Exception{
        JavaCompiler compiler=ToolProvider.getSystemJavaCompiler();
        DiagnosticCollector<JavaFileObject> diagnostics=new DiagnosticCollector<JavaFileObject>();
        StandardJavaFileManager fm=compiler.getStandardFileManager(diagnostics,null,null);
        try{
            Iterable<? extends JavaFileObject> src=fm.getJavaFileObjects(args);
            JavacTask task=(JavacTask)compiler.getTask(null,fm,diagnostics,Arrays.asList("-proc:none","-source","8","-Xlint:-options"),null,src);
            task.parse();boolean error=false;
            for(Diagnostic<?> d:diagnostics.getDiagnostics())if(d.getKind()==Diagnostic.Kind.ERROR){System.err.println(d);error=true;}
            if(error)System.exit(2);
            System.out.println("PASS Java syntax parse for "+args.length+" Android source files. NO type resolution, SDK compilation, DEX or APK verification.");
        }finally{fm.close();}
    }
}
