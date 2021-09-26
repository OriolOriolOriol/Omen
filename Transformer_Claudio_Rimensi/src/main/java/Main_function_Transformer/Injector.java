package Main_function_Transformer;

import soot.*;
import soot.jimple.IdentityStmt;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Iterator;
import java.util.Map;

public class Injector extends BodyTransformer {
    private final String packageName;
    private final File injectorDetailsFiles;

    public Injector(String packageName, String outputFolder) {
        //System.out.println("2-Avvio del modulo Injector...");
        this.packageName = packageName;
        this.injectorDetailsFiles = new File(outputFolder + "/injectorDetails");

        // create directory if not exists
        File directory = new File(outputFolder);
        if (!directory.exists()){
            directory.mkdirs();
        } else {
            // overwrite content of signature file
            try {
                BufferedWriter bw = new BufferedWriter(new FileWriter(this.injectorDetailsFiles, false));
                bw.write("");
                bw.flush();
                bw.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    protected void internalTransform(Body b, String phaseName, Map<String, String> options) {

        // filter dummy functions (e.g., syncronized, constructors, ecc..)
        if (!checkMethod(b.getMethod())) {
            return;
        }

        for(Iterator<Unit> iter=b.getUnits().snapshotIterator();iter.hasNext(); ){
            //java.util.LinkedList$ListItr@6a99eed (non so cosa sia)
            System.out.println(iter);
            // Insert the check after all identify stmt (this object and params)
            Unit unit = iter.next();
            if (unit instanceof IdentityStmt) {
                continue;
            }

        }

    }



    protected boolean checkMethod(SootMethod method) {
        // filter for package name
        if (!method.getDeclaringClass().getName().contains(packageName))
            return false;

        // check if it a constructor
        if (method.getName().contains("<init>"))
            return false;

        // Ignore synchronized methods
        if (method.isSynchronized() || ((method.getModifiers() & Modifier.DECLARED_SYNCHRONIZED) == Modifier.DECLARED_SYNCHRONIZED))
            return false;

        // TODO: Ignore methods of application class (like protector)

        // Ignore static constructor methods
        if (method.getName().contains("<clinit>"))
            return false;

        return true;
    }
}
