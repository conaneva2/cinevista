package org.cinevista.host;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;

/** Exact engineering chart, not a photo or camera output. */
public final class Target {
    private Target() {}
    public static BufferedImage make(int w,int h) {
        BufferedImage image=new BufferedImage(w,h,BufferedImage.TYPE_INT_RGB);
        Graphics2D g=image.createGraphics();
        try {
            g.setColor(new Color(236,236,236)); g.fillRect(0,0,w,h);
            g.setColor(new Color(176,176,176)); g.setStroke(new BasicStroke(1));
            int step=Math.max(20,w/24);
            for(int x=0;x<w;x+=step) g.drawLine(x,0,x,h);
            for(int y=0;y<h;y+=step) g.drawLine(0,y,w,y);
            g.setColor(Color.BLACK); g.setStroke(new BasicStroke(4));
            int d=h/2; g.drawOval((w-d)/2,(h-d)/2,d,d);
            g.drawLine(w/2,0,w/2,h); g.drawLine(0,h/2,w,h/2);
            g.drawRect(8,8,w-17,h-17);
            int box=w/8;
            g.setColor(new Color(184,30,45));g.fillRect(15,15,box,box/2);
            g.setColor(new Color(28,132,75));g.fillRect(w-box-15,15,box,box/2);
            g.setColor(new Color(28,67,170));g.fillRect(15,h-box/2-15,box,box/2);
            g.setColor(new Color(204,159,20));g.fillRect(w-box-15,h-box/2-15,box,box/2);
            g.setColor(Color.BLACK);g.setFont(new Font("SansSerif",Font.BOLD,Math.max(16,w/50)));
            g.drawString("TL",25,40);g.drawString("TR",w-box-5,40);
            g.drawString("BL",25,h-25);g.drawString("BR",w-box-5,h-25);
            g.drawString("CINEVISTA - SYNTHETIC TEST TARGET - NOT A CAMERA SAMPLE",w/7,h/6);
        } finally { g.dispose(); }
        return image;
    }
}
