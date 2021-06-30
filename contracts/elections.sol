pragma solidity ^0.5.0;

contract Election {

    string public name;

    // Store Candidates
    // Fetch Candidate
    mapping ( uint => Candidate) public candidates;
    uint public candidateCount;

    // Store accounts that have voted
    mapping(address => bool) public voters;

    // Store candidate that have bee added
    mapping(address => bool) public added;

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
        address candidate;
    }

    event CandidateAdded (
        uint id,
        string name,
        uint voteCount,
        address candidate
    );

    event votedEvent (
        uint indexed _candidateId
    );

    constructor () public {
        name = "Election Protocol";
    }

    function addCandidate(string memory _name) public {
        require(bytes(_name).length>0);
        // each address can add only one candidate
        require(!added[msg.sender]);

        candidateCount++;
        added[msg.sender] = true;
        candidates[candidateCount] =  Candidate(candidateCount, _name, 0, msg.sender);
    
        emit CandidateAdded(candidateCount, _name, 0, msg.sender);
    }


    function vote(uint _candidateID) public {
        // record that voter has voted
        require(!voters[msg.sender]);
        require(_candidateID > 0 && _candidateID <= candidateCount);

        // record that voter has voted
        voters[msg.sender] = true;

        // update the voteCount
        candidates[_candidateID].voteCount++;

        emit votedEvent(_candidateID);

    }
    
}