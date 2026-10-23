package org.cinevista.core;

/** Platform-independent geometry. Encoded horizontal squeeze; EXIF 1 only.
 * All rectangles use continuous, half-open pixel-edge coordinates.
 */
public final class Geometry {
    public static final double XPAN = 65.0 / 24.0;
    public static final double SCOPE = 2.39;
    private Geometry() {}

    public static final class Rect {
        public final double left, top, right, bottom;
        public Rect(double l, double t, double r, double b) {
            left = l; top = t; right = r; bottom = b;
        }
        public double width() { return right - left; }
        public double height() { return bottom - top; }
    }

    public static final class Plan {
        public final int sourceWidth, sourceHeight, outputWidth, outputHeight;
        public final double squeeze, aspect, retainedFraction, aspectError;
        public final Rect crop;
        public final boolean expanded;
        private Plan(int w, int h, double s, double a, Rect c, int ow, int oh, boolean e) {
            sourceWidth=w; sourceHeight=h; squeeze=s; aspect=a; crop=c;
            outputWidth=ow; outputHeight=oh; expanded=e;
            retainedFraction=c.width()*c.height()/((double)w*h);
            aspectError=Math.abs((double)ow/oh-a)/a;
        }
        public String toJson() {
            return "{\"source_width\":"+sourceWidth+",\"source_height\":"+sourceHeight
                +",\"squeeze\":"+squeeze+",\"target_aspect\":"+aspect
                +",\"source_crop\":{\"left\":"+crop.left+",\"top\":"+crop.top
                +",\"right\":"+crop.right+",\"bottom\":"+crop.bottom+"}"
                +",\"output_width\":"+outputWidth+",\"output_height\":"+outputHeight
                +",\"retained_area_fraction\":"+retainedFraction
                +",\"output_aspect_relative_error\":"+aspectError
                +",\"output_policy\":\""+(expanded?"expanded":"compact")+"\"}";
        }
    }
    private static boolean finite(double x) { return !Double.isNaN(x)&&!Double.isInfinite(x); }
    private static void positive(String name,double x) {
        if(!finite(x)||x<=0) throw new IllegalArgumentException(name+" must be finite and positive");
    }
    private static void size(String name,int x) {
        if(x<2) throw new IllegalArgumentException(name+" must be >= 2");
    }
    private static void offset(String name,double x) {
        if(!finite(x)||x < -1 || x > 1) throw new IllegalArgumentException(name+" must be in [-1,1]");
    }
    /** aspect=null means natural frame. widthCap=null never adds a size limit.
     * Expanded is explicitly interpolated output, not extra captured detail.
     */
    public static Plan plan(int w,int h,double s,Double aspect,double ox,double oy,
                            boolean expanded,Integer widthCap,int orientation) {
        size("width",w); size("height",h); positive("squeeze",s);
        if(s<1) throw new IllegalArgumentException("squeeze must be >= 1");
        if(orientation!=1) throw new IllegalArgumentException("EXIF orientation 1 only; original remains untouched");
        offset("offsetX",ox); offset("offsetY",oy);
        if(widthCap!=null) size("widthCap",widthCap.intValue());
        double a=aspect==null ? w*s/h : aspect.doubleValue(); positive("aspect",a);
        double rr=a/s; positive("raw aspect",rr);
        double cw,ch;
        if((double)w/h>=rr) { ch=h; cw=Math.min(w,ch*rr); }
        else { cw=w; ch=Math.min(h,cw/rr); }
        positive("crop width",cw); positive("crop height",ch);
        double x=Math.max(0,w-cw)*(ox+1)/2, y=Math.max(0,h-ch)*(oy+1)/2;
        double limit=cw*(expanded?s:1);
        if(widthCap!=null) limit=Math.min(limit,widthCap.intValue());
        double outW=Math.floor(limit+1e-9), outH=Math.floor(outW/a+0.5);
        if(!finite(outW)||!finite(outH)||outW<2||outH<2||outW>Integer.MAX_VALUE||outH>Integer.MAX_VALUE)
            throw new IllegalArgumentException("output dimensions invalid or overflow");
        return new Plan(w,h,s,a,new Rect(x,y,x+cw,y+ch),(int)outW,(int)outH,expanded);
    }
    public static Rect fit(double aspect,int fw,int fh,double pixelAspect) {
        positive("aspect",aspect); positive("pixelAspect",pixelAspect); size("display width",fw); size("display height",fh);
        double rr=aspect/pixelAspect; positive("display pixel ratio",rr);
        double w,h;
        if((double)fw/fh>=rr) { h=fh; w=h*rr; } else { w=fw; h=w/rr; }
        return new Rect((fw-w)/2,(fh-h)/2,(fw+w)/2,(fh+h)/2);
    }
    /** A map between the same calibrated source region and a display rectangle.
     * Does not discover the Sony preview's crop or pixel aspect for you.
     */
    public static double[] sourceToDisplay(Rect src,Rect dst,double x,double y) {
        positive("source width",src.width()); positive("source height",src.height());
        positive("display width",dst.width()); positive("display height",dst.height());
        return new double[]{dst.left+(x-src.left)*dst.width()/src.width(), dst.top+(y-src.top)*dst.height()/src.height()};
    }
    public static double[] displayToSource(Rect src,Rect dst,double x,double y) {
        return sourceToDisplay(dst,src,x,y);
    }
}
