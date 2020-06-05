pragma solidity 0.5.16;

import './PenaltyFunction.sol';

/**
 @notice This contract describes the status of a box of eggs. 
 It tracks a series of data sensed during its shipment of the box.
 The box has a state that can be modified by different callers.
 If the sensed data are bad, then a PenaltyFunction contracts computes a penalty value and it will be applied to the box.
 A reference to a PenaltyFunction contract is given as constructor argument. 
*/
contract BoxIncomplete {

    // Events
    event ready();
    event shipping();
    event received(uint amount); // The actual payed amount (expected - penalty)
    event refused(uint penalty); // The penalty that caused the rejection of the box

    // Box state
    enum State {READY, SHIPPING, RECEIVED, REFUSED}

    State public state;

    // Measurement samples    
    uint[] private samples_temperature;
    uint[] private samples_bump;

    // Penalty data
    uint public temperature_threshold;
    uint public bump_threshold;

    uint public producer_price = 50000000000000000; // 0.05 ether
    uint public transporter_price = 75000000000000000; // 0.075 ether
    uint public minimal_price = 20000000000000000; // 0.02 ether, minimal acceptable price for the receiver

    // Function computing the penalty
    PenaltyFunction public penalty_function;

    // Partners
    address public producer;
    address public transporter;
    address public receiver;

    modifier is_allowed(address expected) {
        require(msg.sender == expected, "Operation not allowed by caller");
        _;
    }

    /// @notice Constructor. Stores the addresses of the actors and the penalty function
    /// @param _transporter The address of the transporter
    /// @param _receiver The address of the final receiver
    /// @param _pf The address of the penalty function contract
    constructor (address _transporter, address _receiver, PenaltyFunction _pf) public {
        
        producer = msg.sender;
        transporter = _transporter;
        receiver = _receiver;

        state = State.READY;

        // Fahreneit unit of measure, to avoid small numbers on Celsius
        // https://eggsafety.org/faq/how-are-eggs-transported-safely-to-stores/
        temperature_threshold = 45;

        // Acceleration Suppose values multiplied by 1000, e.g. 5 m/s^2 = 5000
        bump_threshold = 5000;

        penalty_function = _pf;

        emit ready();
    }

    /// @notice Change the state from READY to SHIPPING. Callable by the transporter
    function ship() public is_allowed(transporter) payable {

        uint amount = msg.value;

        require(state == State.READY, "Error, invalid initial state");
        require(amount == producer_price, "Error, funds not match the expected amount");

        (bool success, ) = producer.call.value(amount)("");
        require(success == true, "Error while paying the producer");

        state = State.SHIPPING;
        emit shipping();
    }

    //// @notice Change the state from SHIPPING to ACCEPTED if the minimal price is not met; REFUSED otherwise. Callable by the receiver
    function complete() public is_allowed(receiver) payable {
		uint amount = msg.value;
		require(state == State.SHIPPING, "Error, invalid initial state");
		require(amount == transporter_price, "Error, funds not match the expected amount");
		
		uint penalty = penalty_function.compute_penalty(samples_temperature, samples_bump, temperature_threshold, bump_threshold);
		
		if((transporter_price < penalty) || (transporter_price - penalty) < minimal_price) {
			// The penalty overcomes the difference between initial and minimal price
			(bool success, ) = receiver.call.value(amount)("");
			require(success == true, "Error while refunding receiver");
			state = State.REFUSED;
			emit refused(penalty);
		}
		
		else {
			// Accept the box and pay the transporter
			uint to_pay = 0;
			to_pay = transporter_price - penalty;
			(bool success, ) = transporter.call.value(to_pay)("");
			require(success == true, "Error while paying transporter");
			(bool success2, ) = receiver.call.value(penalty)("");
			require(success2 == true, "Error while refunding penalties to the receiver");
			state = State.RECEIVED;
			emit received(to_pay);
		}
    }

    /// @notice Push sensed data samples to the contract. Only the transporter can push such data
    /// @param _temp An array of temperature data
    /// @param _bumps An array of bump data
    function push_data(uint[] memory _temp, uint[] memory _bumps) public is_allowed(transporter) {

        require(_temp.length == _bumps.length, "Input arrays should have same length");

        uint l = _temp.length;

        for (uint i=0; i<l; i++) {
            samples_temperature.push(_temp[i]);
            samples_bump.push(_bumps[i]);
        }
    }
}