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

import config.Configurations;

/**
 * I've used this class to solve the Midterm from the PeerToPeer&Blockchain's course (2019-2020).
 * The Midterm's infos can be read in the associated copy of the PDF.
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 */
public class CmdLogger {

    public static void main(String[] args) {

        // Creates the reports folder, where all logs will be stored
        File dir = new File("reports" + File.separator);
        if (!dir.exists())
            dir.mkdir();

        String os = System.getProperty("os.name");
        CmdExecuter ce;

        // Checks if Windows is the OS of the running machine
        if(os.toLowerCase().contains("windows"))
            ce = new CmdExecuter(Configurations.COMMAND, Configurations.NUM_OF_CYCLES, Configurations.SECONDS_TO_CYCLE, true);

        // Checks if it's Linux or Mac (Unix)                   NOTE: not tested yet
        else if (os.toLowerCase().contains("nix") || os.toLowerCase().contains("mac"))
            ce = new CmdExecuter(Configurations.COMMAND, Configurations.NUM_OF_CYCLES, Configurations.SECONDS_TO_CYCLE, false);

        else {
            System.err.println("OS not supported: " + os);
            return;
        }

        // Note: it assumes that the ipfs daemon is running
        ce.start();
    }
}
