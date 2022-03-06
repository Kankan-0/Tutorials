
methods {
  getTotalFessEarnedPerShare() returns(uint256) envfree
  getUserBalance(address) returns (uint256) envfree
  assetsOf(address) returns (uint) envfree
}
rule totalFeesEarnedPerShareDoesnotDecrease(method f) {
    uint256 totalBefore = getTotalFessEarnedPerShare();

    env e;
    calldataarg arg;
    f(e, arg);

    uint256 totalAfter = getTotalFessEarnedPerShare();

    assert totalBefore <= totalAfter, "decreased unexpectedly";
}
rule totalFeesEarnedPerShareIncreases(method f) {
  
    uint256 totalBefore = getTotalFessEarnedPerShare();

    env e;
    calldataarg arg;
    f(e, arg);

    uint256 totalAfter = getTotalFessEarnedPerShare();

    assert totalBefore < totalAfter => f.selector == OwnerDoItsJobAndEarnsFeesToItsClients().selector, "chanegd by other functions";
}

rule depositDoesnotDecreaseAssets(address user) {
    env e;
    require e.msg.sender == user;
    uint assetsBefore = assetsOf(user);
    deposit(e);
    uint assetsAfter = assetsOf(user);
    assert assetsAfter >= assetsBefore, "deposit decreased assets";
}

rule withdrawDoesnotIncreaseAssets(address user) {
    env e;
    require e.msg.sender == user;
    uint assetsBefore = assetsOf(user);
    uint userBalance = getUserBalance(user);
    withdraw(e, userBalance);
    uint assetsAfter = assetsOf(user);
    assert assetsAfter <= assetsBefore, "withdraw increased assets";
}