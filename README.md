# puppy

[![Build Status](https://travis-ci.org/coreygirard/puppy.svg?branch=master)](https://travis-ci.org/coreygirard/puppy) <br>
[![Codecov](https://img.shields.io/codecov/c/github/coreygirard/puppy.svg)](https://codecov.io/gh/coreygirard/puppy/)


A featherweight pub/sub architecture genetically engineered to make your project simpler, not more complicated. And to be adorable.

### What's in a name?

Publisher&#8211;Subscriber + Python &#8594; Pub/Sub + .py &#8594; Pub + py &#8594;  ***puppy***


## Hello World

```python
import puppy as pup

puppy = pup.Puppy()

pub = puppy.Pub('topic1')
sub = puppy.SubPull('topic1')

pub.send('hello')
pub.send('world')

print(sub.recv_all())
```
```
['hello', 'world']
```


For those unfamiliar with the Pub/Sub pattern, [Google](https://cloud.google.com/pubsub/docs/overview) and [Wikipedia](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) have pretty useful overviews.

## Installation

```
pip install puppy-pubsub
```

## Usage

[basic usage](docs/basic.md)

[advanced usage](docs/advanced.md)

[reference](docs/reference.md)

## Philosophy

- Prefer simplicity to speed
- Do few things elegantly, rather than many things clumsily
- Puppy is a *tool*, not a *solution*


## Contributing

[guidelines and tutorial](CONTRIBUTING.md)

## License

[MIT](https://tldrlegal.com/license/mit-license)
