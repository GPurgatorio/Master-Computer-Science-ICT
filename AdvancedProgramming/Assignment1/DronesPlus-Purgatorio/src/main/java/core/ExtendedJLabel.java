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

import gui.GUIDrones;
import java.awt.Color;
import java.beans.PropertyChangeEvent;
import java.beans.VetoableChangeListener;
import javax.swing.JLabel;

/**
 * An extension of the JLabel class that will be used to show the position of an associated Drone.
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 */
public class ExtendedJLabel extends JLabel implements VetoableChangeListener {
    
    // The random color of the text
    private final Color textColor;
    // Whether the drone is flying or not
    private boolean droneFlying;
    // Whether the drone's takeOff() method succeded or not yet
    private boolean set = false;
    
    public ExtendedJLabel() {
        super();
        // Initially the Drone is flying
        droneFlying = true;
        // Randomly generates a new color (no checks if too bright or anything!)
        textColor = new java.awt.Color((int)(Math.random() * 0x1000000));
        // Sets the color of the text to the randomly generated one
        setForeground(getColor());
    }
    
    /**
     * Gets the color of the text.
     * 
     * @return the randomly generated color for this label
     */
    private Color getColor() {
        return textColor;
    }
    
    /**
     * Creates a string according to the assignment's requests.
     * If flying: &gt; x,y &lt;
     * Otherwise: &lt; x,y &gt;
     * 
     * @param x the x position of the label
     * @param y the y position of the label
     * @return The string to be displayed on top of the label
     */
    private String getStringText(int x, int y) {
        return droneFlying ? (">" + x + "," + y + "<") : ("<" + x + "," + y + ">");
    }
    
    /**
     * Sets the text accordingly to the given location.
     * 
     * @param loc the location to be displayed
     */
    public void setText(Location loc) {
        super.setText(getStringText((int) loc.getX(), (int) loc.getY()));
    }

    /**
     * Method that gets called when a PropertyChangeEvent is fired.
     * (in this case, from the Drone object this label refers to)
     * 
     * @param pce the PropertyChangeEvent that fired
     */
    @Override
    public void vetoableChange(PropertyChangeEvent pce) {
        switch (pce.getPropertyName()) {
            // The referred drone has moved to a new location
            case "loc":
                // Gets the new location and we check if it's still in the panel's bounds
                Location newVal = (Location) pce.getNewValue();
                int x = checkInBounds((int) newVal.getX(), Configurations.SPAWN_AREA_X);
                int y = checkInBounds((int) newVal.getY(), Configurations.SPAWN_AREA_Y);
                
                // Sets the text accordingly to the new given position..
                setText(getStringText(x, y));
                // .. and sets the label on the new position
                setLocation(x,y);
                
                // The takeOff method succeeded, so we won't consider the future vetoables
                set = true;
                
                // Refreshes the JPanel in order to show the update
                GUIDrones.updateGUI();
                break;
                
            // The referred drone must start/stop flying due to an user's click
            case "fly":
                // First, flip-flop the boolean
                droneFlying = !droneFlying;
                
                // Then simply change the direction of the angle brackets according to the assignment's request
                String txt = this.getText();
                setText("<" + txt.substring(1, txt.length()-1) + ">");
                
                // Refreshes the JPanel in order to show the update
                GUIDrones.updateGUI();
                break;
            
            case "esc":
                // If the takeOff hasn't yet succeeded, we move the Label according to the drone
                if(!set) {
                    set = true;
                    Location defaultLoc = (Location) pce.getNewValue();
                    setLocation((int) defaultLoc.getX(), (int) defaultLoc.getY());
                }
                break;
                
            default:
                System.out.println(pce.getPropertyName() + " fired");
                break;
        }
    }
    
    /**
     * Simple check to not allow the label's movement out of bounds.
     * 
     * @param v the value we would like to move to
     * @param max the maximum value we're allowed to move to
     * @return a value, 0 if negative, #max if out of bounds, v otherwise
     */
    private int checkInBounds(int v, int max) {
        return (v < 0) ? 0 : (v > max ? max : v);
    }
}
