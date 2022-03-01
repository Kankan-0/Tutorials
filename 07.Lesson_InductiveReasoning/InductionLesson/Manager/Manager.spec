methods {
	getCurrentManager(uint256 fundId) returns (address) envfree
	getPendingManager(uint256 fundId) returns (address) envfree
	isActiveManager(address a) returns (bool) envfree
}


// the rule fails to find bug2, but finds bug1
rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	// assume different IDs
	require fundId1 != fundId2;
	// assume different managers
	address manager1Before = getCurrentManager(fundId1);
	address manager2Before = getCurrentManager(fundId2);
	require manager1Before != manager2Before;
	
	// hint: add additional variables just to look at the current state
	bool active1Before = isActiveManager(manager1Before);			
	bool active2Before = isActiveManager(manager2Before);			
	
	require manager1Before != 0 => active1Before;
	require manager2Before != 0 => active2Before;

	env e;
	calldataarg args;
	f(e,args);
	
	address manager1After = getCurrentManager(fundId1);
	address manager2After = getCurrentManager(fundId2);
	
	bool active1After = isActiveManager(manager1After);			
	bool active2After = isActiveManager(manager2After);			
	
	// assert manager1After != 0 => active1After;
	// assert manager2After != 0 => active2After;
	// verify that the managers are still different 
	assert manager1After != manager2After, "managers not different";
}


// /* A version of uniqueManagerAsRule as an invariant */
// invariant uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2)
// 	fundId1 != fundId2 => getCurrentManager(fundId1) != getCurrentManager(fundId2) 
