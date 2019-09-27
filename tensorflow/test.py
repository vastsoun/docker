#!/usr/bin/python

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import argparse
import numpy as np
import tensorflow as tf


def main():
    # Simple hello world using TensorFlow
    # Create a Constant op
    # The op is added as a node to the default graph.
    # The value returned by the constructor represents the output
    # of the Constant op.
    hello = tf.constant('Hello, TensorFlow!')
    # Start tf session
    sess = tf.Session()
    # Run the op
    print(sess.run(hello))


if __name__ == '__main__':
    main()

# EOF
