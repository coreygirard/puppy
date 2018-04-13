# Full documentation


**Puppy**(*[delim]*)

Creates and returns a `Puppy` object.

- `delim` specifies the delimiter for parent/child topics. Must be a one-character string. If unspecified, `delim` defaults to `/`.

**Methods**

- `.Pub()`
- `.SubPush()`
- `.SubPull()`

- `.inject(topics, data)` is a testing/debugging method that injects the message `data` into the specified topic or list of topics
- `.verify()` is a *currently unimplemented* method that will return a list of any topics which lack publishers and/or subscribers. To be used for automated verification of architectures, and possibly throwing errors when trying to publish to a topic with no subscribers or receive from a topic with no publishers

---

Puppy.**Pub**(*topics*)

Creates and returns a `Publisher` object linked to the parent `Puppy` instance.

- `topics` is a string or list of strings, specifying which topics the `Publisher` should publish to.

**Methods**

- `.send()`

---

Puppy.**SubPush**(*topics,callback[,filter]*)

Creates and returns a `SubscriberPush` object linked to the parent `Puppy` instance.

- `topics` is a string or list of strings, specifying which topics the `SubscriberPush` should receive messages from.

- `callback` is the function called with each received message

- `filter` is a function to filter incoming messages:

  - returning `False` will prevent message delivery

  - an error during execution will prevent message delivery

  - any return value other than `False` (including *[falsey](https://stackoverflow.com/questions/39983695/what-is-truthy-and-falsy-in-python-how-is-it-different-from-true-and-false)* values) will allow message delivery

  - if unspecified, the default value is equivalent to `lambda x : True`

**Methods**

*none*

---

Puppy.**SubPull**(*topics[,filter]*)

Creates and returns a `SubscriberPull` object linked to the parent `Puppy` instance.

- `topics` behaves identically to the `topics` argument for **SubPush**

- `filter` behaves identically to the `filter` argument for **SubPush**

**Methods**

- `.recv()` returns the oldest unread message, or `None` if no unread messages exist
- `.recv_all()` returns a list of all unread messages, ordered from `[oldest, ... , newest]`, or `[]` if no unread messages exist
