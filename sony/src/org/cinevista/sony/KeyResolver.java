package org.cinevista.sony;
import java.util.Map;
import java.util.HashMap;
/** Names resolved on device; does not assume A6000 integer codes. */
public final class KeyResolver {
    private KeyResolver() {}
    public static Map<Integer,String> resolve() {
        Map<Integer,String> out = new HashMap<Integer,String>();
        try {
            Class<?> c = Class.forName("com.sony.scalar.sysutil.ScalarInput");
            for (String name : new String[]{"UP","DOWN","LEFT","RIGHT","ENTER","MENU","DELETE","SK1","SK2","S1_1","S1_2","S2"}) {
                try { out.put(Integer.valueOf(c.getField("ISV_KEY_" + name).getInt(null)), name); }
                catch (Exception unavailable) { /* Absent keys stay unmapped. */ }
            }
        } catch (ClassNotFoundException unavailable) { /* Non-Sony: no fabricated key map. */ }
        return out;
    }
}
