methods {
    getFullVoterDetails(address) returns(uint8, bool, bool, uint256, bool) envfree
    getPointsOfContender(address) returns(uint256) envfree
    getFullContenderDetails(address) returns(uint8, bool, uint256) envfree 
    registerVoter(uint8) returns (bool)

    hasVoted(address) returns (bool) envfree
    getWinner() returns (address, uint256) envfree
    registerContender(uint8) returns (bool)
    vote(address, address, address) returns(bool)
}

function getVoterAge(address voter) returns uint8 {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return age;
}
function getVoterVoteAttempts(address voter) returns uint256 {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return vote_attempts;
}

function getVoterRegistrationStatus(address voter) returns bool {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voterReg;
}
function getContenderRegistrationStatus(address contender) returns bool {
    uint8 age; bool contenderReg; uint256 points;
    age, contenderReg, points = getFullContenderDetails(contender);
    return contenderReg;
}

function getVoterVoteBlocked(address voter) returns bool {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return blocked;
}

function getVoterVoted(address voter) returns bool {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voted;
}

rule unregisteredToRegister (method f, address user) {
  env e; calldataarg args;
  bool voterRegBefore = getVoterRegistrationStatus(user);
  bool contenderRegBefore = getContenderRegistrationStatus(user);
  
  require !(voterRegBefore || contenderRegBefore);
  f(e, args);

  bool voterRegAfter = getVoterRegistrationStatus(user);
  bool contenderRegAfter = getContenderRegistrationStatus(user);

  assert (voterRegAfter || contenderRegAfter) => (
    !(voterRegBefore || contenderRegBefore) && (f.selector == registerVoter(uint8).selector || 
    f.selector ==  registerContender(uint8).selector)
  );  
}

rule pointsNonDecreasing(method f, address contender){
    env e; calldataarg args;
    uint8 age; bool registeredBefore; uint256 pointsBefore;
    age, registeredBefore, pointsBefore = getFullContenderDetails(contender);
    require pointsBefore > 0 => registeredBefore; 
    f(e,args);
    bool registeredAfter; uint256 pointsAfter;
    age, registeredAfter, pointsAfter = getFullContenderDetails(contender);

    assert (pointsAfter >= pointsBefore,"Points decreased for a contender");
}
rule voteAttemptsNonDecreasing(method f, address voter){
    env e; calldataarg args;
    bool registeredBefore = getVoterRegistrationStatus(voter);
    uint256 attemptsBefore = getVoterVoteAttempts(voter);
    require attemptsBefore >= 0 => registeredBefore; 
    f(e,args);
    bool registeredAfter; uint256 pointsAfter;
    uint256 attemptsAfter = getVoterVoteAttempts(voter);
    assert (attemptsAfter >= attemptsBefore, "Vote_attempts decreased");
}
rule votedToBlacklisted(method f, address voter) {
    env e; calldataarg args;
    bool blocked_before = getVoterVoteBlocked(voter);
    bool register_before = getVoterRegistrationStatus(voter);
    bool voted_before = getVoterVoted(voter);
    
    uint256 vote_attempts_before = getVoterVoteAttempts(voter);
    require !blocked_before && vote_attempts_before < 3;
    
    f(e,args);

    bool blocked_after = getVoterVoteBlocked(voter);
    uint256 vote_attempts_after = getVoterVoteAttempts(voter);
    assert (blocked_after => vote_attempts_after >= 3, "vote_attempt didn't increase");

}
rule blackListToWhiteList(method f, address voter){
    env e; calldataarg args;
    bool blocked_before = getVoterVoteBlocked(voter);
    bool register_before = getVoterRegistrationStatus(voter);
    require blocked_before => register_before;
    f(e, args);
    bool blocked_after = getVoterVoteBlocked(voter);
    
    assert blocked_before => blocked_after, "can't get out of the blackList";
}