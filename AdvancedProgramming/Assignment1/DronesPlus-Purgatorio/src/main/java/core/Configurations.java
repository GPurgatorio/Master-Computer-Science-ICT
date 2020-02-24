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
package core;

/**
 * Class for many useful and global variables and/or settings.
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 */
public class Configurations {
    
    /** Every how many milliseconds the drones have to move. */
    public static final int REFRESH_RATE = 1000;
    
    /** Prints out some useful infos during the execution. */
    public static final boolean DEBUG = false;
    
    // The panel's dimensions
    public static final int PANEL_WIDTH = 450;
    public static final int PANEL_HEIGHT = 450;
    
    // The label's dimensions
    public static final int LABEL_WIDTH = 75;
    public static final int LABEL_HEIGHT = 20;
    
    // The area where the drones can spawn (must be lower than panel's dimension!)
    public static final int SPAWN_AREA_X = PANEL_WIDTH - LABEL_WIDTH;
    public static final int SPAWN_AREA_Y = PANEL_HEIGHT - LABEL_HEIGHT;
    
}
