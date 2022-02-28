/*
  In our case:
      -UNINITIALIZED = 0
      -PENDING = 1
      -STARTED = 2
      -ENDED = 3
      -CANCELLED = 4
  So for exmple if we write 'state == 0' we mean 'state == UNINITIALIZED'
  or 'state % 2 == 1' we mean 'state == PENDING || state == ENDED'.
*/


methods {
	getStartTimeById(uint256) returns(uint256) envfree
	getEndTimeById(uint256) returns(uint256) envfree
	getStateById(uint256) returns(uint8) envfree
	getNumOfParticipents(uint256) returns (uint256) envfree
	scheduleMeeting(uint256, uint256, uint256)

	getOrganizer(uint256) returns (address) envfree
	startMeeting(uint256)
	cancelMeeting(uint256)
	endMeeting(uint256)
	joinMeeting(uint256) envfree
}

definition meetingUninitialized(uint256 meetingId) returns bool = getStartTimeById(meetingId) == 0 && getEndTimeById(meetingId) == 0 && getStateById(meetingId) == 0 && getNumOfParticipents(meetingId) == 0 && getOrganizer(meetingId) == 0;
definition meetingPending(uint256 meetingId) returns bool = getStartTimeById(meetingId) != 0 && getStartTimeById(meetingId) < getEndTimeById(meetingId) && getStateById(meetingId) == 1 && getNumOfParticipents(meetingId) == 0 && getOrganizer(meetingId) != 0;
definition meetingStarted(uint256 meetingId, env e) returns bool = getStartTimeById(meetingId) <= e.block.timestamp && getEndTimeById(meetingId) > getStartTimeById(meetingId) && getOrganizer(meetingId) != 0 && getStateById(meetingId) == 2;
definition meetingEnded(uint256 meetingId, env e) returns bool = getStartTimeById(meetingId) < e.block.timestamp && getEndTimeById(meetingId) <= e.block.timestamp && getEndTimeById(meetingId) > getStartTimeById(meetingId) && getOrganizer(meetingId) != 0 && getStateById(meetingId) == 3;
definition meetingCanceled(uint256 meetingId) returns bool = getStartTimeById(meetingId) != 0 && getStartTimeById(meetingId) < getEndTimeById(meetingId) && getStateById(meetingId) == 4 && getNumOfParticipents(meetingId) == 0;


// Checks that a meeting can't be ended if it's not started or already not ended.
rule cannotEndIfNotStarted(method f, uint256 meetingId) {
  env e;
  calldataarg args;
  uint8 stateBefore = getStateById(meetingId);
  require stateBefore != 2 && stateBefore != 3;
  f(e,args);
  uint8 stateAfter = getStateById(meetingId);
  assert (stateAfter != 3, "Ended a meeting which was not started");
}

// Checks that a meeting can not be ended before end time.
rule cannotEndPrematurely(method f, uint256 meetingId) {
  env e;
  calldataarg args;
  uint8 stateBefore = getStateById(meetingId);
  uint256 endTime = getEndTimeById(meetingId);
  require stateBefore != 3;
  f(e,args);
  uint8 stateAfter = getStateById(meetingId);
  assert (stateAfter == 3 => endTime <= e.block.timestamp, "Ended a meeting before end time");
}

// Checks that a meeting can be cancelled by only organizer.
rule ownerCanCancel(method f, uint256 meetingId) {
  env e;
  calldataarg args;
  uint8 stateBefore = getStateById(meetingId);
  require stateBefore != 4;
  f(e,args);
  uint8 stateAfter = getStateById(meetingId);
  address organizer = getOrganizer(meetingId);
  assert (stateAfter == 4 => getOrganizer(meetingId) == e.msg.sender, "cancelled a meeting by someone other then organizer");
}

// Checks that state can not transition from PENDING to ENDED.
rule notPendingToEnded(method f, uint256 meetingId) {
  env e;
  calldataarg args;
  uint8 stateBefore = getStateById(meetingId);
  require stateBefore != 4;
  f(e,args);
  uint8 stateAfter = getStateById(meetingId);
  assert (stateBefore == 1 => stateAfter != 3, "state changed from Pending to Ended");
}
// Checks that state transition from PENDING to STARTED can only happen if
// startMeeting() was called, and start_time is in the past.
rule checkPendingToStarted(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);
  uint256 startTime = getStartTimeById(meetingId);
	f(e, args);
  uint8 stateAfter = getStateById(meetingId);
	
	assert ((stateBefore == 1 && stateAfter == 2) => (f.selector == startMeeting(uint256).selector) && startTime <= e.block.timestamp), "the status of the meeting changed from PENDING to STARTED through a function other then startMeeting() or STARTED before start time";
}