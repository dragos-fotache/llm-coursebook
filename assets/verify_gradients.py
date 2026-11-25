"""Independent gradient checks for mlp_numpy.py:
1. Step-size sweep on W1[0, 0] (truncation vs. float64 roundoff).
2. Full 13-entry central-difference check at eps = 1e-5.
3. Independent comparison with PyTorch autograd (if torch is installed),
   including gradient accumulation and torch.no_grad().
"""

import numpy as np
import mlp_numpy as n


def calc(X, Y, params):
    Y_hat, cache = n.forward(X, params)
    loss, E = n.mse_loss(Y_hat, Y)
    grads = n.backward(E, cache, params)
    return loss, grads


def estimate_gradient(X, Y, params, epsilon, param_name, index):
    param = params[param_name]
    theta = param[index]
    param[index] = theta + epsilon
    try:
        Y_hat_plus, _ = n.forward(X, params)
        loss_plus, _ = n.mse_loss(Y_hat_plus, Y)
        param[index] = theta - epsilon
        Y_hat_minus, _ = n.forward(X, params)
        loss_minus, _ = n.mse_loss(Y_hat_minus, Y)
        return (loss_plus - loss_minus) / (2 * epsilon)
    finally:
        param[index] = theta


def numerical_gradients(X, Y, params, epsilon=1e-5):
    num_grads = {}
    for name, param in params.items():
        est = np.empty_like(param)
        for index in np.ndindex(param.shape):
            est[index] = estimate_gradient(X, Y, params, epsilon, name, index)
        num_grads[name] = est
    return num_grads


def make_fixture():
    B, d, h = 4, 2, 3
    rng = np.random.default_rng(0)
    X = rng.normal(size=(B, d))
    params = {
        "W1": rng.normal(size=(d, h)),
        "b1": rng.normal(size=(h,)),
        "W2": rng.normal(size=(h, 1)),
        "b2": rng.normal(size=(1,)),
    }
    Y = rng.normal(size=(B, 1))
    return X, Y, params


def main():
    X, Y, params = make_fixture()
    loss, grads = calc(X, Y, params)
    print(f"Baseline loss: {loss!r}")

    # 1. Step-size sweep on W1[0, 0]
    analytic = grads["W1"][0, 0]
    print(f"\nStep-size sweep on W1[0, 0] (analytic = {analytic:.16e}):")
    for k in range(1, 17):
        eps = 10.0 ** (-k)
        est = estimate_gradient(X, Y, params, eps, "W1", (0, 0))
        err = abs(est - analytic)
        print(f"  eps=1e-{k:02d}  est={est:+.10e}  abs_diff={err:.3e}")

    # 2. Full 13-entry central-difference check at eps = 1e-5
    eps = 1e-5
    tol = 1e-9
    num_grads = numerical_gradients(X, Y, params, epsilon=eps)
    print(f"\nFull 13-entry central-difference check (eps={eps:g}, tol={tol:g}):")
    for name in ("W1", "b1", "W2", "b2"):
        max_diff = float(np.max(np.abs(num_grads[name] - grads[name])))
        assert max_diff < tol, f"{name} exceeded tolerance: {max_diff}"
        print(f"  {name}: max_abs_diff = {max_diff:.3e}")

    # 3. PyTorch autograd check (if installed)
    try:
        import torch
    except ImportError:
        print("\nPyTorch not installed; skipping autograd comparison.")
        return

    X_t = torch.from_numpy(X)
    Y_t = torch.from_numpy(Y)
    params_t = {
        name: torch.from_numpy(arr.copy()).requires_grad_()
        for name, arr in params.items()
    }

    def torch_loss():
        H_t = torch.tanh(X_t @ params_t["W1"] + params_t["b1"])
        Y_hat_t = H_t @ params_t["W2"] + params_t["b2"]
        return torch.mean((Y_hat_t - Y_t) ** 2)

    loss_t = torch_loss()
    loss_t.backward()
    assert abs(loss - loss_t.item()) < 1e-15

    print("\nPyTorch autograd comparison:")
    print(f"  loss abs_diff = {abs(loss - loss_t.item()):.3e}")
    for name in ("W1", "b1", "W2", "b2"):
        max_diff = float(np.max(np.abs(grads[name] - params_t[name].grad.numpy())))
        assert max_diff < 1e-14, f"{name} disagreed with PyTorch: {max_diff}"
        print(f"  {name}: max_abs_diff = {max_diff:.3e}")

    # Gradient accumulation check: second backward without zeroing doubles .grad
    torch_loss().backward()
    for name in ("W1", "b1", "W2", "b2"):
        assert np.allclose(params_t[name].grad.numpy(), 2 * grads[name], rtol=0, atol=1e-14)
    for p in params_t.values():
        p.grad.zero_()
    torch_loss().backward()
    for name in ("W1", "b1", "W2", "b2"):
        assert np.allclose(params_t[name].grad.numpy(), grads[name], rtol=0, atol=1e-14)

    # torch.no_grad() check for inference / parameter update
    with torch.no_grad():
        eval_loss = torch_loss()
        assert not eval_loss.requires_grad
        assert eval_loss.grad_fn is None
    print("  accumulation, zero_(), and torch.no_grad() checks passed.")


if __name__ == "__main__":
    main()
