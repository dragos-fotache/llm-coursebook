"""A small scalar reverse-mode differentiation engine.

Supports addition and multiplication of Value objects, tanh, and a backward
pass that resets the gradients of all nodes reachable from the chosen output.
Keep data fixed between building a graph and running its backward pass.
"""

import math


class Value:
    def __init__(self, data, parents=()):
        self.data = float(data)
        self.grad = 0.0
        self.parents = tuple(parents)
        self._backward = lambda: None

    def __add__(self, other):
        output = Value(self.data + other.data, (self, other))

        def contribute():
            self.grad += output.grad
            other.grad += output.grad

        output._backward = contribute
        return output

    def __mul__(self, other):
        output = Value(self.data * other.data, (self, other))

        def contribute():
            self.grad += output.grad * other.data
            other.grad += output.grad * self.data

        output._backward = contribute
        return output

    def tanh(self):
        activation = math.tanh(self.data)
        output = Value(activation, (self,))

        def contribute():
            self.grad += output.grad * (1 - activation**2)

        output._backward = contribute
        return output

    def _collect(self, nodes):
        if self in nodes:
            return
        for parent in self.parents:
            parent._collect(nodes)
        nodes[self] = None

    def backward(self):
        nodes = {}
        self._collect(nodes)
        for node in nodes:
            node.grad = 0.0
        self.grad = 1.0
        for node in reversed(list(nodes)):
            node._backward()

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"
