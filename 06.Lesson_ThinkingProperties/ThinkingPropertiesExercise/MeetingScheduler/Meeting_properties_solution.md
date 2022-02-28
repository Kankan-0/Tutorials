

## States - 
 A meeting can be in any of these states : defUninitialized, defPending, defStarted, defEnded, defCancelled.
```ruby
- `defUninitialized` - (Uninitialized/Not created) is defined as `meetings[meetingId].status` as `UNINITIALIZED`.
- `defPending`       - is defined as `meetings[meetingId].status` is `PENDING`.
- `defStarted`       - is defined as `meetings[meetingId].status` is `STARTED`.
- `defEnded`         - is defined as `meetings[meetingId].status` is `ENDED`.
- `defCancelled`     - is defined as `meetings[meetingId].status` is `CANCELLED`.
```
1. `defUninitialized` => `getStartTimeById(id) == 0 && getEndTimeById(meetingId) == 0 && getStateById(meetingId) == 0 && getNumOfParticipents(meetingId) == 0 && getOrganizer(meetingId) == 0`. Initially all the fields has default value.

2. `defPending` => `getStartTimeById(meetingId) != 0 && getStartTimeById(meetingId) < getEndTimeById(meetingId) && getStateById(meetingId) == 1 && getNumOfParticipents(meetingId) == 0 && getOrganizer(meetingId) != 0`. Meeting should have valid start and end time.

3. `defStarted` => `getEndTimeById(meetingId) > getStartTimeById(meetingId) && getOrganizer(meetingId) != 0 && getStateById(meetingId) == 2` and `getStartTimeById(meetingId)` should be less than or equal to current timestamp. 

4. `defEnded` => `getEndTimeById(meetingId) > getStartTimeById(meetingId) && getOrganizer(meetingId) != 0 && getStateById(meetingId) == 3` and `getStartTimeById(meetingId)` should be less than or equal to current timestamp.

5. `defCancelled` => `getStartTimeById(meetingId) != 0 && getStartTimeById(meetingId) < getEndTimeById(meetingId) && getStateById(meetingId) == 4 && getNumOfParticipents(meetingId) == 0`. 


## State Transitions - 
6. A meeting can transition between the states in the following ways :

| From                       | To                         | Action                                                               |
|----------------------------|----------------------------|----------------------------------------------------------------------|
| defUninitialized           | defPending                 | By anyone, calling `scheduleMeeting` with valid inputs               |
| defPending                 | defStarted                 | By anyone, calling `startMeeting` provided start_time is in the past |
| defPending                 | defCancelled               | By organizer, calling `cancelMeeting`                                |
| defStarted                 | defEnded                   | By anyone, calling `endMeeting` provided end_time is in the past     |


## Variable Transitions -

7. Number of participants in a meeting should be in a non decreasing order.
8. Start_time should always be less than End_time for a meeting.

## High level properties -
9. If a meeting is not in `defStarted` state it can't be ended by anyone.
10. If a meeting start time has not arrived, it can't be started by anyone.
11. A meeting can only be cancelled by it's organizer, provided the current state is `defPending`.
12. If a meeting end time has not arrived, it can't be ended by anyone.
 
## Unit tests -
13. Start meeting chages the meeting state to started.
14. End meeting chages the meeting state to ended.
15. Cancel meeting chages the meeting state to cancelled.
16. Schedule meeting creates a new meeting.
17. Join meeting increases number of participants.


</br>

---
## Prioritizing
### High Priority:

- Property 1 to 5 are high priority as they should be correct otherwise the system will be in an invalid state.

- Property 6 is high priority because system should transition between states only when certain conditions are met.

- Property 8 is high priority otherwise a meeting can end up in an invalid state.

### Medium Priority:

- Properties 9 to 12 are medium priority as these are required for the system to behave correctly, but property 1-6 covers some part already.

### Low Priority:
- Property 7 is low priority since number of participants doesn't affect the behaviour of the system in a non-trivial way. 
- Properties 13 to 17 are low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They are fairly simple to check by other means, including by manual reviewing of the code.