methods {
		getTokenAtIndex(uint256 index) returns (address) envfree
		getIdOfToken(address token) returns (uint256) envfree
    getReserveCount() returns (uint256) envfree
    addReserve(address, address, address, uint256) envfree 
    removeReserve(address) envfree
}


// invariant listCorrelated(uint256 index) 
//   getTokenAtIndex(index) != 0 => getIdOfToken(getTokenAtIndex(index)) == index

// invariant listCorrelated2(uint256 index, address _token)
//   (index != 0 && _token != 0 => getIdOfToken(_token) == index <=> getTokenAtIndex(index) == _token) 
//     && (index == 0 => getTokenAtIndex(index) == _token => getIdOfToken(_token) == index )
//   }

rule ReserveCountChangesByOne(method f) {
	env e;
	calldataarg args;
	uint256 reserveCountBefore = getReserveCount();
	f(e, args);
	uint256 reserveCountAfter = getReserveCount();
	assert (reserveCountAfter == reserveCountBefore + 1 || reserveCountAfter == reserveCountBefore - 1) => (f.selector == addReserve(address, address, address, uint256).selector || f.selector == removeReserve(address).selector);
}

rule independencyOfTokens(address token1, address token2, address stableToken, address varToken, uint256 fee) {
	env e;
	require token1 != token2;
	uint256 tokenId1Before = getIdOfToken(token1);
  removeReserve(token2);
  uint256 tokenId1After = getIdOfToken(token1);
  assert tokenId1Before == tokenId1After, "id changed for other tokens after removeReserve";
}

rule noTokenSavedAtReserveCountOrFurther(method f, uint256 i, address token, address stableToken, address varToken, uint256 fee) {
	env e;
	calldataarg args;
	uint256 i1;
	// uint256 i2;
	require i1 >= getReserveCount() => getTokenAtIndex(i1) == 0;
	require f.selector != removeReserve(address).selector;
	f(e,args);
	assert i1 >= getReserveCount() => getTokenAtIndex(i1) == 0;
}