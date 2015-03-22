toolshed
========

About
-----
``toolshed`` is an extension to the pretty awesome `toolz`_ library.

toolz brings to the table support for stream and dictionary processing and 
function manipulation inspired by Clojure and other functional languages.

While toolz aims to be a small, curated library of broadly usable functions, 
sometimes the same functions end up being defined in many projects. Either
they're simple tools that simply look better with a name or more specific ones
that are less composable but nonetheless helpful.

Time and time again, you're utilities module fills up with these same overly 
simple and highly composed pieces. You've accumulated a toolshed.

``toolz`` itself has a bit of a shed from recipes, tips and tricks and sample
functions in the documentation, but many of these are don't have written tests.
Toolshed wants to gather these and your shed under one roof where we can all
be good neighbors and borrow what pieces we need.

Structure and Heritage
----------------------
Similar to toolz, toolshed is broken into several components:

* iters: For iterators
* dicts: For dict and dict-like mappings
* funcs: For higher order functions

New components may be added in the future based on proposals, demand and 
feedback; however, in an effort to maintain the namespace, new components will
go through a provisional period in the sandbox before being promoted to the
library proper.

Dependencies
------------
Toolshed aims to be dependent solely on toolz and the standard library. Part of
compatibility with toolz is supporting Python 2.6, 2.7, 3.2, 3.3 and 3.4, as
well as pypi and pypi 3.

Contributiions Welcome
----------------------
Just like ``toolz``, ``toolshed`` welcomes utilities that come from functional
and list processing heritages.

While this library aims to be broader than toolz, we would prefer to not amass
a collection of forgotten tools. An ideal contribution is something different
from utilities here and in ``toolz`` and is outside that sweet spot toolz hits
(that just right amount of composition).

Visiting both our issues page to see what's being proposed here
and `toolz's issue page <https://github.com/pytoolz/toolz/issues>` for what the
mothership is doing is a great idea.

LICENSE
-------
Three Clause BSD. See `License File <https://github.com/justanr/toolshed/blob/master/LICENSE>`

.. _toolz: https://github.com/pytoolz/toolz/
