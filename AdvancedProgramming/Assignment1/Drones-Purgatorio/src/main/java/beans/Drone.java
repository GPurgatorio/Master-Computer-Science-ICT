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

package beans;

import core.Configurations;
import core.Location;
import java.beans.*;
import java.io.Serializable;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

/**
 * A class representing the Drone that will move around the simulated world.
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail dot com>
 */
public class Drone implements Serializable {
    
    /** The property "loc", for location's purposes. */
    public static final String PROP_LOC_PROPERTY = "loc";
    /** The property "fly", for flying's updates. */
    public static final String PROP_FLY_PROPERTY = "fly";
    
    // The location of where the Drone actually is
    private Location loc;
    // Whether the Drone is flying or not
    private boolean flying;
    // Timer that will handle the various TimerTasks of this Drone
    private Timer timer;
    
    // The two PropertyChangeSupport, in order to notify subscribers about changes in "loc"/"fly"
    private final PropertyChangeSupport dronePropertySupport;
    
    /**
     * Constructor
     * @param initLoc the position where to start
     */
    public Drone(Location initLoc) {
        dronePropertySupport = new PropertyChangeSupport(this);
        takeOff(initLoc);
    }
    
    
    /**
     * Starts the drone. 
     * Until the drone's stopped, it will move to a new position every #Configurations.REFRESH_RATE milliseconds
     */
    private void takeOff(Location initLoc) {
        
        print("Drone started flying!");
        
        // "takeOff(initLoc), that sets flying to true, initializes loc to initLoc, 
        // and sets up a Timer to generate a new location for the drone each second"
        flying = true;
        loc = initLoc;
        timer = new Timer();

        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                move();
            }
        }, 0, Configurations.REFRESH_RATE);
    }
    
    
    /**
     * Stops the drone by removing the TimerTasks.
     * Note, the drone won't restart.
     */
    public void land() {
        
        // "land(), that stops the timer, sets flying to false and leaves loc unchanged."
        if(flying) {
            print("Drone stopped flying!");
            flying = false;
            timer.cancel();
            dronePropertySupport.firePropertyChange(PROP_FLY_PROPERTY, true, flying);
        }
    }
    
    
    /**
     * Randomly moves the drone around its actual position.
     * "(with a displacement in each direction within -10 and +10)"
     */
    public void move() {
        Random rand = new Random();
        int sign = 1;
        
        if(rand.nextBoolean())
            sign = -sign;
        double dx = sign * rand.nextDouble() * 10;
        
        if(rand.nextBoolean())
            sign = -sign;
        double dy = sign * rand.nextDouble() * 10;
        
        setLocProperty(dx, dy);
    }
    
    
    /** Returns the actual position of the Drone.
     * @return A location */
    public Location getLocProperty() {
        return this.loc;
    }
    
    
    /**
     * Returns true if the drone is flying, false otherwise.
     * @return A boolean
     */
    public boolean isFlying() {
        return this.flying;
    }
    
    
    /**
     * Changes the location of the Drone by the given parameters and fires a PropertyChangeEvent.
     * Note: the Location class MUST support the clone() method.
     * @param dx the amount of shift in the x-axis
     * @param dy the amount of shift in the y-axis
     */
    private void setLocProperty(double dx, double dy) {
        try {
            Location oldValue = loc.clone();
            loc.translate(dx, dy);
            dronePropertySupport.firePropertyChange(PROP_LOC_PROPERTY, oldValue, this.loc);
            print("A PropertyChangeEvent has been fired");
        }                                                           
        catch(CloneNotSupportedException e) { System.err.println("The Location class doesn't support the clone() method!"); }
    }
    
    
    /**
     * Adds a new listener to the PropertyChangeListener.
     * @param listener the listener
     */
    public void addPropertyChangeListener(PropertyChangeListener listener) {
        dronePropertySupport.addPropertyChangeListener(listener);
    }
    
    
    /**
     * Removes an already existing listener from the specified PropertyChangeListener.
     * @param listener the listener
     */
    public void removePropertyChangeListener(PropertyChangeListener listener) {
        dronePropertySupport.removePropertyChangeListener(listener);
    }
    
    
    /** 
     * Simple beautify of the code to call a standard print
     * @param s the string to print
     */
    private void print(String s) {
        if (Configurations.DEBUG)
            System.out.println(s);
    }
    
}
