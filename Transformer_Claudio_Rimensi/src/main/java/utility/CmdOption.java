package utility;
import org.apache.commons.cli.Option;

public class CmdOption extends Option {
    protected String defaultValue;

    //usato per l'apk path
    public CmdOption(String opt, String longOpt, boolean hasArg, boolean required, String description)
            throws IllegalArgumentException {
        super(opt, longOpt, hasArg, description);
        this.setRequired(required);
    }

    public CmdOption(String opt, String longOpt, boolean hasArg, String description, String defaultValue)
            throws IllegalArgumentException {
        super(opt, longOpt, hasArg, description);
        this.setRequired(false);
        this.defaultValue = defaultValue;
    }
    public String getDefaultValue() {
        if (this.isRequired())
            throw new RuntimeException("Try to retrieve default value from required command line argument");

        return defaultValue;
    }
}
