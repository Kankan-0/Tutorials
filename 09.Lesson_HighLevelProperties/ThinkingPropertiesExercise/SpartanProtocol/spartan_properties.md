# Properties For Spartan

Variable transitions -> 
  1. Owner doesn't change.


High level -> 
  2. User LP token balance increases when add_liquidity is called.
  3. User LP token balance decreases when remove_liquidity is called.
  4. Swap should maintain the initial value of K

</br>

---

## Prioritizing

</br>
### High Priority:

- Properties 2-4 are high priority as failing any of them will indicate that system is not working as intended.

### Medium Priority:

- Properties 1 is low priority since it doesn't have a huge effect on the working of the system.