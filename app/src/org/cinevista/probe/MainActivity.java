package org.cinevista.probe;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.*;

public final class MainActivity extends BaseProbeActivity {
    private TextView status;
    protected void onCreate(Bundle b){super.onCreate(b);
        setContentView(R.layout.probe_home);
        status=(TextView)findViewById(R.id.probe_status);
        bind(R.id.read_device,new View.OnClickListener(){public void onClick(View v){status.setText(ProbeServices.snapshot(MainActivity.this));}});
        bind(R.id.open_preview,new View.OnClickListener(){public void onClick(View v){startActivity(new Intent(MainActivity.this,PreviewActivity.class));}});
        bind(R.id.image_test,new View.OnClickListener(){public void onClick(View v){startActivity(new Intent(MainActivity.this,ImageProbeActivity.class));}});
        bind(R.id.recent_events,new View.OnClickListener(){public void onClick(View v){status.setText(ProbeLog.recent());}});
        bind(R.id.export_report,new View.OnClickListener(){public void onClick(View v){try{status.setText(getString(R.string.report_saved,ProbeLog.export(MainActivity.this,ProbeServices.snapshot(MainActivity.this)).getAbsolutePath()));}catch(Exception e){status.setText(getString(R.string.report_error,ProbeLog.error(e)));}}});
        bind(R.id.exit_probe,new View.OnClickListener(){public void onClick(View v){finish();}});
    }
    private void bind(int id,View.OnClickListener click){findViewById(id).setOnClickListener(click);}
}
