"""Explicit forward and backward passes for a one-hidden-layer MLP in NumPy.

Network:
    Z1 = X @ W1 + b1
    H = tanh(Z1)
    Y_hat = H @ W2 + b2
    E = Y_hat - Y
    L = mean(E ** 2)

Expected shapes for batch size B, input width d, and hidden width h:
    X: (B, d)
    W1: (d, h),   b1: (h,)
    W2: (h, 1),   b2: (1,)
    Y_hat, Y, E: (B, 1)
"""

import numpy as np


def forward(X, params):
    Z_1 = X @ params["W1"] + params["b1"]
    H = np.tanh(Z_1)
    Y_hat = H @ params["W2"] + params["b2"]
    cache = {"H": H, "X": X}
    return Y_hat, cache


def mse_loss(Y_hat, Y):
    if Y_hat.shape != Y.shape:
        raise ValueError("Y_hat and Y do not have the same shape")
    if Y.ndim != 2 or Y.shape[1] != 1:
        raise ValueError("Wrong shape on Y and Y_hat: they should be (B, 1) column vectors")

    E = Y_hat - Y
    loss = float(np.mean(E**2))
    return loss, E


def backward(E, cache, params):
    H = cache["H"]
    B = H.shape[0]
    X = cache["X"]
    W1 = params["W1"]
    W2 = params["W2"]
    b1 = params["b1"]
    b2 = params["b2"]

    G_Yhat = (2 / B) * E
    G_W2 = H.T @ G_Yhat
    G_b2 = G_Yhat.sum(axis=0)
    G_H = G_Yhat @ W2.T

    G_Z1 = G_H * (1 - H * H)
    G_W1 = X.T @ G_Z1
    G_b1 = G_Z1.sum(axis=0)

    if G_W1.shape != W1.shape:
        raise ValueError("gradients of W1 do not have the same shape as W1")
    if G_b1.shape != b1.shape:
        raise ValueError("gradients of b1 do not have the same shape as b1")
    if G_W2.shape != W2.shape:
        raise ValueError("gradients of W2 do not have the same shape as W2")
    if G_b2.shape != b2.shape:
        raise ValueError("gradients of b2 do not have the same shape as b2")

    return {"W1": G_W1, "b1": G_b1, "W2": G_W2, "b2": G_b2}
