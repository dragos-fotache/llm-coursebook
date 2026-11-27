"""Standalone training experiments for Milestone 1, Unit 7.

Uses the verified two-layer NumPy network from ``mlp_numpy.py`` to reproduce:
1. Exercise 1: full-batch gradient descent on y = sin(x), step-0 linear
   prediction ratio at eta = 0.1 vs. eta = 1e-4, and all-zero initialization.
2. Exercise 2: odd-symmetry bias invariance (b1 = 0, b2 = 0) vs. random b1
   initialization, and a two-layer linear network without tanh.
3. Exercise 3: controlled learning-rate sweep (0.005, 0.1, 0.4, 0.6) and
   tanh activation saturation (w1_scale = 0.5 vs. 20.0).
"""

import numpy as np
import mlp_numpy as net


def make_dataset(num_points=64):
    X = np.linspace(-np.pi, np.pi, num_points, dtype=np.float64).reshape(-1, 1)
    Y = np.sin(X)
    return X, Y


def init_params(w1_scale=0.5, b1_scale=0.5, b2_scale=0.0, hidden=8, seed=0):
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0.0, w1_scale, size=(1, hidden))
    b1 = (
        rng.normal(0.0, b1_scale, size=(hidden,))
        if b1_scale > 0.0
        else np.zeros(hidden, dtype=np.float64)
    )
    W2 = rng.normal(0.0, 0.5, size=(hidden, 1))
    b2 = (
        rng.normal(0.0, b2_scale, size=(1,))
        if b2_scale > 0.0
        else np.zeros(1, dtype=np.float64)
    )
    return {"W1": W1, "b1": b1, "W2": W2, "b2": b2}


def forward_linear(X, params):
    Z_1 = X @ params["W1"] + params["b1"]
    Y_hat = Z_1 @ params["W2"] + params["b2"]
    return Y_hat, {"Z_1": Z_1, "X": X}


def backward_linear(E, cache, params):
    X = cache["X"]
    Z_1 = cache["Z_1"]
    W2 = params["W2"]
    B = X.shape[0]

    G_Yhat = (2 / B) * E
    G_W2 = Z_1.T @ G_Yhat
    G_b2 = G_Yhat.sum(axis=0)
    G_Z1 = G_Yhat @ W2.T
    G_W1 = X.T @ G_Z1
    G_b1 = G_Z1.sum(axis=0)
    return {"W1": G_W1, "b1": G_b1, "W2": G_W2, "b2": G_b2}


def grad_norm(grads):
    return float(np.sqrt(sum(np.sum(g**2) for g in grads.values())))


def array_norm(arr):
    return float(np.sqrt(np.sum(arr**2)))


def step_calc(X, Y, params, linear=False):
    if linear:
        Y_hat, cache = forward_linear(X, params)
        loss, E = net.mse_loss(Y_hat, Y)
        grads = backward_linear(E, cache, params)
    else:
        Y_hat, cache = net.forward(X, params)
        loss, E = net.mse_loss(Y_hat, Y)
        grads = net.backward(E, cache, params)
    return loss, grads, cache


def train(X, Y, params, eta, steps, linear=False, loss_cap=1e6):
    params = {k: v.copy() for k, v in params.items()}
    history = {
        "loss": [],
        "gnorm": [],
        "W1": [],
        "b1": [],
        "W2": [],
        "b2": [],
        "mean_dtanh": [],
        "sat_frac": [],
    }
    for _ in range(steps + 1):
        loss, grads, cache = step_calc(X, Y, params, linear=linear)
        history["loss"].append(loss)
        history["gnorm"].append(grad_norm(grads))
        for k in ("W1", "b1", "W2", "b2"):
            history[k].append(array_norm(grads[k]))
        if not linear:
            H = cache["H"]
            history["mean_dtanh"].append(float(np.mean(1.0 - H * H)))
            history["sat_frac"].append(float(np.mean(np.abs(H) > 0.99)))
        if not np.isfinite(loss) or loss > loss_cap:
            break
        for k in params:
            params[k] -= eta * grads[k]
    return params, history


def main():
    X, Y = make_dataset()

    print("=== Exercise 1: baseline (b1=0, b2=0, eta=0.1) ===")
    p0 = init_params(w1_scale=0.5, b1_scale=0.0, b2_scale=0.0)
    _, hist1 = train(X, Y, p0, eta=0.1, steps=2000)
    for s in (0, 1, 10, 100, 500, 1000, 2000):
        print(
            f"step={s:4d}  loss={hist1['loss'][s]:.6f}  |g|={hist1['gnorm'][s]:.6f}"
            f"  |GW1|={hist1['W1'][s]:.4f}  |Gb1|={hist1['b1'][s]:.2e}"
            f"  |GW2|={hist1['W2'][s]:.4f}  |Gb2|={hist1['b2'][s]:.2e}"
        )

    print("\n=== Exercise 1: step-0 local linear prediction ratio ===")
    for eta in (0.1, 1e-4):
        p = {k: v.copy() for k, v in p0.items()}
        l0, g0, _ = step_calc(X, Y, p)
        gn = grad_norm(g0)
        pred = -eta * (gn**2)
        for k in p:
            p[k] -= eta * g0[k]
        l1, _, _ = step_calc(X, Y, p)
        actual = l1 - l0
        print(
            f"eta={eta:<7g}  L0={l0:.6f}  L1={l1:.6f}"
            f"  pred={pred:+.6e}  actual={actual:+.6e}  ratio={actual / pred:.6f}"
        )

    print("\n=== Exercise 1: all-zero initialization ===")
    zeros = {
        "W1": np.zeros((1, 8)),
        "b1": np.zeros(8),
        "W2": np.zeros((8, 1)),
        "b2": np.zeros(1),
    }
    for label, target in [("sin(x)", Y), ("sin(x) + 1", Y + 1.0)]:
        l0, g0, _ = step_calc(X, target, zeros)
        print(
            f"{label:10s}: loss={l0:.4f}"
            f"  |GW1|={array_norm(g0['W1']):.1e}  |Gb1|={array_norm(g0['b1']):.1e}"
            f"  |GW2|={array_norm(g0['W2']):.1e}  |Gb2|={array_norm(g0['b2']):.4f}"
        )

    print("\n=== Exercise 2: symmetry breaking vs. linear 2-layer network ===")
    p_sym = init_params(w1_scale=0.5, b1_scale=0.0, b2_scale=0.0)
    p_rnd = init_params(w1_scale=0.5, b1_scale=0.5, b2_scale=0.0)
    _, h_sym = train(X, Y, p_sym, eta=0.1, steps=2000)
    _, h_rnd = train(X, Y, p_rnd, eta=0.1, steps=2000)
    _, h_lin = train(X, Y, p_rnd, eta=0.1, steps=2000, linear=True)
    print(f"tanh (b1=0):       L0={h_sym['loss'][0]:.6f} -> L2000={h_sym['loss'][-1]:.6f}")
    print(f"tanh (b1~N(0,.5)): L0={h_rnd['loss'][0]:.6f} -> L2000={h_rnd['loss'][-1]:.6f}")
    print(
        f"linear (no tanh):  L0={h_lin['loss'][0]:.6f} -> L2000={h_lin['loss'][-1]:.16f}"
        f"  |g|={h_lin['gnorm'][-1]:.2e}"
    )

    print("\n=== Exercise 3A: learning-rate sweep (500 steps) ===")
    for eta in (0.005, 0.1, 0.4, 0.6):
        _, h = train(X, Y, init_params(0.5), eta=eta, steps=500)
        n_steps = len(h["loss"]) - 1
        print(
            f"eta={eta:<5g}  steps={n_steps:3d}  L0={h['loss'][0]:.6f}"
            f"  L1={h['loss'][1]:.6f}  L_end={h['loss'][-1]:.6f}"
        )

    print("\n=== Exercise 3B: activation saturation (eta=0.1, 500 steps) ===")
    for scale in (0.5, 20.0):
        p_init = init_params(w1_scale=scale)
        _, h = train(X, Y, p_init, eta=0.1, steps=500)
        print(
            f"w1_scale={scale:<4g}: L0={h['loss'][0]:.6f} -> L500={h['loss'][-1]:.6f}"
            f"  mean(1-H^2)={h['mean_dtanh'][0]:.4f}  frac(|H|>0.99)={h['sat_frac'][0]:.4f}"
            f"  |GW1|_0={h['W1'][0]:.4f}  |GW2|_0={h['W2'][0]:.4f}"
        )
        if scale == 20.0:
            x_star = -p_init["b1"] / p_init["W1"][0]
            print(
                f"  transition points x* = -b1/w1 in [{x_star.min():+.4f}, {x_star.max():+.4f}]"
            )


if __name__ == "__main__":
    main()
