/*
 * Copyright (C) 2019 Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package logging;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import config.Configurations;

/**
 * Creates a Thread that will call the specified command in the CMD (Windows) or shell (Unix).
 * The given command will be repeated a given number of times: if there's no need for cycles,
 * just specify the 2nd parameter as a 0 or as a negative number.
 *
 * Tested on:
 *      Windows 10
 *      MacOs Mojave v.10
 *      Arch Linux
 *
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 */
public class CmdExecuter extends Thread {

    /** The command to be executed */
    private final String command;
    /** The number of times to repeat the given command */
    private int iterNum;
    /** Cycle's delta time (seconds) */
    private final int refreshRate;
    /** If the OS running this program is Windows */
    private final boolean isWindows;

    /**
     * Constructor
     *
     * @param commandToExecute the command that will be executed in the CMD
     * @param numOfCycles the number of times that the command should be repeated
     * @param secondsToCycle cycle's delta time (ms)
     * @param isWindows if the hosting machine has Windows as the OS
     */
    public CmdExecuter(String commandToExecute, int numOfCycles, int secondsToCycle, boolean isWindows) {
        command = commandToExecute;
        iterNum = numOfCycles;
        if(numOfCycles > 0)
            refreshRate = secondsToCycle * 1000;
        else
            refreshRate = 0;
        this.isWindows = isWindows;
    }


    public void run() {

        /* We build a process that opens a terminal and then calls the command */
        ProcessBuilder pb;
        if(isWindows)
            pb = new ProcessBuilder("cmd", "/c", command);
        else
            pb = new ProcessBuilder("sh", "-c", command);

        /* Note: if refreshRate > 0, this is an endless cycle. Terminate it with CTRL + C */
        do {

            iterNum--;

            // Day_Month-Hour(24)_Minute
            SimpleDateFormat s = new SimpleDateFormat(Configurations.LOG_FORMAT);
            String timestamp = s.format(new Date());

            /* Creates the log file */
            File log = new File(Configurations.LOG_DIRECTORY + timestamp + Configurations.LOG_EXTENSION);

            try {
                if (!log.exists())
                    log.createNewFile();
            } catch(IOException e) { System.err.println("Error while creating the log file " + timestamp); break;}

            /* Redirects the output to the log file */
            pb.redirectOutput(ProcessBuilder.Redirect.to(log));

            /* Starts the process and waits for it to finish */
            try {
                Process p = pb.start();
                p.waitFor();

                /* Waits the specified time */
                if(refreshRate > 0 && iterNum > 0)
                    Thread.sleep(refreshRate);
            }
            catch (Exception e) { System.err.println(e.getMessage()); break; }

        } while(iterNum > 0);

        System.out.println("Thread terminating..");
    }
}
