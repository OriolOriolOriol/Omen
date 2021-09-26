package Main_function_Transformer;

import soot.javaToJimple.LocalGenerator;
import soot.jimple.AssignStmt;
import soot.jimple.ClassConstant;
import soot.jimple.Jimple;
import soot.jimple.Stmt;
import org.json.simple.JSONObject;
import soot.*;
import utility.Base_Transformer;
import utility.Print_dex;
import utility.Random_choice;
import utility.UnitHelper;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class Extractor extends BodyTransformer{
    private final String apk;
    private final String androidJar;
    private final String output_Path;
    private final String package_name;
    private final File signaturesFile;
    private int percentuale_extrazione;
    JSONObject obj = new JSONObject();

    public Extractor(String package_name,String apk, String androidJar, int percentuale_extrazione, String output_file) {
        //System.out.println("1-Avvio del modulo Extractor...");
        if (percentuale_extrazione < 0 || percentuale_extrazione > 100) {
            throw new IllegalArgumentException("The chance of extract a method must be between 0% and 100%");
        }
        this.apk = apk;
        this.androidJar = androidJar;
        this.output_Path = output_file;
        this.package_name=package_name;
        this.percentuale_extrazione=percentuale_extrazione;
        this.signaturesFile = new File(output_file + "/signatures");

        // create directory(Outcomes) if not exists
        File directory = new File(output_file);
        if (!directory.exists()) {
            directory.mkdirs();
        } else {
            // overwrite content of signature file
            try {
                BufferedWriter bw = new BufferedWriter(new FileWriter(signaturesFile, false));
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

        if (!checkMethod(b.getMethod())) { // TODO: check how method are choosen and if $ (inner classes) can be considered
            return;
        }
        if(Random_choice.checkChance(percentuale_extrazione)) {
                SootMethod metodo_originale = b.getMethod();
                System.out.println("Transforming method --> " + metodo_originale.getName() + " of class " + metodo_originale.getDeclaringClass().getName());
                String nuovo_nome_classe= metodo_originale.getDeclaringClass() + metodo_originale.getName().replace("<", "").replace(">","") ;
                //System.out.println(nuovo_nome_classe);
                String folder = UUID.randomUUID().toString().replace("-", "");
                // write to file -> get lock
                synchronized (signaturesFile) {
                try {

                    BufferedWriter bw =  new BufferedWriter(new FileWriter(signaturesFile, true));
                    String bytecodeSignature = metodo_originale.getBytecodeSignature();
                    //elimini '<' e '>' dalla bytecodesignature
                    String bytecode_modified= bytecodeSignature.substring(1,bytecodeSignature.length()-1);
                    obj.put("Name_Class",nuovo_nome_classe);
                    obj.put("Bytecode_Signature",bytecode_modified);
                    obj.put("Folder",folder);
                    bw.write(obj.toJSONString());
                    bw.newLine();
                    bw.flush();
                    bw.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            /**
             * 1-Prendo il body dei metodi che sono stati presi a random
             **/
            Base_Transformer base= new Base_Transformer();
            base.makeAllPublic(b.getUnits().snapshotIterator());
            // Extract body and print it to a dex file
            SootClass extractedClass=  (base.extractMethodBody(b, nuovo_nome_classe, "hook")).getMethod().getDeclaringClass();
             //extractedClass = br.com.cjdinfo.puzzle.MainActivitysalvaJogo

            // Add the 'myClass' static field on extractedClass
            SootField myClassField =
                    new SootField("myClass", Scene.v().getSootClass("java.lang.Class").getType(), Modifier.STATIC | Modifier.PUBLIC);
            extractedClass.addField(myClassField);

            // Init static field -> add a static constructor
            SootMethod classInitializer = new SootMethod("<clinit>", Collections.emptyList(), VoidType.v(), Modifier.STATIC);
            extractedClass.addMethod(classInitializer);
            Body classInitializerBody = Jimple.v().newBody(classInitializer);
            //System.out.println(classInitializerBody);
            /**
            mi stampa questo:
             static void <clinit>()
             {
             }
             Uno per ciascun metodo estratto
            * **/
            classInitializer.setActiveBody(classInitializerBody);

            classInitializerBody.getUnits().addLast(Jimple.v().newAssignStmt(
                    Jimple.v().newStaticFieldRef(myClassField.makeRef()),
                    ClassConstant.fromType(extractedClass.getType())));

            //System.out.println(classInitializerBody);
            /**
             * static void <clinit>()
             *     {
             *         <br.com.cjdinfo.puzzle.AdsMobinitBanner: java.lang.Class myClass> = class "Lbr/com/cjdinfo/puzzle/AdsMobinitBanner;";
             *     }
             * **/
            classInitializerBody.getUnits().addLast(Jimple.v().newReturnVoidStmt());
            classInitializerBody.validate();
            // Print the corresponding dex to file(mi salva il body dei metodi qui dentro)
            Print_dex dexPrinter = new Print_dex(output_Path, folder);
            dexPrinter.add(extractedClass);
            dexPrinter.writeToFile();

            /**
             * 2-Ora inserisco una runtimeException al posto dei body dei metodi estratti
             **/
            Body newBody = base.assignEmptyBody(metodo_originale);

            // Create throw stmt
            RefType type = RefType.v("java.lang.RuntimeException");

            // Init new throw local and insert in the new Body
            Local throwLocal = (new LocalGenerator(newBody)).generateLocal(type);
            Value rValue = UnitHelper.getInitValue(type);
            AssignStmt initLocalVariable = Jimple.v().newAssignStmt(throwLocal, rValue);
            newBody.getUnits().addLast(initLocalVariable);

            // Create units
            Stmt newStmt = Jimple.v().newAssignStmt(throwLocal, Jimple.v().newNewExpr(type));
            Stmt invStmt = Jimple.v().newInvokeStmt(Jimple.v().newSpecialInvokeExpr(throwLocal,
                    Scene.v().getMethod("<java.lang.RuntimeException: void <init>()>").makeRef()));
            Stmt throwStmt = Jimple.v().newThrowStmt(throwLocal);

            newBody.getUnits().addLast(newStmt);
            newBody.getUnits().addLast(invStmt);
            newBody.getUnits().addLast(throwStmt);

            // Validate method
            newBody.validate();
        }//chiusura if
    }//chiusura metodo internalTransform

    /**
        * Controlla se il metodo di input appartiene al package name e se non è un costruttore o un metodo ereditato
        *
        * @param method: L'input è il metodo che viene controllato
        * @return true Se il metodo è conforme ai criteri altrimenti ritorna false
     */

    protected boolean checkMethod(SootMethod method) {
        // filter for package name
        if (!method.getDeclaringClass().getName().contains(package_name))
            return false;

        // check if it a constructor
        if (method.getName().contains("<init>")) // TODO: handle also constructors
            return false;

        // TODO: check if 'this' class is an android class!

        // check if method is not inheredit from superClass
        SootClass superClass = method.getDeclaringClass().getSuperclass();
        while(true) {

            try {
                superClass.getMethod(method.getSubSignature());
                return false;
            } catch (Exception e) {
                ;
            }

            if (superClass.getName().equals("java.lang.Object"))
                break;

            superClass = superClass.getSuperclass();
        }

        return true;
    }


}