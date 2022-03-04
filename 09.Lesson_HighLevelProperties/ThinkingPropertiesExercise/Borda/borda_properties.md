# Properties For Borda

1. Valid states -> 
  Unregistered :-> both getFullVoterDetails and getFullContenderDetails  returns all 0
  Registered :-> either getFullVoterDetails or getFullContenderDetails  returns non 0. The registered flag is set to true. 
  Voted :-> hasVoted returns true
  Blacklisted :-> black_listed flag is set to true

2. state transition -> 
  Unregistered -> Registered (register voter/register contender called)
  Registered -> Voted (vote called)
  Voted -> Blacklisted (calling vote more than two times)

Variable transitions -> 
 3. Contender points should not decrease.Increases if vote is called with one of the address as contender.
 4. Vote attempts should not decrease.

High level -> 
  5. Can not unregister; once a user registers, register flag should never be false.
  6. Once a user gets blacklisted, can not get out of blacklist.
  7. Blacklisted user can not vote.
  8. User points should increase properly. 
      If an address is the first argument to the vote function, points increases by 3.
      If an address is the second argument to the vote function, points increases by 2.
      If an address is the third argument to the vote function, points increases by 1.
  9. User can not vote more than once.

Unit tests ->
  10. Register voter should update the register flag for the voter to true if it was false before.
  11. Register contender should update the register flag for the contender to true if it was false before.

</br>

---

## Prioritizing

</br>
### High Priority:

- Properties 1-9 are high priority as failing any of them will indicate that system is not working as intended.

### Low Priority:

- Properties 10 & 11 are low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They fairly simple to check by other means, including by manual reviewing of the code.