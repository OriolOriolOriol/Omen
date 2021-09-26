package jadx.core.dex.info;

import java.util.*;

import org.jetbrains.annotations.Nullable;

import jadx.api.plugins.input.data.IMethodProto;
import jadx.api.plugins.input.data.IMethodRef;
import jadx.core.codegen.TypeGen;
import jadx.core.dex.instructions.args.ArgType;
import jadx.core.dex.nodes.RootNode;
import jadx.core.dex.nodes.VariableNode;
import jadx.core.utils.Utils;

public final class MethodInfo implements Comparable<MethodInfo> {

	private final String name;
	private final ArgType retType;
	private final List<ArgType> argTypes;
	private final ClassInfo declClass;
	private final String shortId;
	private String alias;
	private Map<String, String> varNameMap;

	private MethodInfo(ClassInfo declClass, String name, List<ArgType> args, ArgType retType) {
		this.name = name;
		this.alias = name;
		this.declClass = declClass;
		this.argTypes = args;
		this.retType = retType;
		this.shortId = makeShortId(name, argTypes, retType);
	}

	public static MethodInfo fromRef(RootNode root, IMethodRef methodRef) {
		InfoStorage infoStorage = root.getInfoStorage();
		int uniqId = methodRef.getUniqId();
		MethodInfo prevMth = infoStorage.getByUniqId(uniqId);
		if (prevMth != null) {
			return prevMth;
		}
		methodRef.load();
		ArgType parentClsType = ArgType.parse(methodRef.getParentClassType());
		ClassInfo parentClass = ClassInfo.fromType(root, parentClsType);
		ArgType returnType = ArgType.parse(methodRef.getReturnType());
		List<ArgType> args = Utils.collectionMap(methodRef.getArgTypes(), ArgType::parse);
		MethodInfo newMth = new MethodInfo(parentClass, methodRef.getName(), args, returnType);
		MethodInfo uniqMth = infoStorage.putMethod(newMth);
		infoStorage.putByUniqId(uniqId, uniqMth);
		return uniqMth;
	}

	public static MethodInfo fromDetails(RootNode root, ClassInfo declClass, String name, List<ArgType> args, ArgType retType) {
		MethodInfo newMth = new MethodInfo(declClass, name, args, retType);
		return root.getInfoStorage().putMethod(newMth);
	}

	public static MethodInfo fromMethodProto(RootNode root, ClassInfo declClass, String name, IMethodProto proto) {
		List<ArgType> args = Utils.collectionMap(proto.getArgTypes(), ArgType::parse);
		ArgType returnType = ArgType.parse(proto.getReturnType());
		return fromDetails(root, declClass, name, args, returnType);
	}

	public String makeSignature(boolean includeRetType) {
		return makeSignature(false, includeRetType);
	}

	public String makeSignature(boolean useAlias, boolean includeRetType) {
		return makeShortId(useAlias ? alias : name,
				argTypes,
				includeRetType ? retType : null);
	}

	public static String makeShortId(String name, List<ArgType> argTypes, @Nullable ArgType retType) {
		StringBuilder sb = new StringBuilder();
		sb.append(name);
		sb.append('(');
		for (ArgType arg : argTypes) {
			sb.append(TypeGen.signature(arg));
		}
		sb.append(')');
		if (retType != null) {
			sb.append(TypeGen.signature(retType));
		}
		return sb.toString();
	}

	public boolean isOverloadedBy(MethodInfo otherMthInfo) {
		return argTypes.size() == otherMthInfo.argTypes.size()
				&& name.equals(otherMthInfo.name)
				&& !Objects.equals(this.shortId, otherMthInfo.shortId);
	}

	public String getName() {
		return name;
	}

	public String getFullName() {
		return declClass.getFullName() + '.' + name;
	}

	public String getFullId() {
		return declClass.getFullName() + '.' + shortId;
	}

	public String getRawFullId() {
		return declClass.makeRawFullName() + '.' + shortId;
	}

	/**
	 * Method name and signature
	 */
	public String getShortId() {
		return shortId;
	}

	public ClassInfo getDeclClass() {
		return declClass;
	}

	public ArgType getReturnType() {
		return retType;
	}

	public List<ArgType> getArgumentsTypes() {
		return argTypes;
	}

	public int getArgsCount() {
		return argTypes.size();
	}

	public boolean isConstructor() {
		return name.equals("<init>");
	}

	public boolean isClassInit() {
		return name.equals("<clinit>");
	}

	public String getAlias() {
		return alias;
	}

	public void setAlias(String alias) {
		this.alias = alias;
	}

	public boolean hasAlias() {
		return !name.equals(alias);
	}

	public synchronized void setVarNameMap(Set<String> names) {
		if (varNameMap == null) {
			varNameMap = new HashMap<>();
		}
		for (String name : names) {
			String[] indexesAndName = name.split(VariableNode.VAR_SEPARATOR);
			if (indexesAndName.length == 2) {
				varNameMap.put(indexesAndName[0], indexesAndName[1]);
			}
		}
	}

	public String getVariableName(String indexes) {
		if (varNameMap != null) {
			return varNameMap.get(indexes);
		}
		return null;
	}

	public boolean hasVarNameMap() {
		return varNameMap != null && varNameMap.size() > 0;
	}

	@Override
	public int hashCode() {
		return shortId.hashCode() + 31 * declClass.hashCode();
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj) {
			return true;
		}
		if (!(obj instanceof MethodInfo)) {
			return false;
		}
		MethodInfo other = (MethodInfo) obj;
		return shortId.equals(other.shortId)
				&& declClass.equals(other.declClass);
	}

	@Override
	public int compareTo(MethodInfo other) {
		int clsCmp = declClass.compareTo(other.declClass);
		if (clsCmp != 0) {
			return clsCmp;
		}
		return shortId.compareTo(other.shortId);
	}

	@Override
	public String toString() {
		return declClass.getFullName() + '.' + name
				+ '(' + Utils.listToString(argTypes) + "):" + retType;
	}
}
