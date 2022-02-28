
## States - (only one valid state at a time + in a valid state at any time)
 An auction can be in any of these states : Uninitialized(not created/closed), Created(bid not placed), Bid placed.


## State Transitions - state changes acc to correct order + under the right conditions
 An auction can transition between the states in the following ways :

| From                    | To                      | Action                                           |
|-------------------------|-------------------------|--------------------------------------------------|
| Uninitialized           | Created(bid not placed) | By owner, calling newAuction                     |
| Created(bid not placed) | Bid placed              | By anyone, with valid inputs                     |
| Bid placed              | Uninitialized           | By anyone, calling close when conditions are met |



## Variable Transitions -

* Auction prize should change in decreasing order.
* End_time should be fixed for an auction.
* Bid expiry can not be decreased.
* TotalSupply can not be decreased.
* TotalSupply should always be less than maxUint256 value.

## High level properties -
* Auction should be closable after 1 days from creation time if atleast a single bid was placed.
* After creation an auction can't be closed if no bids are placed.
* Can't create a duplicate auction when another with same id is in progress.
* TransferTo should keep the balances constant. 
  * SenderBefore + ReceiverBefore == SenderAfter + ReceiverAfter
* User can't decrease other's balance apart from their own.

 
## Unit tests -
* New bid should decrease the prize
* New bid should not decrease the bid expiry time.