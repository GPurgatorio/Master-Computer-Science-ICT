/*
 * Copyright 2010 Aalto University, ComNet
 * Released under GPLv3. See LICENSE.txt for details.
 */
package core;

import input.EventQueue;
import input.ExternalEvent;
import input.ScheduledUpdatesQueue;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

/**
 * World contains all the nodes and is responsible for updating their
 * location and connections.
 */
public class World {
	/** name space of optimization settings ({@value})*/
	public static final String OPTIMIZATION_SETTINGS_NS = "Optimization";

	/**
	 * Should the order of node updates be different (random) within every
	 * update step -setting id ({@value}). Boolean (true/false) variable.
	 * Default is @link {@link #DEF_RANDOMIZE_UPDATES}.
	 */
	public static final String RANDOMIZE_UPDATES_S = "randomizeUpdateOrder";
	/** should the update order of nodes be randomized -setting's default value
	 * ({@value}) */
	public static final boolean DEF_RANDOMIZE_UPDATES = true;

	
	/**
	 * Real-time simulation enabled -setting id ({@value}). 
	 * If set to true and simulation time moves faster than real time,
	 * the simulation will pause after each update round to wait until real
	 * time catches up. Default = false.
	 */
	public static final String REALTIME_SIM_S = "realtime";
	/** should the update order of nodes be randomized -setting's default value
	 * ({@value}) */
	
	/**
	 * Should the connectivity simulation be stopped after one round
	 * -setting id ({@value}). Boolean (true/false) variable. Default = false.
	 */
	public static final String SIMULATE_CON_ONCE_S = "simulateConnectionsOnce";

	private int sizeX;
	private int sizeY;
	private List<EventQueue> eventQueues;
	private double updateInterval;
	private SimClock simClock;
	private double nextQueueEventTime;
	private EventQueue nextEventQueue;
	/** list of nodes; nodes are indexed by their network address */
	private List<DTNHost> hosts;
	private boolean simulateConnections;
	/** nodes in the order they should be updated (if the order should be
	 * randomized; null value means that the order should not be randomized) */
	private ArrayList<DTNHost> updateOrder;
	/** is cancellation of simulation requested from UI */
	private boolean isCancelled;
	private List<UpdateListener> updateListeners;
	/** Queue of scheduled update requests */
	private ScheduledUpdatesQueue scheduledUpdates;
	private boolean simulateConOnce;
	
	private boolean realtimeSimulation;
	private long simStartRealtime;

	private double patchProb;
	private double installCheck;
	private double statCheck;
	// Used because The ONE calls updateHosts() many times and would cause too many patches
	public int bugTime;

	private File out;

	/**
	 * Constructor.
	 */
	public World(List<DTNHost> hosts, int sizeX, int sizeY,
			double updateInterval, List<UpdateListener> updateListeners,
			boolean simulateConnections, List<EventQueue> eventQueues) {
		this.hosts = hosts;
		this.sizeX = sizeX;
		this.sizeY = sizeY;
		this.updateInterval = updateInterval;
		this.updateListeners = updateListeners;
		this.simulateConnections = simulateConnections;
		this.eventQueues = eventQueues;

		this.simClock = SimClock.getInstance();
		this.scheduledUpdates = new ScheduledUpdatesQueue();
		this.isCancelled = false;

		this.simStartRealtime = -1;

		this.bugTime = 0;
		
		setNextEventQueue();
		initSettings();
	}

	/**
	 * Initializes settings fields that can be configured using Settings class
	 */
	private void initSettings() {
		Settings s = new Settings(OPTIMIZATION_SETTINGS_NS);
		boolean randomizeUpdates = s.getBoolean(RANDOMIZE_UPDATES_S, 
				DEF_RANDOMIZE_UPDATES);

		this.simulateConOnce = s.getBoolean(SIMULATE_CON_ONCE_S, false);
		
		this.realtimeSimulation = s.getBoolean(REALTIME_SIM_S ,false);

		if(randomizeUpdates) {
			// creates the update order array that can be shuffled
			this.updateOrder = new ArrayList<DTNHost>(this.hosts);
		}
		else { // null pointer means "don't randomize"
			this.updateOrder = null;
		}

		s = new Settings("PandemicFlu");

		patchProb = s.getDouble("patchProbability");
		if(patchProb < 0 || patchProb > 1) {
			System.err.println("Error in config: PatchProb isn't a valid value [0,1] -> " + patchProb);
			System.exit(-1);
		}

		installCheck = s.getInt("installCheck");
		statCheck = s.getInt("statCheck");
		if(installCheck < 0 || statCheck < 0) {
			System.err.println("Error in config: installCheck or statCheck have negative values");
			System.exit(-1);
		}

		File dir = new File("reports/");
		dir.mkdir();

		out = new File("reports/" + s.valueFillString(new Settings().getSetting(SimScenario.SCENARIO_NS +
				"." +	SimScenario.NAME_S)) + "_PandemicFluStats.txt");
	}

	/**
	 * Moves hosts in the world for the time given time initialize host
	 * positions properly. SimClock must be set to <CODE>-time</CODE> before
	 * calling this method.
	 * @param time The total time (seconds) to move
	 */
	public void warmupMovementModel(double time) {
		if (time <= 0) {
			return;
		}

		while(SimClock.getTime() < -updateInterval) {
			moveHosts(updateInterval);
			simClock.advance(updateInterval);
		}

		double finalStep = -SimClock.getTime();

		moveHosts(finalStep);
		simClock.setTime(0);
	}

	/**
	 * Goes through all event Queues and sets the
	 * event queue that has the next event.
	 */
	public void setNextEventQueue() {
		EventQueue nextQueue = scheduledUpdates;
		double earliest = nextQueue.nextEventsTime();

		/* find the queue that has the next event */
		for (EventQueue eq : eventQueues) {
			if (eq.nextEventsTime() < earliest){
				nextQueue = eq;
				earliest = eq.nextEventsTime();
			}
		}

		this.nextEventQueue = nextQueue;
		this.nextQueueEventTime = earliest;
	}

	/**
	 * Update (move, connect, disconnect etc.) all hosts in the world.
	 * Runs all external events that are due between the time when
	 * this method is called and after one update interval.
	 */
	public void update () {
		double runUntil = SimClock.getTime() + this.updateInterval;
		
		if (realtimeSimulation) {
			if (this.simStartRealtime < 0) {
				/* first update round */
				this.simStartRealtime = System.currentTimeMillis();
			}

			long sleepTime = (long) (SimClock.getTime() * 1000 
					- (System.currentTimeMillis() - this.simStartRealtime));
			if (sleepTime > 0) {
				try {
					Thread.sleep(sleepTime);
				} catch (InterruptedException e) {
					throw new SimError("Sleep interrupted:" + e);
				}
			}
		}
		
		setNextEventQueue();

		/* process all events that are due until next interval update */
		while (this.nextQueueEventTime <= runUntil) {
			simClock.setTime(this.nextQueueEventTime);
			ExternalEvent ee = this.nextEventQueue.nextEvent();
			ee.processEvent(this);
			updateHosts(); // update all hosts after every event
			setNextEventQueue();
		}

		moveHosts(this.updateInterval);
		simClock.setTime(runUntil);

		updateHosts();

		/* inform all update listeners */
		for (UpdateListener ul : this.updateListeners) {
			ul.updated(this.hosts);
		}

		pandemicFluChecks();
	}

	/**
	 * Updates all hosts (calls update for every one of them). If update
	 * order randomizing is on (updateOrder array is defined), the calls
	 * are made in random order.
	 */
	private void updateHosts() {
		if (this.updateOrder == null) { // randomizing is off
			for (int i=0, n = hosts.size();i < n; i++) {
				if (this.isCancelled) {
					break;
				}
				hosts.get(i).update(simulateConnections);
			}
		}
		else { // update order randomizing is on
			assert this.updateOrder.size() == this.hosts.size() :
				"Nrof hosts has changed unexpectedly";
			Random rng = new Random(SimClock.getIntTime());
			Collections.shuffle(this.updateOrder, rng);

			for (int i=0, n = hosts.size();i < n; i++) {
				if (this.isCancelled) {
					break;
				}

				this.updateOrder.get(i).update(simulateConnections);
			}
		}

		if (simulateConOnce && simulateConnections) {
			simulateConnections = false;
		}
	}

	/**
	 * Moves all hosts in the world for a given amount of time
	 * @param timeIncrement The time how long all nodes should move
	 */
	private void moveHosts(double timeIncrement) {
		for (int i=0,n = hosts.size(); i<n; i++) {
			DTNHost host = hosts.get(i);
			host.move(timeIncrement);
		}
	}

	/**
	 * Asynchronously cancels the currently running simulation
	 */
	public void cancelSim() {
		this.isCancelled = true;
	}

	/**
	 * Returns the hosts in a list
	 * @return the hosts in a list
	 */
	public List<DTNHost> getHosts() {
		return this.hosts;
	}

	/**
	 * Returns the x-size (width) of the world
	 * @return the x-size (width) of the world
	 */
	public int getSizeX() {
		return this.sizeX;
	}

	/**
	 * Returns the y-size (height) of the world
	 * @return the y-size (height) of the world
	 */
	public int getSizeY() {
		return this.sizeY;
	}

	/**
	 * Returns a node from the world by its address
	 * @param address The address of the node
	 * @return The requested node or null if it wasn't found
	 */
	public DTNHost getNodeByAddress(int address) {
		if (address < 0 || address >= hosts.size()) {
			throw new SimError("No host for address " + address + ". Address " +
					"range of 0-" + (hosts.size()-1) + " is valid");
		}

		DTNHost node = this.hosts.get(address);
		assert node.getAddress() == address : "Node indexing failed. " +
			"Node " + node + " in index " + address;

		return node;
	}

	/**
	 * Schedules an update request to all nodes to happen at the specified
	 * simulation time.
	 * @param simTime The time of the update
	 */
	public void scheduleUpdate(double simTime) {
		scheduledUpdates.addUpdate(simTime);
	}

	public void pandemicFluChecks() {

		// The ONE simulator calls update() MANY times for no reasons in the same moment
		if(SimClock.getIntTime() == bugTime)
			return;

		bugTime = SimClock.getIntTime();

		// Checks if it's the time to try to patch the devices
		boolean check = false;
		if(SimClock.getIntTime() % installCheck == 0)
			check = true;

		// It's time to try to patch hosts
		if(check) {
			for (int i = 0, n = hosts.size(); i < n; i++)
				hosts.get(i).patchInfection(patchProb);
		}

		// Checks if it's time to print stats
		if(SimClock.getIntTime() % statCheck == 1)
			printStats();
	}

	private void printStats() {
		try {
			FileWriter fw = new FileWriter(out, true);

			int susceptible = 0, infected = 0, recovered = 0;
			for(DTNHost h : hosts) {
				if(h.isPatched())
					recovered++;
				else if(h.isInfectious())
					infected++;
				else
					susceptible++;
			}
			String SIR = SimClock.getIntTime() + " -> susceptible:" + susceptible +
					" infected:" + infected + " recovered:" + recovered + '\n';
			fw.write(SIR);
			fw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
