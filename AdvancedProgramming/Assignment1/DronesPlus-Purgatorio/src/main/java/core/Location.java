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
  * Class to hold 2D coordinates and perform simple arithmetics and
  * transformations. 
  * Some methods are there just to fully implement a classic Location class,
  * but are not actually used in the project. 
  * These are left there for future updates and improvements, like drone collisions, etc.
  * 
  * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
  */
public class Location implements Comparable<Location>, Cloneable{
	
    private double x;
    private double y;

    /**
     * Constructor
     * 
     * @param x Initial X-coordinate
     * @param y Initial Y-coordinate
     */
    public Location(double x, double y) {
        setLocation(x,y);
    }


    /**
     * Sets the location of this coordinate object
     * 
     * @param x The x coordinate to set
     * @param y The y coordinate to set
     */
    private void setLocation(double x, double y) {
        this.x = x;
        this.y = y;
    }


    /**
     * Sets this coordinate's location to be equal to other
     * coordinates location
     * 
     * @param c The other coordinate
     */
    public void setLocation(Location c) {
        this.x = c.x;
        this.y = c.y;
    }


    /**
     * Moves the point by dx and dy
     * 
     * @param dx How much to move the point in X-direction
     * @param dy How much to move the point in Y-direction
     */
    public void translate(double dx, double dy) {
        this.x += dx;
        this.y += dy;
    }


    /**
     * Returns the distance to another coordinate
     * 
     * @param other The other coordinate
     * @return The distance between this and another coordinate
     */
    public double distance(Location other) {
        double dx = this.x - other.x;
        double dy = this.y - other.y;

        return Math.sqrt(dx*dx + dy*dy);
    }


    /**
     * Returns the x coordinate
     * 
     * @return x coordinate
     */
    public double getX() {
        return this.x;
    }


    /**
     * Returns the y coordinate
     * 
     * @return y coordinate
     */
    public double getY() {
        return this.y;
    }


    /**
     * Returns a text representation of the coordinate (rounded to 2 decimals)
     * 
     * @return a text representation of the coordinate
     */
    @Override
    public String toString() {
        return String.format("(%.2f,%.2f)", x, y);
    }


    /**
     * Returns a clone of this coordinate
     * 
     * @throws CloneNotSupportedException if super doesn't support clone
     * @return a clone
     */
    @Override
    public Location clone() throws CloneNotSupportedException {
        try {
            Location clone = (Location) super.clone();
            return clone;
        } catch (CloneNotSupportedException e) {
            System.exit(-1);
        }
        return null;
    }


    /**
     * Checks if this coordinate's location is equal to other coordinate's
     * 
     * @param c The other coordinate
     * @return True if locations are the same
     */
    public boolean equals(Location c) {
        if (c == this) {
            return true;
        }
        else {
            return (x == c.x && y == c.y);
        }
    }

    /**
     *
     * @param o The other object
     * @return false if o is null or the actual result of equals((Location) o)
     */
    @Override
    public boolean equals(Object o) {
        if (o == null) 
            return false;
        return equals((Location) o);
    }


    /**
     * Hash code generated from combining the x and y coords
     * 
     * @return a hash code of the String made of the coordinates
     */
    @Override
    public int hashCode() {
        return (x + "," + y).hashCode();
    }


    /**
     * Compares this coordinate to other coordinate.Coordinate whose y
     * value is smaller comes first and if y values are equal, the one with
     * smaller x value comes first.
     * 
     * @param other The other coordinate
     * @return -1, 0 or 1 if this node is before, in the same place or
     * after the other coordinate
     */
    @Override
    public int compareTo(Location other) {
        
        if (this.y < other.y)
            return -1; 
       
        else if (this.y > other.y) 
            return 1;
        
        else if (this.x < other.x)
            return -1;
        
        else if (this.x > other.x) 
            return 1;
        
        else
            return 0;
        
    }
}
