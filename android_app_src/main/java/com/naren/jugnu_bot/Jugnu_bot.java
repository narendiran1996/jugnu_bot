package com.naren.jugnu_bot;

import android.support.v7.app.ActionBarActivity;

import android.app.Activity;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.*;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

public class Jugnu_bot extends ActionBarActivity {

    ImageView choc,box,go;
    TextView tv;
    Button emb,canc;
    EditText ipad;
    ArrayList<String> x;
    int count;
    EditText portt;

    public void setstat()
    {
        String xy="CURRENT LIST:"+x.toString();
        tv.setText(xy);
    }
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        setContentView(R.layout.activity_jugnu_bot);
        x=new ArrayList<String>(2);
        count=0;
        choc=(ImageView)findViewById(R.id.iv1);
        box=(ImageView)findViewById(R.id.iv2);
        go=(ImageView)findViewById(R.id.iv3);
        canc=(Button)findViewById(R.id.can);
        tv=(TextView)findViewById(R.id.tv);
        emb=(Button)findViewById(R.id.emb);

        ipad=(EditText)findViewById(R.id.ip);
        portt=(EditText)findViewById(R.id.po);

        choc.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view)
            {
                if (count<1)
                {
                    x.add("CHOCOLATE");
                    setstat();
                    count=count+1;
                }
                else
                {
                    Toast.makeText(getApplicationContext(),"CANT' add more than one item",Toast.LENGTH_SHORT).show();
                }
            }
        });
        box.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view)
            {
                if (count<1)
                {
                    x.add("BOX");
                    setstat();
                    count=count+1;
                }
                else
                {
                    Toast.makeText(getApplicationContext(),"CANT' add more than one item",Toast.LENGTH_SHORT).show();
                }
            }
        });
        emb.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view)
            {
                x=new ArrayList<String>(2);
                setstat();
                count=0;
            }
        });
        go.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view)
            {
                String ad=ipad.getText().toString();
                int po=Integer.parseInt(portt.getText().toString());
                Socket sc;

                DataOutputStream dout= null;

                try {
                    sc=new Socket(ad,po);

                    if (sc.isConnected())
                    {
                        dout = new DataOutputStream(sc.getOutputStream());
                        dout.writeBytes(x.toString());
                        dout.flush();
                        dout.close();
                        sc.close();
                    }

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });

        canc.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view)
            {
                String ad=ipad.getText().toString();
                int po=Integer.parseInt(portt.getText().toString());
                Socket sc;

                DataOutputStream dout= null;

                try {
                    sc=new Socket(ad,po);

                    if (sc.isConnected())
                    {
                        dout = new DataOutputStream(sc.getOutputStream());
                        dout.writeBytes("CANCEL");
                        dout.flush();
                        dout.close();
                        sc.close();
                    }

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }
}
