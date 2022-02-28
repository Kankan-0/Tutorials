## States - 
 An event can be either in `defNotCreated` or in `defCreated` state.
 A Ticket for an event can be either in `defUnsold` or in `defAvailableForResell` or in `defNotAvailableForResell` state.

```
1. `defNotCreated` => `eventsMap[eventID].owner == 0 && eventsMap[eventID].ticketPrice == 0 && eventsMap[eventID].ticketsRemaining == 0` and `eventsMap[eventID].attendees[attendeeId] == 0` for all attendees. Initially all the fields has default value.

2. `defCreated` => `eventsMap[eventID].owner != 0`. Event will have a valid owner.

3. `defAvailableForResell` => `offerings[offerId].deadline != 0`. Deadline should be non zero if a ticket is available for resell.; 

4. `defNotAvailableForResell` => `offerings[offerId].deadline == 0 && offerings[offerId].price == 0 && offerings[offerId].buyer == 0`. All the fields should have default values if a ticket is not available for resell.;

5. `defUnsold` => `eventsMap[_eventID].attendees[ticketID] == 0` ticketID for _eventID is unsold.;

## State Transitions - 
6. Following state transitions are possible :

| From                       | To                         | Action                                                 |
|----------------------------|----------------------------|--------------------------------------------------------|
| defNotCreated              | defCreated                 | By anyone, calling `createEvent` with valid inputs     |
| defUnsold                  | defNotAvailableForResell   | By anyone, calling `buyNewTicket` with valid inputs    |
| defNotAvailableForResell   | defAvailableForResell      | By anyone, calling `offerTicket`   with valid inputs   |
| defAvailableForResell      | defNotAvailableForResell   | By anyone, calling `buyOfferedTicket` with valid inputs|


## Variable Transitions -

7. Number of events should be non decreasing.
8. transactionFee can not be changed.
9. Number of available tickets for an event can't increase.

## High level properties -
10. Buying new ticket should decrease number of available tickets.
11. Balance of contract owner should not decrease.
12. Balance of event owner should not decrease.
13. Creating new events increases the number of events.
14. A ticket should have only one buyer.
15. Resell ticket can only be bought before deadline passes. 
 
## Unit tests -


</br>

---
## Prioritizing
### High Priority:

- Property 1 to 5 are high priority as they should be correct otherwise the system will be in an invalid state.

- Property 6 is high priority because system should transition between states only when certain conditions are met.

- Property 7 is high priority otherwise event collision can happen and information about certain events will be overwritten.

- Property 11-12 is high priority otherwise no one will run a depot or organize an event.

- Property 14 is high priority otherwise multiple people can use the same ticket which is not intended.




### Medium Priority:

- Property 8 is medium priority as changing tx fee will result in a loss for the depot owner.

- Property 9-10 is medium priority as miscalculation here will not be devastating, but the system might not behave as intended.

### Low Priority:
- Properties 13, 15 are low priority since they are fairly simple to check by other means, including by manual reviewing of the code.