
methods {
	ballAt() returns uint256 envfree
	pass() envfree
}


invariant neverReachPlayer4() 
	ballAt() != 4 && ballAt() != 3

rule ballNotIn4(method f) {
	env e;
	calldataarg args;
	uint256 ballAtBefore = ballAt();
	require ballAtBefore != 3 && ballAtBefore != 4;
	f(e,args);
	uint256 ballAtAfter = ballAt();
	assert ballAtAfter != 4;
}