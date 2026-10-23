package org.cinevista.tests;
import java.io.*;
import org.cinevista.core.Geometry;
public final class PlanOracle {
    public static void main(String[] args)throws Exception {
        BufferedReader in=new BufferedReader(new InputStreamReader(System.in,"UTF-8"));String line;
        while((line=in.readLine())!=null){String[] p=line.split(" ");
            System.out.println(Geometry.plan(Integer.parseInt(p[0]),Integer.parseInt(p[1]),Double.parseDouble(p[2]),p[3].equals("auto")?null:Double.valueOf(p[3]),Double.parseDouble(p[4]),Double.parseDouble(p[5]),p[6].equals("expanded"),p[7].equals("none")?null:Integer.valueOf(p[7]),1).toJson());
        }
    }
}
