package config;

import java.io.File;

public class Configurations {

    // If it's true it'll start to send requests to URL_GEOLOC
    public static final boolean MAKE_HTTP_REQUESTS = false;

    // NOTE: nearly 1500 requests required around 6 minutes
    public static final String URL_GEOLOC = "http://api.ipstack.com/";

    /** Change it to your access key to see the geolocalization */
    public static final String YOUR_ACCESS_KEY = "YOUR_ACCESS_KEY_HERE";

    // The command to execute in the bash
    public static String COMMAND = "ipfs swarm peers -v";
    public static int NUM_OF_CYCLES = 10;
    public static int SECONDS_TO_CYCLE = 300;

    // Some formats
    public static final String LOG_EXTENSION = ".txt";
    public static final String LOG_FORMAT = "dd_MM-HH_mm";

    // Paths
    public static final String LOG_DIRECTORY = "reports" + File.separator;
    public static final String IPSTACK_DIRECTORY = "geoloc" + File.separator;
    public static final String OUT_DIRECTORY = "generatedFiles" + File.separator;

    // What is considered to be a "Fast" peer (in ms)
    public static final int LATENCY_FAST = 300;
    // What is considered to be a not fast but not slow peer (in ms)
    public static final int LATENCY_MEDIUM = 1000;

    // Enables some prints during execution
    public static final boolean DEBUG = false;
}
