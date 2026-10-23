package org.cinevista.host;

import org.cinevista.io.*;
import org.cinevista.core.*;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.Iterator;
import javax.imageio.*;
import javax.imageio.stream.ImageOutputStream;

/** Desktop reference only. It is NOT an Android/camera image backend. */
public final class ImageExporter {
    public static final class Result {
        public final File image, manifest;
        public final Geometry.Plan plan;
        Result(File i,File m,Geometry.Plan p) { image=i; manifest=m; plan=p; }
    }
    private ImageExporter() {}
    public static Result export(File source,File root,double squeeze,Double aspect,
            double ox,double oy,boolean expanded,Integer cap,boolean assumeSrgb) throws IOException {
        JpegGuard.Info info=JpegGuard.read(source); info.requireSupported(assumeSrgb);
        Geometry.Plan p=Geometry.plan(info.width,info.height,squeeze,aspect,ox,oy,expanded,cap,info.orientation);
        long inputPixels=(long)info.width*info.height, outputPixels=(long)p.outputWidth*p.outputHeight;
        long budget=(inputPixels+outputPixels)*4L+32L*1024*1024;
        if(inputPixels>50000000L||outputPixels>90000000L||budget>Runtime.getRuntime().maxMemory()*0.70)
            throw new IOException("Reference memory budget exceeded. Explicitly select a smaller input/output; no silent downsample");
        String before=Filesafe.sha256(source);
        File job=Filesafe.reserveJob(root),tmp=Filesafe.child(job,"image.jpg.part"),dest=Filesafe.child(job,"image.jpg");
        BufferedImage in=null,out=null;
        try {
            in=ImageIO.read(source);
            if(in==null||in.getWidth()!=info.width||in.getHeight()!=info.height) throw new IOException("Decoder/header mismatch");
            out=render(in,p);
            writeJpegNew(out,tmp,0.95f);
            JpegGuard.Info result=JpegGuard.read(tmp);
            if(result.width!=p.outputWidth||result.height!=p.outputHeight) throw new IOException("Encoded size mismatch");
            BufferedImage check=ImageIO.read(tmp);
            if(check==null) throw new IOException("Output cannot decode"); check.flush();
            if(!before.equals(Filesafe.sha256(source))) throw new IOException("Source changed while processing; no result published");
            Filesafe.publish(tmp,dest);
            String data="{\"schema\":1,\"backend\":\"desktop-java2d-reference\",\"device_test\":false,"
                +"\"state\":\"EXPORTED_APP_ONLY\",\"source_sha256\":\""+before+"\","
                +"\"source_unchanged\":true,\"output_sha256\":\""+Filesafe.sha256(dest)+"\","
                +"\"color_policy\":\"sRGB only; explicit assumption for unlabelled input; no MakerNote copy\","
                +"\"orientation_policy\":\"EXIF 1 or absent only\",\"plan\":"+p.toJson()+"}";
            File manifest=Filesafe.child(job,"manifest.json"); Filesafe.writeUtf8New(manifest,data+"\n");
            return new Result(dest,manifest,p);
        } finally { if(in!=null) in.flush(); if(out!=null) out.flush(); }
    }
    public static BufferedImage render(BufferedImage input,Geometry.Plan p) {
        if(input.getWidth()!=p.sourceWidth||input.getHeight()!=p.sourceHeight) throw new IllegalArgumentException("Plan/input mismatch");
        BufferedImage out=new BufferedImage(p.outputWidth,p.outputHeight,BufferedImage.TYPE_INT_RGB);
        Graphics2D g=out.createGraphics();
        try {
            g.setColor(Color.BLACK); g.fillRect(0,0,out.getWidth(),out.getHeight());
            g.setRenderingHint(RenderingHints.KEY_INTERPOLATION,RenderingHints.VALUE_INTERPOLATION_BICUBIC);
            AffineTransform t=new AffineTransform();
            t.scale(p.outputWidth/p.crop.width(),p.outputHeight/p.crop.height());
            t.translate(-p.crop.left,-p.crop.top);
            g.drawImage(input,t,null);
        } finally { g.dispose(); }
        return out;
    }
    public static void writeJpegNew(BufferedImage image,File file,float quality) throws IOException {
        Iterator<ImageWriter> it=ImageIO.getImageWritersByFormatName("jpeg");
        if(!it.hasNext()) throw new IOException("JPEG encoder missing");
        ImageWriter writer=it.next(); FileOutputStream stream=Filesafe.createNew(file);
        ImageOutputStream ios=null;
        try {
            ios=ImageIO.createImageOutputStream(stream);
            if(ios==null) throw new IOException("Cannot open image output");
            writer.setOutput(ios); ImageWriteParam param=writer.getDefaultWriteParam();
            param.setCompressionMode(ImageWriteParam.MODE_EXPLICIT); param.setCompressionQuality(quality);
            writer.write(null,new IIOImage(image,null,null),param); ios.flush(); stream.getFD().sync();
        } finally { writer.dispose(); if(ios!=null) ios.close(); stream.close(); }
    }
}
