
# Properties For ERC20

Variable transitions -> 
  1. totalSupply increases only when mint is called.
  2. totalSupply decreases only when burn is called.
  3. mint should increase user balance.
  4. burn should decrease user balance.

High level -> 

  5. totalSupply should be greater than user balance for all users.
  6. totalSupply should be greater or equal to sum of all user balances.
  7. transfer should not change totalsupply.
      senderBefore + receiverBefore = senderAfter + receiverAfter
  8. transferFrom reduces allowance for the caller.

</br>

---

## Prioritizing

</br>
### High Priority:

- Properties 1-8 are high priority as failing any of them will indicate that system is not working as intended.
