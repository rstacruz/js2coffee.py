/*
 * // Really bad snippet from jQuery...
event = typeof event === "object" ?
  // jQuery.Event object
  event[expando] ? event :
  // Object literal
  jQuery.extend( jQuery.Event(type), event ) :
  // Just the event type (string)
  jQuery.Event(type);
  */

// Simplified
e = a ? b ? c : d : e;

// Probably means..
//e = a ? (b ? c : d) : e;
