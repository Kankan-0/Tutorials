

## States - 
 A meeting can be in any of these states : Active, OwnerDoesItsJob.
```ruby
- `Active` -  is defined as `owner != 0`.
- `OwnerDoesItsJob` - is defined as `totalFeesEarnedPerShare != 0`.
```
1. `Active` => `owner() != 0
2. `OwnerDoesItsJob` => `totalFeesEarnedPerShare() != 0

## State Transitions - 
3. The system can transition between the states in the following ways :

| From                       | To                         | Action                                                               |
|----------------------------|----------------------------|----------------------------------------------------------------------|
| Active                     | OwnerDoesItsJob            | By anyone, calling `OwnerDoItsJobAndEarnsFeesToItsClients`           |

## Variable Transitions -

4. totalFeesEarnedPerShare should be non decreasing.
5. feesCollectedPerShare for an account should be non decreasing.

## High level properties -
6. Owner can never be changed.
7. User can not withdraw more than the amount they have deposited.

## Unit tests -
8. OwnerDoItsJobAndEarnsFeesToItsClients should increase totalFeesEarnedPerShare.


</br>

---
## Prioritizing
### High Priority:

- Property 1 to 3 are high priority as they should be correct otherwise the system will be in an invalid state.

- Property 4-5,7 are high priority as they should be correct otherwise the system will not work as intended.

- Property 6 is high priority as changing an owner is not desirable.

### Low Priority:
- Property 7 is low priority since it is fairly simple to check by other means, including by manual reviewing of the code.