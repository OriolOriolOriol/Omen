import Main_function_Transformer.Extractor;
import Main_function_Transformer.Injector;
import org.apache.commons.cli.*;
import org.apache.commons.io.FileUtils;
import soot.*;
import utility.CmdOption;
import utility.ManifestHelper;

import java.io.File;
import java.util.*;

public class Main {
    public static final String[] CMD_ARGUMENTS = {"android-jars","apk-path","extractor-chance","output_path","soot-classpath","run-injector"};
    public static String percentuale_extractor="";
    public static String apk="";
    public static String androidJar="";
    public static String output_path="";
    public static String package_name="";
    public static Boolean injector;
    public static String injector_stringa="";
    public static ArrayList<String> lista_parametri;
    public static void main(String[] args){

            System.out.println("Lista parametri passati...");
            lista_parametri=List_opzioni(args);
            try {
                System.out.println("Avvio configurazioni iniziali...");
                injector=Boolean.parseBoolean(injector_stringa);
                setupSoot(apk, androidJar, output_path);
                package_name = ManifestHelper.getPackageName(apk);
                /**
                 * Delete dir when running the Transformer again
                 * **/
                File directory = new File(output_path);
                if (directory.exists()) {
                    FileUtils.deleteDirectory(directory);
                }
                System.out.println("Operation completed :)");
            }catch (Exception e){
                System.err.println("Error during the configurations" + e);
            }

            Extractor extractor = new Extractor(package_name, apk, androidJar, Integer.parseInt(percentuale_extractor), output_path);
            PackManager.v().getPack("jtp").add(new Transform("jtp.methodExtractor", extractor));

            if(injector==true){
                Injector injector=new Injector(package_name,output_path);
                PackManager.v().getPack("jtp").add(new Transform("jtp.injectControls", injector));
            }
            //è questo il metodo che mi fa avviare internalTransform di extractor e gli altri
            PackManager.v().runPacks();

            System.out.println("Creation of protect APK...");
            //Crea l'apk modificato  in cui sono state apportate le modifiche
            PackManager.v().writeOutput();
        }


    public static void setupSoot(String apk, String androidJar, String output_Path) {
        G.reset();
        // Generic options
        soot.options.Options.v().set_allow_phantom_refs(true);
        soot.options.Options.v().set_whole_program(true);
        soot.options.Options.v().set_prepend_classpath(true);
        //Read (Apk Dex-to-Jimple) Options
        soot.options.Options.v().set_android_jars(androidJar); // The path to Android Platforms
        soot.options.Options.v().set_src_prec(soot.options.Options.src_prec_apk); // Determine the input is an APK
        soot.options.Options.v().set_process_dir(Collections.singletonList(apk)); // Provide paths to the APK
        soot.options.Options.v().set_process_multiple_dex(true);  // Inform Dexpler that the APK may have more than one .dex files
        soot.options.Options.v().set_include_all(true);
        // Write (APK Generation) Options
        soot.options.Options.v().set_output_format(soot.options.Options.output_format_dex);
        soot.options.Options.v().set_output_dir(output_Path);
        soot.options.Options.v().set_validate(true); // Validate Jimple bodies in each transofrmation pack
        // Resolve required classes
        Scene.v().addBasicClass("java.io.PrintStream", SootClass.SIGNATURES);
        Scene.v().addBasicClass("java.lang.System", SootClass.SIGNATURES);
        Scene.v().loadNecessaryClasses();
    }

    private static org.apache.commons.cli.Options getOptions() {

        String pattern="C:\\Users\\claud\\OneDrive\\Desktop";
        //path AndroidJar
        Option optionAndroidJar = new CmdOption("a","android-jars",true,true,
                "The path to the android jars. The default is '$HOME/Android/Sdk/platforms'");

        //path apk file
        Option optionApkPath = new CmdOption("i","apk-path",true,true,
                "The path to the target apk file.");

        //Percentuale metodi estratti (valore di default che è 20)
        Option optionExtractorChance = new CmdOption("ex","extractor-chance",true,
                "The percentage to extract a method. The default value is 20%", "20");

        Option output_path = new CmdOption("o","output_path",true,
                "The percentage to extract a method. The default value is 20%", pattern);

        Option optionClasspath = new CmdOption("c","soot-classpath",true,
                "The path to the wanted soot.jar file.",
                Scene.v().defaultClassPath() + ";" + Main.class.getProtectionDomain().getCodeSource().getLocation().getPath() + ";");

        Option injectors=new CmdOption("ri","run-injector",true,"Flag that enable the injector module. The default value is false", "false");


        org.apache.commons.cli.Options options = new org.apache.commons.cli.Options();
        options.addOption(optionAndroidJar);
        options.addOption(optionApkPath);
        options.addOption(optionExtractorChance);
        options.addOption(output_path);
        options.addOption(optionClasspath);
        options.addOption(injectors);

        return options;

    }


    public static ArrayList<String> List_opzioni(String[] args){
        ArrayList<String> lista_finale= new ArrayList<>();

        //lavoro sugli argomenti da passare al programma
        org.apache.commons.cli.Options options = getOptions();

        CommandLineParser parser = new DefaultParser();//parsa gli argomenti passati nel gradle
        Map<String, String> argomenti = new HashMap<>();//li associ
        try {
            CommandLine cmdLine = parser.parse(options, args);
            //ciclo le opzioni che mi sono state passate,ti permette di associare ciò che hai inserito nel gradle con il nome dell'opzione
            for(org.apache.commons.cli.Option opt : options.getOptions()) {
                if(opt.isRequired())
                    argomenti.put(opt.getLongOpt(), cmdLine.getOptionValue(opt.getOpt()));
                else
                    argomenti.put(opt.getLongOpt(), cmdLine.getOptionValue(opt.getOpt(), ((CmdOption) opt).getDefaultValue()));
            }
            //Listo gli argomenti passati e tiro fuori quello che mi serve per l'extractor
            int count=1;
            System.out.println("===========================================");
            for (Map.Entry<String, String> entry : argomenti.entrySet()) {
                System.out.println(count+ ")" + " " +  entry.getKey()+":"+ entry.getValue());
                if(entry.getKey().equals(CMD_ARGUMENTS[2]))
                    percentuale_extractor=entry.getValue();
                if(entry.getKey().equals(CMD_ARGUMENTS[1]))
                    apk=entry.getValue();
                if(entry.getKey().equals(CMD_ARGUMENTS[0]))
                    androidJar=entry.getValue();
                if(entry.getKey().equals(CMD_ARGUMENTS[3]))
                    output_path=entry.getValue();
                if(entry.getKey().equals(CMD_ARGUMENTS[5]))
                    injector_stringa= entry.getValue();

                count++;
            }
            System.out.println("===========================================");
        }catch (ParseException e) {
            //Fa il check che si inseriscono gli argomenti
            System.err.println("Error on parsing options: " + e.getMessage());
            System.exit(1);
        }

        lista_finale.add(percentuale_extractor);
        lista_finale.add(apk);
        lista_finale.add(androidJar);
        lista_finale.add(output_path);
        lista_finale.add(injector_stringa);

        return lista_finale;

        }


}//chiusura Classe Main

