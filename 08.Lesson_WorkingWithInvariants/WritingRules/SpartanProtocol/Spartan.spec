methods {
    balanceOf(address) returns (uint256) envfree
    totalSupply() returns (uint256) envfree
    getOwnerBalance() returns (uint256) envfree
    add_liquidity() returns (uint256)
    remove_liquidity()
    getKValue() envfree

}

// invariant totalFunds_GE_single_user_balance()
//     forall address user. totalSupply() >= balanceOf(user)

rule addLiquidityIncreaseLPToken( method f, address user) {
    env e;
    require e.msg.sender == user;
    uint256 balanceBefore = balanceOf(user);
    uint256 units = add_liquidity(e);
    uint256 balanceAfter = balanceOf(user);

    assert balanceBefore + units == balanceAfter, "addLiquidity didn't increase lp token balance";
}

rule removeLiquidityIncreaseLPToken( method f, address user) {
    env e;
    require e.msg.sender == user;
    uint256 balanceBefore = balanceOf(user);
    uint256 units;
    remove_liquidity(e, units);
    uint256 balanceAfter = balanceOf(user);

    assert balanceBefore - units == balanceAfter, "removeLiquidity didn't decrease lp token balance";
}

rule KdoesnotChange(method f) {
    env e;
    calldataarg args;

    uint256 kValueBefore = getKValue();
    swap(e, args);
    uint256 kValueAfter = getKValue();

    assert kValueBefore == kValueAfter, "K changed after swapping";
}