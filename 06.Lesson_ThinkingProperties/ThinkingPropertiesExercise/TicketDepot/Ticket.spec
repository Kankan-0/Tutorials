methods {
  getNumEvents() returns(uint16) envfree
  transactionFee() returns(uint64) envfree
  getTicketInfo() returns(uint256, uint64,address) envfree
}

definition availableForResell(uint16 eventId, uint16 ticketId) returns bool = getTicketDeadline(eventId, ticketId) != 0;
definition notAvailableForResell(uint16 eventId, uint16 ticketId) returns bool = getTicketDeadline(eventId, ticketId) == 0 && getTicketBuyer(eventId, ticketId) == 0 && getTicketPrice(eventId, ticketId) == 0;
definition ticketUnsold(uint16 eventId, uint16 ticketId) returns bool = getTicketOwner(eventId, ticketId) == 0;

function getTicketDeadline(eventId, ticketId) returns uint256{
  uint256 deadline; uint64 price; address buyer;
  deadline, price, buyer = getTicketInfo(eventId, ticketId);
  return deadline;
}
function getTicketBuyer(eventId, ticketId) returns address{
  uint256 deadline; uint64 price; address buyer;
  deadline, price, buyer = getTicketInfo(eventId, ticketId);
  return buyer;
}
function getTicketPrice(eventId, ticketId) returns uint64{
  uint256 deadline; uint64 price; address buyer;
  deadline, price, buyer = getTicketInfo(eventId, ticketId);
  return price;
}

// Checks that number of events can not decrease.
rule eventsNonDecreasing(method f) {
  env e;
  calldataarg args;
  uint16 numEventsBefore = getNumEvents();
  f(e, args);
  uint16 numEventsAfter = getNumEvents();

  assert (numEventsBefore <= numEventsAfter , "number of events decreased unexpectedly");
}

// Checks that transaction fee remains constant.
rule txFeeRemainsConstant(method f) {
  env e;
  calldataarg args;
  uint64 txFeeBefore = transactionFee();
  f(e, args);
  uint64 txFeeAfter = transactionFee();

  assert (txFeeBefore == txFeeAfter , "tx fee changed unexpectedly");
}

// Checks that buyNewTicket decreases available tickets.
rule ticketShouldDecreaseWithBuyNewTicket(method f, uint16 eventId) {
  env e;
  calldataarg args;
  uint16 availableTicketsBefore = getTicketsLeft(eventId);
  f(e, args);
  uint16 availableTicketsAfter = getTicketsLeft(eventId);

  assert (availableTicketsBefore > availableTicketsAfter => f.selector == buyNewTicket(uint16,address).selector , "available tickets should decrease");
}
// Checks that notAvailableForResell tickets are now availableForResell only if offerTicket is called.
rule ticketResellStateChange1(method f, uint16 eventId, uint16 ticketId) {
  env e;
  calldataarg args;
  require notAvailableForResell(eventId, ticketId);
  f(e, args);

  assert (availableForResell(eventId, ticketId) => f.selector == offerTicket(uint16, uint16, uint64, address, uint16).selector, "ticket available for resell through some other functions");
}
// Checks that availableForResell tickets are now notAvailableForResell only if buyOfferedTicket is called.
rule ticketResellStateChange2(method f, uint16 eventId) {
  env e;
  calldataarg args;
  require availableForResell(eventId, ticketId);
  f(e, args);

  assert (notAvailableForResell(eventId, ticketId) => f.selector == buyOfferedTicket(uint16, uint16, address).selector, "ticket not available for resell through some other functions");
}
// Checks that unsold tickets are now notAvailableForResell only if buyNewTicket is called.
rule ticketStateChange3(method f, uint16 eventId) {
  env e;
  calldataarg args;
  require ticketUnsold(eventId, ticketId);
  f(e, args);

  assert (notAvailableForResell(eventId, ticketId) => f.selector == buyNewTicket(uint16, address).selector, "ticket unsold to not available for resell through some other functions");
}