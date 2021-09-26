package jadx.plugins.input.javaconvert;

import java.nio.file.Path;
import java.util.List;

import jadx.api.plugins.JadxPluginInfo;
import jadx.api.plugins.input.JadxInputPlugin;
import jadx.api.plugins.input.data.ILoadResult;
import jadx.api.plugins.input.data.impl.EmptyLoadResult;
import jadx.plugins.input.dex.DexInputPlugin;

public class JavaConvertPlugin implements JadxInputPlugin {

	@Override
	public JadxPluginInfo getPluginInfo() {
		return new JadxPluginInfo("java-convert", "JavaConvert", "Convert .jar and .class files to dex");
	}

	@Override
	public ILoadResult loadFiles(List<Path> input) {
		ConvertResult result = JavaConvertLoader.process(input);
		if (result.isEmpty()) {
			result.close();
			return EmptyLoadResult.INSTANCE;
		}
		return DexInputPlugin.loadDexFiles(result.getConverted(), result);
	}
}
