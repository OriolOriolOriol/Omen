  
/*
 * raptor_frida_android_enum.js - Java class/method enumerator
 * Copyright (c) 2017 Marco Ivaldi <raptor@0xdeadbeef.info>
 *
*/
/*
Java.perform(function() {
	var hook;
	var targetClass = "lab.galaxy.yahfa.HookMain";
	try{
		send('[AUXILIARY] Getting Methods and Implementations of Class: ' + targetClass)
		hook = Java.use(targetClass);
	} catch (err){
		send('[AUXILIARY] Hooking ' + targetClass + ' [\"Error\"] => ' + err);
		return;
	}
	var methods = hook.class.getDeclaredMethods();
	hook.$dispose;
	methods.forEach(function(method) { 
		send('[AUXILIARY] ' + method)
	});
	
});
*/
Java.perform(function() {
	var classes = Java.enumerateLoadedClassesSync();
	send('[AUXILIARY] Loaded Classes');
	classes.forEach(function(aClass) {
		try{
			var className = aClass.match(/[L](.*);/)[1].replace(/\//g, ".");
			send('[AUXILIARY] ' + className);
		}
		catch(err){}
	});
});