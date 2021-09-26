package utility;

import soot.*;
import soot.javaToJimple.LocalGenerator;
import soot.jimple.*;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public  class Base_Transformer {

    public Base_Transformer() {}
    /**
     * Transform all protected and private fields or methods in public ones.
     *
     * @param units The iterator over a list of units
     */
    public void makeAllPublic(Iterator<Unit> units) {
        while (units.hasNext()) {
            Stmt stmt = (Stmt) units.next();
            if (stmt.containsInvokeExpr() &&
                    (stmt.getInvokeExpr() instanceof SpecialInvokeExpr || stmt.getInvokeExpr() instanceof StaticInvokeExpr ||
                            stmt.getInvokeExpr() instanceof VirtualInvokeExpr || stmt.getInvokeExpr() instanceof InterfaceInvokeExpr)) {
                UnitHelper.makePublic(stmt.getInvokeExpr().getMethod());
            }
            if (stmt.containsFieldRef()) {
                //TODO: check if remove final or not TransformerHelper.removeFinal(originStmt.getFieldRef().getField());
                UnitHelper.makePublic(stmt.getFieldRef().getField());
            }
        }
    }

    /**
     * This methods create a new class (named 'newClassName') with a method (named 'newMethodName') which have the same input body.
     *
     * @param body The wanted body
     * @param newClassName The new class name
     * @param newMethodName The new method name
     *
     * @return The body of the new method
     */
    public Body extractMethodBody(Body body, String newClassName, String newMethodName) { //}, boolean wrapPrimitiveTypes) {
        SootMethod originMethod = body.getMethod();

        // Create a new method
        List<Type> params = new ArrayList<>();
        if (!originMethod.isStatic()) {
            params.add(body.getThisLocal().getType());
        }
        params.addAll(originMethod.getParameterTypes());
        SootMethod extractedMethod = new SootMethod(newMethodName, params, originMethod.getReturnType(), Modifier.PUBLIC | Modifier.STATIC);

        // Create a new class
        SootClass extractedClass = new SootClass(newClassName, Modifier.PUBLIC);
        extractedClass.setSuperclass(Scene.v().getObjectType().getSootClass());
        extractedMethod.setDeclaringClass(extractedClass);
        extractedClass.addMethod(extractedMethod);

        // Create a new body
        Body extractedBody = Jimple.v().newBody();
        extractedBody.setMethod(extractedMethod);
        extractedMethod.setActiveBody(extractedBody);

        if (originMethod.isStatic()) {
            extractedBody.getLocals().addAll(body.getLocals());
            extractedBody.getUnits().addAll(body.getUnits());
        } else {
            // Insert all original local, renaming the 'this' local
            Local newThisLocal = null;
            for (Iterator<Local> locals = body.getLocals().snapshotIterator(); locals.hasNext(); ) {
                Local local = locals.next();

                if (local.equals(body.getThisLocal())) {
                    local.setName("$nl0");
                    newThisLocal = local;
                }

                extractedBody.getLocals().addLast(local);
            }

            // Insert all original unit, removing the init of 'this' object
            for (Iterator<Unit> units = body.getUnits().snapshotIterator(); units.hasNext(); ) {
                Stmt stmt = (Stmt) units.next();

                if (stmt instanceof IdentityStmt) {
                    if (((IdentityStmt) stmt).getLeftOp().equals(body.getThisLocal())) {
                        extractedBody.getUnits().addLast(Jimple.v().newIdentityStmt(newThisLocal,
                                Jimple.v().newParameterRef(newThisLocal.getType(), 0)));
                        continue;
                    } else if (((IdentityStmt) stmt).getRightOp() instanceof ParameterRef) {
                        // increase the number of the params
                        ParameterRef parameterRef = (ParameterRef) ((IdentityStmt) stmt).getRightOp();
                        extractedBody.getUnits().addLast(Jimple.v().newIdentityStmt(((IdentityStmt) stmt).getLeftOp(),
                                Jimple.v().newParameterRef(((IdentityStmt) stmt).getLeftOp().getType(), parameterRef.getIndex() + 1)));
                        continue;
                    }
                }

                extractedBody.getUnits().addLast(stmt);
            }
        }

        // Insert all traps
        extractedBody.getTraps().addAll(body.getTraps());
        extractedMethod.setDeclared(true);

        // Validate body
        extractedBody.validate();

        return extractedBody;
    }

    public Body assignEmptyBody(SootMethod originMethod) {
        Body newBody = Jimple.v().newBody();
        newBody.setMethod(originMethod);
        originMethod.setActiveBody(newBody);

        if (!originMethod.isStatic()) {
            // Create a dummy this local variable
            Local thisLocal = Jimple.v().newLocal("r0", originMethod.getDeclaringClass().getType());
            newBody.getLocals().addFirst(thisLocal);
            newBody.getUnits().addFirst(
                    Jimple.v().newIdentityStmt(thisLocal, Jimple.v().newThisRef(RefType.v(originMethod.getDeclaringClass()))));
        }

        // Create dummies local for each input parameters
        int index = 0;
        for(Type parameterType : originMethod.getParameterTypes()) {
            Local local = (new LocalGenerator(newBody)).generateLocal(parameterType);// Jimple.v().newLocal("r0", originMethod.getDeclaringClass().getType());
            newBody.getUnits().addLast(
                    Jimple.v().newIdentityStmt(local, Jimple.v().newParameterRef(parameterType, index++)));
        }

        return newBody;
    }
}
