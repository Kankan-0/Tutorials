methods {
    totalSupply() returns (uint256) envfree
      
    balanceOf(address) returns(uint256) envfree
    allowance(address, address) returns(uint256) envfree
    transfer(address, uint256) returns (bool)
    transferFrom(address, address, uint256) returns (bool)
    increaseAllowance(address, uint256) returns (bool)

    approve(address, uint256) returns (bool)
    decreaseAllowance(address, uint256) returns(bool)
}

invariant totalFunds_GE_single_user_funds()
  forall address user. totalSupply() >= balanceOf(user)

  // Checks that increaseAllowance() increases allowance of spender
rule increaseAllowanceIncreases() {
	env e;
  address spender; uint256 amount;
	uint256 allowanceBefore = allowance(e.msg.sender, spender);
	increaseAllowance(e, spender, amount);
	uint256 allowanceAfter = allowance(e.msg.sender, spender);

	assert (amount > 0 => (allowanceAfter > allowanceBefore)) && (amount == 0 => (allowanceAfter == allowanceBefore)), "allowance did not increase";
}

  // Checks that decreaseAllowance() decreases allowance of spender
rule decreaseAllowanceDecreases() {
	env e;
  address spender; uint256 amount;
	uint256 allowanceBefore = allowance(e.msg.sender, spender);
	decreaseAllowance(e, spender, amount);
	uint256 allowanceAfter = allowance(e.msg.sender, spender);

	assert (amount > 0 => (allowanceAfter < allowanceBefore)) && (amount == 0 => (allowanceAfter == allowanceBefore)), "allowance did not decrease";
}

// Checks that the sum of sender and recipient accounts remains the same after transfer(), i.e. assets doesn't disappear nor created out of thin air
rule integrityOfTransfer(address recipient, uint256 amount) {
	env e;
	uint256 balanceSenderBefore = balanceOf(e.msg.sender);
	uint256 balanceRecipientBefore = balanceOf(recipient);
	transfer(e, recipient, amount);

	assert balanceRecipientBefore + balanceSenderBefore == balanceOf(e.msg.sender) + balanceOf(recipient), "the total funds before and after a transfer should remain the constant";
}

// Checks that transferFrom reduces allowance.
rule integrityOfTransferFrom(address recipient, address sender, uint256 amount) {
	env e;
  uint256 allowanceBefore = allowance(sender, e.msg.sender);
	// uint256 balanceSenderBefore = balanceOf(e.msg.sender);
	// uint256 balanceRecipientBefore = balanceOf(recipient);
  require allowanceBefore >= amount;
	transferFrom(e, sender, recipient, amount);
  uint256 allowanceAfter = allowance(sender, e.msg.sender);
  assert (amount > 0 => (allowanceAfter < allowanceBefore)) && (amount == 0 => (allowanceAfter == allowanceBefore)), "allowance did not decrease after transferFrom";
}