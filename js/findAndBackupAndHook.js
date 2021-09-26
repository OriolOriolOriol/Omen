 // frida -U --no-pause -f <package> -l findAndBackupAndHook.js


Java.perform(function() {
    //var txtFile = "C:\\Users\\claud\\OneDrive\\Desktop\\Analisi\\tmp\\log.txt";
    //var file = new File(txtFile);
    //file.open("a");
    var argument;
    const inMemoryDexClassLoader = Java.use('dalvik.system.InMemoryDexClassLoader');
    const byteBufferClass = Java.use('java.nio.ByteBuffer');
    //var file = new File("C:\\Users\\claud\\OneDrive\\Desktop\\Analisi\\tmp\\log.txt","w");
    const hookMainClass = Java.use("lab.galaxy.yahfa.HookMain");

    hookMainClass.findAndBackupAndHook.implementation = function(cls, str1, str2, hook, backup) {
        /*
        console.log("\n[+] findAndBackupAndHook method [+]");
        console.log("Class name", cls.getName());
        console.log("Target method name", str1);
        console.log("Signature", str2);
        console.log("Hook method name", hook);
        
        */
        argument= "Class name: " + cls.getName() + "\n" + "Target method name: " +  str1 + "\n" + "Signature: " + str2 +  "\n" + "Hook method name: " + hook;
        send(argument)
        return this.findAndBackupAndHook(cls, str1, str2, hook, backup);
    };

});