from types import MethodType as _MethodType
from weakref import ref as _ref
from weakref import WeakMethod as _WeakMethod


__version__ = '0.3'


event_registry: dict = {}
_achivement_ids: list = []


def dispatch_event(name: str, *args) -> None:
    """Dispatch an event by name, with optional arguments.

    Any handlers set with the :py:func:`achievements.set_handler` function
    will recieve the event. If no handlers have been set, this
    function call will pass silently.

    :note:: If optional arguments are provided, but set handlers
            do not account for them, it will likely result in a
            TypeError or other undefined crash.
    """
    for func in event_registry.get(name, []):
        func()(*args)


def _make_callback(name: str):
    """Create an internal callback to remove dead handlers."""
    def callback(weak_method):
        event_registry[name].remove(weak_method)
        if not event_registry[name]:
            del event_registry[name]

    return callback


def set_handler(name: str, func) -> None:
    """Register a function to handle the named event type.

    After registering a function (or method), it will receive all
    events that are dispatched by the specified name.

    :note:: Only a weak reference is kept to the passed function,
    """
    if name not in event_registry:
        event_registry[name] = set()

    if isinstance(func, _MethodType):
        event_registry[name].add(_WeakMethod(func, _make_callback(name)))
    else:
        event_registry[name].add(_ref(func, _make_callback(name)))


def remove_handler(name: str, func) -> None:
    """Unregister a handler from receiving events of this name.

    If the passed function/method is not registered to
    receive the named event, or if the named event does
    not exist, this function call will pass silently.
    """
    if func not in event_registry.get(name, []):
        return

    event_registry[name].remove(func)
    if not event_registry[name]:
        del event_registry[name]


class Achievement:
    """Base Achievement class"""

    def __init__(self, uid: int, name: str, caption: str = "", maximum: int = 1):
        """Create a new Achievement object.

        At a minimum, Achievements must have a unique ID and name.
        You can optionally provide a sub caption (description).
        """
        assert uid not in _achivement_ids
        _achivement_ids.append(uid)

        self.id = uid
        self.name = name
        self.caption = caption

        self._maximum = maximum

        self._achieved = False
        self._value = 0

    @property
    def achieved(self):
        return self._achieved

    @property
    def maximum(self):
        return self._maximum

    @property
    def value(self):
        return self._value

    def increment(self, value):
        if self._achieved:
            return

        self._value = max(self._maximum, self._value + value)
        dispatch_event('on_change', self._value)

        if self._value == self._achieved:
            dispatch_event('on_achieved')

    def reset(self):
        self._achieved = False
        self._value = 0

    def set_achieved(self):
        if not self._achieved:
            dispatch_event('on_achieved')
        self._achieved = True

    def __del__(self):
        _achivement_ids.remove(self.id)
