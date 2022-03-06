# Properties For Spartan

Variable transitions -> 
  1. Owner doesn't change.
  2. K changes only by calling add_liquidity or remove_liquidity or init_pool.

High level -> 
  3. User LP token balance increases when add_liquidity is called.
  4. User LP token balance decreases when remove_liquidity is called.
  5. Swap should maintain the initial value of K
  
Unit tests ->
  6. Init_pool initializes owner balance with 100000

</br>

---

## Prioritizing

</br>
### High Priority:

- Properties 2-4 are high priority as failing any of them will indicate that system is not working as intended.

### Medium Priority:

- Property 1 is medium priority since it doesn't have a huge effect on the working of the system.

### Low Priority 
- Property 6 is low priority since it can be verified easily by other means also.