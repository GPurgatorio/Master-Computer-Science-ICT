pragma solidity 0.5.16;

/// @notice A contract interface to compute the penalty given a set of sensed data
contract PenaltyFunction {

    // Penalties, in Ether, for each un-satisfied condition 
    uint public temperature_penalty = 5000000000000000; // 0.005 ether
    uint public bump_penalty = 2000000000000000; // 0.002 ether

    /// @notice Function signature to compute the penalty given a set of sensed data
    /// @param _temperature The array of temperature data
    /// @param _bump The array of bumps data
    /// @param temperature_threshold The threshold value to penalize a temperature data 
    /// @param bump_threshold The threshold value to penalize a bump data 
    function compute_penalty(uint[] calldata _temperature,
                            uint[] calldata _bump,
                            uint temperature_threshold,
                            uint bump_threshold) external view returns(uint);
}


/// @notice This penalty contract computes the penalty by multiplying the penalty of a data with its occurence and summing them up
contract SimplePenalty is PenaltyFunction {

    function compute_penalty(uint[] calldata _temperature,
                            uint[] calldata _bump,
                            uint temperature_threshold,
                            uint bump_threshold) external view  returns(uint) {

        uint l = _temperature.length;
        uint tmp_penalty_count = 0;
        uint bmp_penalty_count = 0;

        for(uint i=0; i<l; i++) {

            if(_temperature[i] > temperature_threshold)
                tmp_penalty_count++;

            if(_bump[i] > bump_threshold)
                bmp_penalty_count++;                
        }

        uint penalty = bmp_penalty_count*bump_penalty + tmp_penalty_count*temperature_penalty;
        
        return penalty;
    }
}


/// @notice This penalty contract computes the penalty by assigning higher weight to values overcoming the threshold with higher index. The first occurrence does not increase the penalty
contract IncreasingPenalty is PenaltyFunction {
    
    function compute_penalty(uint[] calldata _temperature,
                            uint[] calldata _bump,
                            uint temperature_threshold,
                            uint bump_threshold) external view returns(uint) {
    
        uint l = _temperature.length;
        uint tmp_penalty = 0;
        uint bmp_penalty = 0;
        uint tmp_penalty_count = 0;
        uint bmp_penalty_count = 0;

        for(uint i=0; i<l; i++) {

            if(_temperature[i] > temperature_threshold) {

                tmp_penalty += tmp_penalty_count*temperature_penalty;
                tmp_penalty_count++;
            }

            if(_bump[i] > bump_threshold) {

                bmp_penalty += bmp_penalty_count*bump_penalty;
                bmp_penalty_count++;                
            }
        }

        return tmp_penalty + bmp_penalty;        
    }
}