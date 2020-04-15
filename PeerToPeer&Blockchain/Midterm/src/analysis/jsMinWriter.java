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

package analysis;

import config.Configurations;

import java.io.*;

/**
 * Creates a minified JS file using the Plotly library and syntax.
 */
public class jsMinWriter extends Thread {

    private final String[] locations;
    private final String[] locLong;
    private final int[] quantities;
    private final String[] stats;
    private final int[] statValue;
    private final int[] newPeersPerHour;
    private final int[] totPeersPerHour;


    /**
     * Constructor
     *
     * @param fullNameCountries the countries' names, long version (e.g. Italy)
     * @param alpha3 the countries' ISO 3166-1 alpha-3 version (e.g. ITA)
     * @param countriesSize the number of peers per country (relation 1:1 with fullNameCountries)
     * @param statsToPrint the stats to show in the General Stats
     * @param statValues the values to show in the General Stats (relation 1:1 with statsToPrint)
     * @param newPerHour the number of new peers met at time i
     * @param totPerHour the total number of peers at time i
     */
    public jsMinWriter(String[] fullNameCountries, String[] alpha3, int[] countriesSize, String[] statsToPrint,
                       int[] statValues, int[] newPerHour, int[] totPerHour) {
        locLong = fullNameCountries;
        locations = alpha3;
        quantities = countriesSize;
        stats = statsToPrint;
        statValue = statValues;
        newPeersPerHour = newPerHour;
        totPeersPerHour = totPerHour;
    }


    /**
     * Creates a minified version of a JavaScript file using Plotly with the given data.
     *
     * Note: this code is not meant to be too much human-friendly due to the "minimization" part.
     * It was used just because the JS depended only on raw data that changed many times!
     */
    public void run() {

        int tot = 0, max = 0;
        int commasCheck = 0;
        int size;
        File js;
        FileWriter fw;

        if((size = totPeersPerHour.length) != newPeersPerHour.length) {
            print("Length is different, can't parse correctly.");
            return;
        }

        File dir = new File(Configurations.OUT_DIRECTORY);
        if(!dir.exists())
            dir.mkdir();

        try {
            js = new File(Configurations.OUT_DIRECTORY + "generatedPlotly.js");
            if (!js.exists())
                js.createNewFile();
            fw = new FileWriter(js);
        }
        catch(IOException e) { print("Error while creating file[writer]: " + e.getMessage()); return; }

        // Used for the World Chart
        String worldData = "var data = [{type:'scattergeo', mode:'markers', locations:[";

        // Used for the Pie Chart
        String pieData = "var data2 = [{type:\"pie\", labels:[";

        for(String loc : locations) {
            commasCheck++;

            worldData += "\'" + loc + "\'";
            // Append a comma if it's not the last element
            if(commasCheck != locations.length)
                worldData += ",";
        }

        commasCheck = 0;
        for(String loc : locLong) {
            commasCheck++;

            pieData += loc;
            // Append a comma if it's not the last element
            if(commasCheck != locLong.length)
                pieData += ",";
        }
        pieData += "], values:[";

        worldData += "], marker:{reversescale:true, size:[";
        commasCheck = 0;
        for(int q : quantities) {
            commasCheck++;

            // Count the total for the avg
            tot += q;
            // And store the max
            if(q > max) max = q;

            // In %
            worldData += (int) Math.ceil((float) q*max/(tot*2));
            // Append a comma if it's not the last element
            if(commasCheck != quantities.length)
                worldData += ",";
        }
        worldData += "], color:[";

        commasCheck = 0;
        for(int q : quantities) {
            commasCheck++;

            // Append the value in % to worldData (color)
            worldData += (int) Math.ceil((float) q*100/max);
            // and append the value in flat number
            pieData += String.valueOf(q);

            // Append a comma if it's not the last element
            if(commasCheck != quantities.length) {
                worldData += ",";
                pieData += ",";
            }
        }

        // End with default pieces of JS
        worldData += "], cmin:0, cmax:100, colorscale:'Greens', " +
                "colorbar:{title:'Peers Concentration',ticksuffix:'(% max)',showticksuffix:'last'}, " +
                "line:{color:'black'}}, name:'peers data'}];\n" +
                "var layout = {'geo':{'scope':'world', 'resolution':50}};\n" +
                "Plotly.newPlot('world',data,layout);";
        pieData += "],textinfo:\"percent\",textposition:\"inside\",automargin:true}]\n" +
                "var layout2={height:400,width:400,margin:{\"t\":0,\"b\":0,\"l\":0,\"r\":0}," +
                "showLegend:false}\nPlotly.newPlot('tester',data2,layout2)";

        // Start building the general stats innerHTML
        String statData = "document.getElementById(\"gen-stats-list\").innerHTML = \"<ul>";

        // Used simply as index for the int array
        commasCheck = 0;
        for(String s : stats) {
            // Creates an Unordered List of elements where the string is in bold
            statData += "<li><b>" + s + ":</b> " + statValue[commasCheck] + "</li>";
            commasCheck++;
        }
        statData += "</ul>\"";

        // Builds an array of indexes for the x axis
        String x = "x:[";
        for(int i=1; i<size; i++) {
            x += (float) i/2 + ",";
        }
        x += (float) size/2 + "],";

        // Used for the cartesian graph
        String cartesianGraph = "var newPeers={name:'New Peers'," + x + "y:[";

        // Concatenates the "new peers per hour"
        for(int i=0; i<size-1; i++)
            cartesianGraph += newPeersPerHour[i] + ",";
        cartesianGraph += newPeersPerHour[size-1] + "],mode:'lines+markers',type:'scatter'};\n";

        // Then concatenates the "total peers per hour"
        cartesianGraph += "var totPeers={name:'Tot Peers'," + x + "y:[";
        for(int i=0;i<size-1;i++)
            cartesianGraph += totPeersPerHour[i] + ",";
        cartesianGraph += totPeersPerHour[size-1] + "],mode:'lines+markers',type:'scatter'};\n";

        // Finally the "average"
        cartesianGraph += "var avgPeers={name:'Avg Peers'," + x + "y:[";
        int sum = 0;
        for(int i=1;i<size;i++) {
            sum += totPeersPerHour[i-1];
            cartesianGraph += sum / i + ",";
        }
        sum += totPeersPerHour[size-1];
        cartesianGraph += sum/size + "],mode:'lines',type:'scatter'};\n";

        // Sets up the remaining needed options
        cartesianGraph += "var layout3={xaxis:{title:{text:'Hours',font:{family:'Courier New,monospace'," +
                "size: 18,color: '#7f7f7f'}},},yaxis: {title:{text:'Number of Peers',font:{family: 'Courier New," +
                "monospace',size: 18,color: '#7f7f7f'}}}}\n";

        // Shows the Cartesian Graph
        cartesianGraph += "var graphData=[newPeers,totPeers,avgPeers];\nPlotly.newPlot('graph',graphData,layout3);";

        // Write the minified js file
        try {
            fw.write(worldData + "\n");
            fw.write(pieData + "\n");
            fw.write(statData + "\n");
            fw.write(cartesianGraph + "\n");
            fw.close();
        }
        catch(IOException e) { print("Error while writing into file: " + e.getMessage()); return; }

    }


    /**
     * Simple print to stdout if the boolean DEBUG in Configurations.java is True
     *
     * @param s the string to print
     */
    private static void print(String s) {
        if(Configurations.DEBUG)
            System.out.println(s);
    }
}
