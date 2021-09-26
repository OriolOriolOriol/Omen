
/*
frida-ps -U | grep br
frida -U -p <pid> -l inmemorydexclassloaderhooking.js
*/

// Con objection -> android hooking watch class_method dalvik.system.InMemoryDexClassLoader.$init --dump-args --dump-return
// Importing dentro objection -> evaluate (o trova modo migliore)
Java.perform(function() {
    console.log("Debug");

    const inMemoryDexClassLoader = Java.use('dalvik.system.InMemoryDexClassLoader');
    const byteBufferClass = Java.use('java.nio.ByteBuffer');
    const byteArrClass = Java.use("[B");

    console.log(byteBufferClass.wrap.overload('[B'));

    inMemoryDexClassLoader.$init.overload('java.nio.ByteBuffer','java.lang.ClassLoader').implementation = function(byteBuffer, parent) {
        console.log("[*] InMemoryDexClassLoader constructor");
        // console.log(byteBuffer);
        
        // read the ByteBuffer
        var dim = byteBuffer.remaining();
        // console.log("dimension", dim);
        // var byteArrObject = byteArrClass.$new();
        var byteArrObject = Java.array('byte', new Array(dim).fill(0));
        // console.log("byte obj", byteArrObject);
        byteBuffer.get(byteArrObject);
        // console.log(byteArrObject);

        var result = "[";
        for(var i = 0; i < byteArrObject.length-1; ++i){
            // result+= (String.fromCharCode(byteArrObject[i]));
            // TODO: fix negative values
            result += byteArrObject[i].toString(16) + ",";
        }
        result += byteArrObject[byteArrObject.length-1].toString(16) + "]";
        console.log(result);

        // recreate object
        var newObj = byteBufferClass.wrap(byteArrObject);
        // console.log("New obj", newObj);
        return this.$init(newObj, parent);
  };

});

